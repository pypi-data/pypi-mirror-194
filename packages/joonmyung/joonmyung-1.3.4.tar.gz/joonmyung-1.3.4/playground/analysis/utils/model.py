from playground.analysis.project.ICCV2023.versions.register_models import *
from playground.analysis.project.Timms import *
from joonmyung.utils import isDir
from timm import create_model
import torch
import os

class JModel():
    def __init__(self, model_name = None, num_classes = None
                 , model_path= None
                 , model_number = 0, device="cuda", p=False):
        # Pretrained_Model
        self.model_name = model_name
        self.num_classes = num_classes

        # Other
        self.model_path = model_path
        self.model_number = model_number
        if p and model_path:
            print("file list : ", sorted(os.listdir("/" + os.path.join(*model_path.split("/")[:-1])), reverse=True))
        self.device = device

    def getModel(self, epoch=0):
        model, args = None, None
        if self.model_number == 0:
            model = create_model(self.model_name, pretrained=True, num_classes=self.num_classes, in_chans=3, global_pool=None, scriptable=False).to(self.device)
        elif self.model_number == 1:
            model = torch.hub.load('facebookresearch/deit:main', self.model_name, pretrained=True).to(self.device)
        elif self.model_number == 2:
            model_path = self.model_path.format(str(epoch))
            if not isDir(model_path): raise FileExistsError

            checkpoint = torch.load(model_path, map_location='cpu')
            args = checkpoint['args']
            model = get_model(args).to(self.device)
            model.load_state_dict(checkpoint['model'])

        model.eval()

        return model, args


