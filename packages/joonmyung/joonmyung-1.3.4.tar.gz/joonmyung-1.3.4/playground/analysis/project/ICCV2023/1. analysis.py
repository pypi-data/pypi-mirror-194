from playground.analysis.project.ICCV2023.versions.register_models import get_mixup_fn
from playground.analysis.lib_import import *
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Section A. Setting
view = [False, True, True, False, False] # [IMAGE, ROLL_ATTN, ROLL_GRAD, OTHER]
evaluation = [False] # Evaluation
save_path, save, p, device = '/hub_data/joonmyung/conference/playgrounds/results/', False, True, 'cuda'
server, conference, version, name = "148", "2023ICCV", "1.7.8", "OURS:P:01"


# Section B. Data
dataset_name, mixup = "imagenet", False
data_path, root_path = data2path(server, dataset_name, conference, version, name)
data_num = [[0, 0], [1, 0], [2, 0], [3, 0], [0, 1], [1, 1], [2, 1], [3, 1]]

dataset = JDataset(data_path, dataset_name, device=device)
samples, targets, imgs, label_names = dataset.getItems(data_num)
if view[0]: drawImgPlot(dataset.unNormalize(samples), columns = label_names, col=len(samples))


# Section C. Model Load
model_number, model_path, model_name, epoch = 1, None, None, None
if model_number == 0:
    model_name = "vit_small_patch16_224"
elif model_number == 1:
    model_name = "deit_tiny_patch16_224"
elif model_number == 2:
    epoch = 20
    model_path = os.path.join(root_path, "checkpoint_{}.pth")
modelMaker = JModel(model_name, dataset.num_classes, model_path, model_number=model_number, device=device, p=p)
model, args = modelMaker.getModel(epoch)

if evaluation[0]: evaluate(dataset.getAllItems(), model, device="cuda")

if model_number in [0, 1]: # torch.hub or timm pretrained
    model = Analysis(model, device=device)
    _ = model(samples)
elif model_number == 2: # 2023ICCV
    if version == "1.7.8":
        samples_, targets_, tmix_info = samples, targets, {}
        if mixup:
            mixup_fn = get_mixup_fn(args)
            samples, targets, tmix_info = mixup_fn(samples, targets, model)

        key_name = "output_all"
        CTN = args.cls_token_num
        UTN = args.mae_task_type[2]
        DTN = args.mae_task_type[6]
        ATN = 1 if args.mae_task_type[4] else 0

        model = Analysis(model, cls_start = 0, cls_end = CTN, patch_start = CTN + UTN * 2 + DTN + ATN
                         , key_name=key_name, device=device)
        _, info = model(samples, samples_, tmix_info=tmix_info, analysis=3)



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

if view[3]:
    datas = [dataset.unNormalize(samples_), dataset.unNormalize(samples), dataset.unNormalize(samples_.flip(0)), dataset.unNormalize(info["mae_pred_1"]), dataset.unNormalize(info["mae_pred_2"])]
    drawImgPlot(datas, col=len(datas))
