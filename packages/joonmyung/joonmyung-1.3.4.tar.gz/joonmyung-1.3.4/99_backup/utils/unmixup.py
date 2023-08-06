import torch
import torch.nn as nn
from timm.data.mixup import Mixup

import numpy as np
class TMix(Mixup):

    def __init__(self, mixup_alpha=1., switch_prob=0.5, label_smoothing=0.1, num_classes=1000
                 , mixed_ratio_type = 1, patch_size = 16):
        self.mixup_alpha = mixup_alpha
        self.switch_prob = switch_prob
        self.label_smoothing = label_smoothing
        self.mixed_ratio_type = mixed_ratio_type
        self.num_classes = num_classes
        self.patch_size = patch_size
        self.m = nn.Upsample(scale_factor=patch_size, mode='nearest')

    def TokenMix(self, x): # (128, 196, 192)
        B, C, H, W = x.shape
        p = h = H // self.patch_size
        T = p ** 2
        if self.mixed_ratio_type == 1:
            T_mixup_keep = int(T * ((0.75 - 0.25) * torch.rand(1) + 0.25))
        elif self.mixed_ratio_type == 2:
            T_mixup_keep = int(T * max(0.25, min(0.75, np.random.beta(1.0, 1.0))))
        else:
            T_mixup_keep = int(T * 0.5)

        mask     = torch.zeros(B, T, device="cuda").scatter_(1, torch.topk(torch.randn(B, T, device="cuda"), T_mixup_keep, dim=1)[1], 1).unsqueeze(dim=-1)
        mask_img = self.m(mask.reshape(B, 1, p, h).repeat(1,C,1,1))
        x = mask_img * x + (1 - mask_img) * x.flip(0)

        lam = T_mixup_keep / T
        return x, mask, lam

    def __call__(self, imgs, target):
        assert len(imgs) % 2 == 0, 'Batch size should be even when using this'

        use_Tmix = np.random.rand() < self.switch_prob
        if use_Tmix:
            mixed_imgs, mask, lam = self.TokenMix(imgs)
            mixed_target, target_target, source_target = mixup_target(target, self.num_classes, lam, self.label_smoothing, imgs.device)
            return mixed_imgs, mixed_target, mask
        else:
            lam = np.random.beta(self.mixup_alpha, self.mixup_alpha)
            if not lam == 1:
                lam = float(lam)
                x_flipped = imgs.flip(0).mul_(1. - lam)
                imgs.mul_(lam).add_(x_flipped)
            mixed_target, _, _ = mixup_target(target, self.num_classes, lam, self.label_smoothing, imgs.device)  # tuple or tensor

            return imgs, mixed_target, None


class TMix_165(Mixup):
    def __init__(self, mixup_alpha=1., switch_prob=0.5, label_smoothing=0.1, num_classes=1000
                 , mixed_ratio_type = 1, mixed_mask_type = 1, patch_size = 16):
        self.mixup_alpha = mixup_alpha
        self.switch_prob = switch_prob
        self.label_smoothing = label_smoothing
        self.mixed_ratio_type = mixed_ratio_type
        self.mixed_mask_type = mixed_mask_type
        self.num_classes = num_classes
        self.patch_size = patch_size
        self.m = nn.Upsample(scale_factor=patch_size, mode='nearest')

    def TokenMix(self, x): # (128, 196, 192)
        B, C, H, W = x.shape
        p = h = H // self.patch_size
        T = p ** 2
        if self.mixed_ratio_type == 1:
            T_mixup_keep = int(T * ((0.75 - 0.25) * torch.rand(1) + 0.25))
        elif self.mixed_ratio_type == 2:
            T_mixup_keep = int(T * max(0.25, min(0.75, np.random.beta(1.0, 1.0))))
        else:
            T_mixup_keep = int(T * 0.5)
        if self.mixed_mask_type == 0:
            mask     = torch.zeros(B//2, T, device="cuda").scatter_(1, torch.topk(torch.randn(B//2, T, device="cuda"), T_mixup_keep, dim=1)[1], 1).unsqueeze(dim=-1)
            mask = torch.cat([mask, mask.flip(0)], dim=0)
        elif self.mixed_mask_type == 1:
            mask = torch.zeros(B, T, device="cuda").scatter_(1, torch.topk(torch.randn(B, T, device="cuda"), T_mixup_keep, dim=1)[1], 1).unsqueeze(dim=-1)
        else:
            raise ValueError
        mask_img = self.m(mask.reshape(B, 1, p, h).expand(-1,C,-1,-1))
        x = mask_img * x + (1 - mask_img) * x.flip(0)

        lam = T_mixup_keep / T
        return x, mask, lam

    def __call__(self, imgs, target):
        assert len(imgs) % 2 == 0, 'Batch size should be even when using this'

        use_Tmix = np.random.rand() < self.switch_prob
        if use_Tmix:
            mixed_imgs, mask, lam = self.TokenMix(imgs)
            mixed_target, target_target, source_target = mixup_target(target, self.num_classes, lam, self.label_smoothing, imgs.device)
            return mixed_imgs, mixed_target, mask
        else:
            lam = np.random.beta(self.mixup_alpha, self.mixup_alpha)
            if not lam == 1:
                lam = float(lam)
                x_flipped = imgs.flip(0).mul_(1. - lam)
                imgs.mul_(lam).add_(x_flipped)
            mixed_target, _, _ = mixup_target(target, self.num_classes, lam, self.label_smoothing, imgs.device)  # tuple or tensor

            return imgs, mixed_target, None