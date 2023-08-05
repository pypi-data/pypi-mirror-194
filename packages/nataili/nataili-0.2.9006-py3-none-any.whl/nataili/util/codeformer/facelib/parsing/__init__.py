import torch

from nataili.util.codeformer.facelib.parsing.bisenet import BiSeNet
from nataili.util.codeformer.facelib.parsing.parsenet import ParseNet
from nataili.util.codeformer.misc import load_file_from_url


def init_parsing_model(model_name="bisenet", half=False, device="cuda"):
    if model_name == "bisenet":
        model = BiSeNet(num_class=19)
        model_url = "https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/parsing_bisenet.pth"
    elif model_name == "parsenet":
        model = ParseNet(in_size=512, out_size=512, parsing_ch=19)
        model_url = (
            "https://s3.eu-central-1.wasabisys.com/nextml-model-data/codeformer/weights/facelib/parsing_parsenet.pth"
        )
    else:
        raise NotImplementedError(f"{model_name} is not implemented.")

    model_path = load_file_from_url(url=model_url, model_dir="weights/facelib", progress=True, file_name=None)
    load_net = torch.load(model_path, map_location=lambda storage, loc: storage)
    model.load_state_dict(load_net, strict=True)
    model.eval()
    model = model.to(device)
    return model
