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
    if kwargs["wandb_version"] == "1.3.2":
        from .deit_132 import VisionTransformer
    else:
        from .deit import VisionTransformer
    model = VisionTransformer(
        num_heads=num_heads,
        norm_layer=partial(nn.LayerNorm, eps=1e-6), **kwargs)
    model.default_cfg = _cfg()

    return model