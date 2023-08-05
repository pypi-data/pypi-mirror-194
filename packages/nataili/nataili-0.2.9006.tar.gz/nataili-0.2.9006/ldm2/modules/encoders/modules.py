import math
import os
import torch
import torch.nn as nn
from torch.utils.checkpoint import checkpoint

from transformers import T5Tokenizer, T5EncoderModel, CLIPTokenizer, CLIPTextModel

import open_clip
from ldm2.util import default, count_params
from nataili.util.logger import logger


class AbstractEncoder(nn.Module):
    def __init__(self):
        super().__init__()

    def encode(self, *args, **kwargs):
        raise NotImplementedError


class IdentityEncoder(AbstractEncoder):

    def encode(self, x):
        return x


class ClassEmbedder(nn.Module):
    def __init__(self, embed_dim, n_classes=1000, key='class', ucg_rate=0.1):
        super().__init__()
        self.key = key
        self.embedding = nn.Embedding(n_classes, embed_dim)
        self.n_classes = n_classes
        self.ucg_rate = ucg_rate

    def forward(self, batch, key=None, disable_dropout=False):
        if key is None:
            key = self.key
        # this is for use in crossattn
        c = batch[key][:, None]
        if self.ucg_rate > 0. and not disable_dropout:
            mask = 1. - torch.bernoulli(torch.ones_like(c) * self.ucg_rate)
            c = mask * c + (1-mask) * torch.ones_like(c)*(self.n_classes-1)
            c = c.long()
        c = self.embedding(c)
        return c

    def get_unconditional_conditioning(self, bs, device="cuda"):
        uc_class = self.n_classes - 1  # 1000 classes --> 0 ... 999, one extra class for ucg (class 1000)
        uc = torch.ones((bs,), device=device) * uc_class
        uc = {self.key: uc}
        return uc


def disabled_train(self, mode=True):
    """Overwrite model.train with this function to make sure train/eval mode
    does not change anymore."""
    return self


class FrozenT5Embedder(AbstractEncoder):
    """Uses the T5 transformer encoder for text"""
    def __init__(self, version="google/t5-v1_1-large", device="cuda", max_length=77, freeze=True):  # others are google/t5-v1_1-xl and google/t5-v1_1-xxl
        super().__init__()
        self.tokenizer = T5Tokenizer.from_pretrained(version)
        self.transformer = T5EncoderModel.from_pretrained(version)
        self.device = device
        self.max_length = max_length   # TODO: typical value?
        if freeze:
            self.freeze()

    def freeze(self):
        self.transformer = self.transformer.eval()
        #self.train = disabled_train
        for param in self.parameters():
            param.requires_grad = False

    def forward(self, text):
        batch_encoding = self.tokenizer(text, truncation=True, max_length=self.max_length, return_length=True,
                                        return_overflowing_tokens=False, padding="max_length", return_tensors="pt")
        tokens = batch_encoding["input_ids"].to(self.device)
        outputs = self.transformer(input_ids=tokens)

        z = outputs.last_hidden_state
        return z

    def encode(self, text):
        return self(text)


