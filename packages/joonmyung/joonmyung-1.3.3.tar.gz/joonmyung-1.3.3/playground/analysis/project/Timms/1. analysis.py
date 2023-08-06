from playground.analysis.project.ICCV2023.versions.register_models import get_mixup_fn
from playground.analysis.lib_import import *
import os

# Section A. Setting
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
view = [False, True, True, False, False] # [IMAGE, ROLL_ATTN, ROLL_GRAD, OTHER]
evaluation = [False] # Evaluation
save_path, save, p, device = '/hub_data/joonmyung/conference/playgrounds/results/', False, True, 'cuda'

# Section B. Data
dataset_name, server = "imagenet", "148"
data_path, _ = data2path(server, dataset_name)
data_num = [[0, 0], [1, 0], [2, 0], [3, 0], [0, 1], [1, 1], [2, 1], [3, 1]]

dataset = JDataset(data_path, dataset_name, device=device)
samples, targets, imgs, label_names = dataset.getItems(data_num)


# Section C. Model Load
# model_number, model_name = 0, "vit_small_patch16_224"
model_number, model_name = 1, "deit_tiny_patch16_224"
modelMaker = JModel(model_name, dataset.num_classes, model_number=model_number, device=device, p=p)
model, args = modelMaker.getModel()

model = Analysis(model, device=device)
_ = model(samples)

if evaluation[0]: evaluate(dataset.getAllItems(), model, device="cuda")

if view[0]: drawImgPlot(dataset.unNormalize(samples), columns = label_names, col=len(samples))

# Section D. Analysis
# bs, ls, starts, col = None, None, [0], len(samples)
# discard_ratios, head_fusion, category_index, data_from = [0.0, 0.3, 0.6, 0.9], "mean", targets, "cls"  # Attention, Gradient
bs, ls, starts, col = None, [0, 4, 8, 11], None, len(samples)
discard_ratios, head_fusion, category_index, data_from = [0.0, 0.9], "mean", targets, "cls"  # Attention, Gradient
if view[1]: # Attention Map
    rollout_attn     = model.rollout(True, False, head_fusion=head_fusion, discard_ratios = discard_ratios
                                     , starts=starts, ls=ls, bs=bs, data_from=data_from
                                     , mean=True, reshape=True)
    datas = overlay(samples, rollout_attn, dataset_name)
    drawImgPlot(datas, col=col)

if view[2]: # Gradient
    rollout_attn = model.rollout(False, True, index=category_index, head_fusion=head_fusion, discard_ratios=discard_ratios
                                 , starts=starts, ls=ls, bs=bs, data_from=data_from
                                 , mean=True, reshape=True)
    datas = overlay(samples, rollout_attn, dataset_name)
    drawImgPlot(datas, col=col)

