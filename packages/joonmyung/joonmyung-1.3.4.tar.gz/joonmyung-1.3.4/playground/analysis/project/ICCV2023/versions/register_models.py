# Copyright (c) 2015-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the CC-by-NC license found in the
# LICENSE file in the root directory of this source tree.
#

import torch
import torch.nn as nn
from functools import partial

from timm.models.vision_transformer import _cfg
from timm.models.registry import register_model


@register_model
def deit_tiny(pretrained=False, **kwargs):
    num_heads = 3                    # 3 & 64 : DeiT
    kwargs['embed_dim'] *= num_heads # 4 & 48 : ConViT
    if kwargs["wandb_version"] <= "1.7.4":
        from .V174.models.deit import VisionTransformer
    elif kwargs["wandb_version"] <= "1.7.5":
        from .V175.models.deit import VisionTransformer
    elif kwargs["wandb_version"] <= "1.7.8":
        from .V178.models.deit import VisionTransformer
    else:
        raise ValueError
    model = VisionTransformer(
        num_heads=num_heads,
        norm_layer=partial(nn.LayerNorm, eps=1e-6), **kwargs)
    model.default_cfg = _cfg()

    return model

def get_model(args):
    from timm import create_model
    if args.wandb_version <= "1.7.4":
        model = create_model(args.model, pretrained=args.pretrained, num_classes=args.nb_classes, drop_rate=args.drop, drop_path_rate=args.drop_path, drop_block_rate=args.drop_block, embed_dim=args.embed_dim, input_size=args.input_size, cls_token_num=args.cls_token_num,
                             decoder_param=args.decoder_param, norm_pix_loss=args.norm_pix_loss, mae_task_type=args.mae_task_type,
                             wandb_version=args.wandb_version)
    elif args.wandb_version <= "1.7.5":
        model = create_model(args.model, pretrained=args.pretrained, num_classes=args.nb_classes, drop_rate=args.drop, drop_path_rate=args.drop_path, drop_block_rate=args.drop_block, embed_dim=args.embed_dim, input_size=args.input_size, cls_token_num=args.cls_token_num,
                             decoder_param=args.decoder_param, norm_pix_loss=args.norm_pix_loss, mae_task_type=args.mae_task_type, tmix_type=args.tmix_type,
                             wandb_version=args.wandb_version)
    elif args.wandb_version <= "1.7.8":
        model=create_model(args.model,pretrained=args.pretrained,num_classes=args.nb_classes,drop_rate=args.drop,drop_path_rate=args.drop_path,drop_block_rate=args.drop_block,embed_dim=args.embed_dim,input_size=args.input_size,cls_token_num=args.cls_token_num,decoder_param=args.decoder_param,norm_pix_loss=args.norm_pix_loss,mae_task_type=args.mae_task_type,mae_target_detach=args.mae_target_detach,tmix_type=args.tmix_type,
                                 wandb_version=args.wandb_version)
    else:
        raise ValueError
    return model

def get_mixup_fn(args):
    if args.wandb_version <= "1.7.4":
        from .V174.utils.tmix import TMix
        mixup_fn = TMix(
            mixup_alpha=args.mixup, switch_prob=1.0, label_smoothing=args.smoothing,
            cls_token_num=args.cls_token_num, mixed_ratio_type=args.mixed_ratio_type,
            mae_task_type=args.mae_task_type,
            num_classes=args.nb_classes)
    elif args.wandb_version <= "1.7.5":
        from .V175.utils.tmix import TMix
        mixup_fn = TMix(
            mixup_alpha=args.mixup, switch_prob=1.0, label_smoothing=args.smoothing,
            cls_token_num=args.cls_token_num, mixed_ratio_type=args.mixed_ratio_type, tmix_type=args.tmix_type,
            mae_task_type=args.mae_task_type,
            num_classes=args.nb_classes)
    elif args.wandb_version <= "1.7.8":
        from .V178.utils.tmix import TMix
        mixup_fn = TMix(
            mixup_alpha=args.mixup, switch_prob=1.0, label_smoothing=args.smoothing,
            cls_token_num=args.cls_token_num, mixed_ratio_type=args.mixed_ratio_type, tmix_type=args.tmix_type,
            mae_task_type=args.mae_task_type, use_bce=args.use_bce,
            num_classes=args.nb_classes)


    return mixup_fn