class FrozenCLIPEmbedder(AbstractEncoder):
    """Uses the CLIP transformer encoder for text (from Hugging Face)"""
    def __init__(self, version="openai/clip-vit-large-patch14", device="cuda", max_length=77):
        super().__init__()
        # TODO: Update this
        if os.path.exists("models/clip-vit-large-patch14"):
            self.tokenizer = CLIPTokenizer.from_pretrained("models/clip-vit-large-patch14")
            self.transformer = CLIPTextModel.from_pretrained("models/clip-vit-large-patch14")
        else:
            self.tokenizer = CLIPTokenizer.from_pretrained(version)
            self.transformer = CLIPTextModel.from_pretrained(version)
        self.device = device
        self.max_length = max_length
        self.chunk_length = 75
        self.freeze()

        vocab = self.tokenizer.get_vocab()
        self.comma_token = vocab.get(',</w>', None)
        self.id_start = self.tokenizer.bos_token_id
        self.id_end = self.tokenizer.eos_token_id
        self.id_pad = self.id_end

    def empty_chunk(self):
        """creates an empty PromptChunk and returns it"""

        chunk = PromptChunk()
        chunk.tokens = [self.id_start] + [self.id_end] * (self.chunk_length + 1)
        return chunk

    def freeze(self):
        self.transformer = self.transformer.eval()
        for param in self.parameters():
            param.requires_grad = False

    def get_target_prompt_token_count(self, token_count):
        """returns the maximum number of tokens a prompt of a known length can have before it requires one more PromptChunk to be represented"""

        return math.ceil(max(token_count, 1) / self.chunk_length) * self.chunk_length

    def tokenize(self, texts):
        tokenized = self.tokenizer(texts, truncation=False, add_special_tokens=False)["input_ids"]

        return tokenized

    def encode_with_transformers(self, tokens, clip_skip):
        outputs = self.transformer(input_ids=tokens, output_hidden_states=True)

        if clip_skip > 1:
            z = outputs.hidden_states[-clip_skip]
            z = self.transformer.text_model.final_layer_norm(z)
        else:
            z = outputs.last_hidden_state

        return z

    def encode_embedding_init_text(self, init_text, nvpt):
        """Converts text into a tensor with this text's tokens' embeddings. Note that those are embeddings before they are passed through
        transformers. nvpt is used as a maximum length in tokens. If text produces less teokens than nvpt, only this many is returned."""

        raise NotImplementedError
    
    def tokenize_line(self, line):
        """
        this transforms a single prompt into a list of PromptChunk objects - as many as needed to
        represent the prompt.
        Returns the list and the total number of tokens in the prompt.
        """
        tokenized = self.tokenize(line)

        chunks = []
        chunk = PromptChunk()
        token_count = 0
        last_comma = -1

        def next_chunk():
            """puts current chunk into the list of results and produces the next one - empty"""
            nonlocal token_count
            nonlocal last_comma
            nonlocal chunk
            token_count += len(chunk.tokens)
            to_add = self.chunk_length - len(chunk.tokens)
            if to_add > 0:
                chunk.tokens += [self.id_end] * to_add

            chunk.tokens = [self.id_start] + chunk.tokens + [self.id_end]

            last_comma = -1
            chunks.append(chunk)
            chunk = PromptChunk()

        for tokens in zip(tokenized):
            position = 0
            while position < len(tokens):
                token = tokens[position]

                if token == self.comma_token:
                    last_comma = len(chunk.tokens)

                elif len(chunk.tokens) == self.chunk_length and last_comma != -1 and len(chunk.tokens) - last_comma <= 20:
                    break_location = last_comma + 1

                    reloc_tokens = chunk.tokens[break_location:]
                    chunk.tokens = chunk.tokens[:break_location]

                    next_chunk()
                    chunk.tokens = reloc_tokens

                if len(chunk.tokens) == self.chunk_length:
                    next_chunk()

                chunk.tokens.append(token)
                position += 1

        if len(chunk.tokens) > 0 or len(chunks) == 0:
            next_chunk()

        return chunks, token_count

    def process_texts(self, text):
        token_count = 0
        batch_chunks = []
        chunks, current_token_count = self.tokenize_line(text)
        token_count = max(current_token_count, token_count)

        batch_chunks.append(chunks)
        return batch_chunks, token_count
    
    def process_tokens(self, remade_batch_tokens, clip_skip):
        """
        sends one single prompt chunk to be encoded by transformers neural network.
        remade_batch_tokens is a batch of tokens - a list, where every element is a list of tokens; usually
        there are exactly 77 tokens in the list.
        """
        tokens = torch.asarray(remade_batch_tokens).to(self.device)

        # this is for SD2: SD1 uses the same token for padding and end of text, while SD2 uses different ones.
        if self.id_end != self.id_pad:
            for batch_pos in range(len(remade_batch_tokens)):
                index = remade_batch_tokens[batch_pos].index(self.id_end)
                tokens[batch_pos, index+1:tokens.shape[1]] = self.id_pad

        z = self.encode_with_transformers(tokens, clip_skip)

        return z

    def forward(self, text, clip_skip):
        if len(text) < 50:
            batch_encoding = self.tokenizer(text, truncation=True, max_length=self.max_length, return_length=True,
                                            return_overflowing_tokens=False, padding="max_length", return_tensors="pt")
            tokens = batch_encoding["input_ids"].to(self.device)
            z = self.encode_with_transformers(tokens, clip_skip)

            return z
        
        else:
            batch_chunks, token_count = self.process_texts(text)
            logger.debug(f"Token count for prompt = {token_count}")
            chunk_count = max([len(x) for x in batch_chunks])

            zs = []
            for i in range(chunk_count):
                batch_chunk = [chunks[i] if i < len(chunks) else self.empty_chunk() for chunks in batch_chunks]

                tokens = [x.tokens for x in batch_chunk]

                z = self.process_tokens(tokens, clip_skip)
                zs.append(z)

            return torch.hstack(zs)

    def encode(self, text, clip_skip):
        return self(text, clip_skip)


