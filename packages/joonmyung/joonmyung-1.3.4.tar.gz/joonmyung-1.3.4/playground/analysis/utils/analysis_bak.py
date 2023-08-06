from playground.analysis.lib_import import *
import torch

class Analysis:
    def __init__(self, model, key_name=None, attn_name_in='attn_drop', attn_name_out = 'decoder'
                 , cls_start=0, cls_end=1, patch_start=1, patch_end=None
                 , device="cuda"):
        # Section A. Model
        self.model = model
        self.key_name = key_name

        # Section B. Attention
        self.kwargs_roll = {"cls_start" : cls_start, "cls_end" : cls_end
                            , "patch_start" : patch_start, "patch_end" : patch_end}

        # Section C. Setting
        self.device = device
        for name, module in self.model.named_modules():
            if (attn_name_in in name) and (attn_name_out not in name):
                module.register_forward_hook(self.get_attention)
                module.register_backward_hook(self.get_gradient)

    def get_attention(self, module, input, output):
        self.attentions.append(output.cpu())

    def get_gradient(self, module, grad_input, grad_output):
        self.gradients.append(grad_input[0].cpu())

    def __call__(self, input_tensors, index=None, **kwargs):
        self.attentions, self.gradients, self.result = [], [], {}
        self.model.zero_grad()
        self.model.eval()
        outputs = self.model(input_tensors, **kwargs)

        if type(outputs) == tuple:
            self.output = outputs[0][self.key_name] if type(outputs[0]) == dict else outputs[0]
        else:
            self.output = outputs

        return outputs
    def rollout(self, attn=True, grad=False, index=None,
                head_fusion="mean", discard_ratios=0.9, data_from="cls"
                , starts=[0], ls=None, bs=None
                , reshape=False, mean=True):

        attns = []
        if attn:
            attns.append(self.attentions)
        if grad:
            self.gradients = []
            self.model.zero_grad()
            if index == None: index = self.output.max(dim=1)[1]
            index = torch.eye(1000, device=self.device)[index]
            loss = (self.output * index).sum()
            loss.backward(retain_graph=True)
            attns.append(self.gradients)

        return rollout(*attns
                       , head_fusion=head_fusion, discard_ratios=discard_ratios, data_from=data_from
                       , starts=starts, ls=ls, bs=bs
                       , reshape=reshape, mean=mean)


if __name__ == '__main__':
    # Section A. Data
    dataset_name, server, device = "imagenet", "148", 'cuda'
    data_path, _ = data2path(server, dataset_name)
    data_num = [[0, 0], [1, 0], [2, 0], [3, 0], [0, 1], [1, 1], [2, 1], [3, 1]]

    dataset = JDataset(data_path, dataset_name, device=device)
    samples, targets, imgs, label_names = dataset.getItems(data_num)

    # Section B. Model
    # model_number, model_name = 0, "vit_small_patch16_224"
    model_number, model_name = 1, "deit_tiny_patch16_224"
    modelMaker = JModel(model_name, dataset.num_classes, model_number=model_number, device=device)
    model, args = modelMaker.getModel()

    model = Analysis(model, device=device)
    _, rolls = model(samples)

    rollout_attn = model.rollout(True, False)
    datas = overlay(dataset.unNormalize(samples), rollout_attn)
    drawImgPlot(datas)