class FrozenOpenCLIPEmbedder(AbstractEncoder):
    """
    Uses the OpenCLIP transformer encoder for text
    """
    LAYERS = [
        #"pooled",
        "last",
        "penultimate"
    ]
    def __init__(self, arch="ViT-H-14", version="laion2b_s32b_b79k", device="cuda", max_length=77,
                 freeze=True, layer="last"):
        super().__init__()
        assert layer in self.LAYERS
        model, _, _ = open_clip.create_model_and_transforms(arch, device=torch.device('cpu'), pretrained=version)
        del model.visual
        self.model = model

        self.device = device
        self.max_length = max_length
        if freeze:
            self.freeze()
        self.layer = layer
        if self.layer == "last":
            self.layer_idx = 0
        elif self.layer == "penultimate":
            self.layer_idx = 1
        else:
            raise NotImplementedError()

    def freeze(self):
        self.model = self.model.eval()
        for param in self.parameters():
            param.requires_grad = False

    def forward(self, text, clip_skip=None):
        tokens = open_clip.tokenize(text)
        z = self.encode_with_transformer(tokens.to(self.device))
        return z

    def encode_with_transformer(self, text):
        x = self.model.token_embedding(text)  # [batch_size, n_ctx, d_model]
        x = x + self.model.positional_embedding
        x = x.permute(1, 0, 2)  # NLD -> LND
        x = self.text_transformer_forward(x, attn_mask=self.model.attn_mask)
        x = x.permute(1, 0, 2)  # LND -> NLD
        x = self.model.ln_final(x)
        return x

    def text_transformer_forward(self, x: torch.Tensor, attn_mask = None):
        for i, r in enumerate(self.model.transformer.resblocks):
            if i == len(self.model.transformer.resblocks) - self.layer_idx:
                break
            if self.model.transformer.grad_checkpointing and not torch.jit.is_scripting():
                x = checkpoint(r, x, attn_mask)
            else:
                x = r(x, attn_mask=attn_mask)
        return x

    def encode(self, text, clip_skip=None):
        return self(text)


class FrozenCLIPT5Encoder(AbstractEncoder):
    def __init__(self, clip_version="openai/clip-vit-large-patch14", t5_version="google/t5-v1_1-xl", device="cuda",
                 clip_max_length=77, t5_max_length=77):
        super().__init__()
        self.clip_encoder = FrozenCLIPEmbedder(clip_version, device, max_length=clip_max_length)
        self.t5_encoder = FrozenT5Embedder(t5_version, device, max_length=t5_max_length)
        print(f"{self.clip_encoder.__class__.__name__} has {count_params(self.clip_encoder)*1.e-6:.2f} M parameters, "
              f"{self.t5_encoder.__class__.__name__} comes with {count_params(self.t5_encoder)*1.e-6:.2f} M params.")

    def encode(self, text):
        return self(text)

    def forward(self, text):
        clip_z = self.clip_encoder.encode(text)
        t5_z = self.t5_encoder.encode(text)
        return [clip_z, t5_z]


class PromptChunk:

    def __init__(self):
        self.tokens = []
