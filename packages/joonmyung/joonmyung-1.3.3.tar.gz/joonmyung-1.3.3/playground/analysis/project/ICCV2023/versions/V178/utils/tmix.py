from timm.data.mixup import Mixup, one_hot

import torch.nn as nn
import numpy as np
import torch




def mixup_target(target, num_classes, lam=1., smoothing=0.0, device='cuda'):
    off_value = smoothing / num_classes
    on_value = 1. - smoothing + off_value
    y1 = one_hot(target, num_classes, on_value=on_value, off_value=off_value, device=device)
    y2 = one_hot(target.flip(0), num_classes, on_value=on_value, off_value=off_value, device=device)
    mixed_target = y1 * lam + y2 * (1. - lam)
    return mixed_target, y1, y2


def batch_index_generate(x, idx):
    if len(x.size()) == 3:
        B, N, C = x.size()
        offset = torch.arange(B, dtype=torch.long, device=x.device).view(B, 1) * N
        idx = idx + offset
        return idx.reshape(-1)
    elif len(x.size()) == 2:
        B, N = x.size()
        offset = torch.arange(B, dtype=torch.long, device=x.device).view(B, 1) * N
        idx = idx + offset
        return idx
    else:
        raise NotImplementedError


import copy

@torch.no_grad()
def rollout(attentions, head_fusion="mean", discard_ratio = 0.1, starts=[0], ls=None, bs=None, point="cls"
            , cls_start=0, cls_end=1, patch_start=1, patch_end=None
            , reshape=False, mean = True):
    # attentions : L * (B, H, h, w)
    device = attentions[0].device
    if type(attentions) == list: attentions = torch.stack(attentions, dim=0) # (L, B, H, w, h)

    if head_fusion == "mean":
        attentions = attentions.mean(axis=2) #
    elif head_fusion == "max":
        attentions = attentions.max(axis=2)[0]
    elif head_fusion == "min":
        attentions = attentions.min(axis=2)[0]
    elif head_fusion == "median":
        attentions = attentions.median(axis=2)[0]
    else:
        raise "Attention head fusion type Not supported"

    if bs is not None:
        attentions = attentions[:, bs]

    _, B, _, T = attentions.shape
    H = W = int(T ** 0.5)
    if starts is not None:
        results, I = [], torch.eye(T, device=device).unsqueeze(0).expand(B, -1, -1)  # (B, 197, 197)
        for start in starts:
            result = I
            for attn in copy.deepcopy(attentions[start:]):  # (L, B, w, h)
                flat = attn.reshape(B, -1)
                _, indices = flat.topk(int(flat.shape[-1] * discard_ratio), -1, False)
                indices = indices * (indices != 0)
                for b in range(B):
                    flat[b, indices[b]] = 0

                attn = (attn + 1.0 * I) / 2
                attn = attn / attn.sum(dim=-1, keepdim=True)
                result = torch.matmul(attn, result)  # (1, 197, 197)
                # cls_start

            result = result[:, cls_start:cls_end, patch_start:patch_end] if point == "cls" else result[:, patch_start:patch_end, patch_start:patch_end]
            if mean:
                result = result.mean(dim=1) if mean else result
            result = result / result.max(dim=-1, keepdim=True)[0]
            results.append(result)
        results = torch.stack(results, dim=0)

    if ls is not None:
        results = attentions[ls, :, cls_start:cls_end, patch_start:patch_end] if point == "cls" else attentions[ls, :, patch_start:patch_end, patch_start:patch_end].mean(dim=2)

    return results.reshape(-1, B, H, W) if reshape else results

class TMix(Mixup):

    def __init__(self, mixup_alpha = 1., switch_prob=0.5, label_smoothing=0.1,
                 mixed_ratio_type=1, tmix_type=0, use_bce=False,
                 cls_token_num = 0, mae_task_type = None,
                 num_classes=1000, patch_size = 16):
        self.mixup_alpha = mixup_alpha
        self.switch_prob = switch_prob
        self.label_smoothing = label_smoothing

        self.mixed_target_type = mae_task_type[0]
        self.unmix_token_num = mae_task_type[2]
        self.mixed_ratio_type = mixed_ratio_type
        self.tmix_type = tmix_type
        self.cls_token_num = cls_token_num
        self.use_bce = use_bce


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
        mask_idx = torch.topk(torch.randn(B, T, device="cuda"), T, dim=1)[1]
        mask_p = mask_idx[:,:T_mixup_keep]
        mask_n = mask_idx[:,T_mixup_keep:]
        mask     = torch.zeros(B, T, device="cuda").scatter_(1, mask_p, 1).unsqueeze(dim=-1)
        mask_img = self.m(mask.reshape(B, 1, p, h).repeat(1,C,1,1))
        x = mask_img * x + (1 - mask_img) * x.flip(0)

        lam = T_mixup_keep / T
        return x, mask, mask_p, mask_n, lam

    def __call__(self, imgs, targets, model=None):
        assert len(imgs) % 2 == 0, 'Batch size should be even when using this'
        info_tmix = {}

        use_Tmix = np.random.rand() < self.switch_prob
        if use_Tmix:
            mixed_imgs, mask, mask_p, mask_n, lam = self.TokenMix(imgs)

            info_tmix["mask"] = mask
            info_tmix["mask_p"] = mask_p
            info_tmix["mask_n"] = mask_n

            if self.mixed_target_type or self.tmix_type == 2: # Relabeling or need Feature
                with torch.no_grad():
                    model.eval()
                    info = model(imgs, analysis=self.tmix_type)
                    model.train()

            if self.mixed_target_type:
                if self.mixed_target_type == 1:
                    attn = info["encoder_attn"][-1][:, :, self.cls_token_num + self.unmix_token_num * 2:, self.cls_token_num + self.unmix_token_num * 2:].mean(dim=[1,2]) # (B, T)
                elif self.mixed_target_type == 2:
                    # attn = rollout(info["encoder_attn"], "mean").mean(dim=[1])  # (B, T)
                    attn = rollout(info["encoder_attn"], "mean", starts=[0], point="cls"
                                   , cls_start=0, cls_end=self.cls_token_num, patch_start=self.cls_token_num + self.unmix_token_num * 2, patch_end=None
                                   , discard_ratio=0.6)[0]

                elif self.mixed_target_type == 3:
                    attn = info["encoder_attn"][-1][:,:,:self.cls_token_num + self.unmix_token_num * 2, self.cls_token_num + self.unmix_token_num * 2:].mean(dim=[1,2])

                _, targets_p, targets_n = mixup_target(targets, self.num_classes, lam=1., smoothing=self.label_smoothing, device=imgs.device)
                attn_A = (attn.unsqueeze(-1) * mask).sum(1) / attn.unsqueeze(-1).sum(dim=1)  # (B, 1)
                attn_B = (attn.unsqueeze(-1).flip(0) * (1 - mask)).sum(1) / attn.unsqueeze(-1).flip(0).sum(dim=1)  # (B, 1)
                if self.use_bce:
                    mixed_targets = (targets_p * attn_A + targets_n * attn_B).clamp(0, 1)
                else:
                    mixed_targets = (targets_p * attn_A + targets_n * attn_B) / (attn_A + attn_B)
            else:
                mixed_targets, targets_p, targets_n = mixup_target(targets, self.num_classes, lam, self.label_smoothing, imgs.device)

            if self.tmix_type == 2:
                info_tmix["encoder_features"] = info["encoder_features"]

            info_tmix["targets_p"] = targets_p
            info_tmix["targets_n"] = targets_n


            return mixed_imgs, mixed_targets, info_tmix

        else:
            lam = np.random.beta(self.mixup_alpha, self.mixup_alpha)
            if not lam == 1:
                lam = float(lam)
                x_flipped = imgs.flip(0).mul_(1. - lam)
                imgs.mul_(lam).add_(x_flipped)
            mixed_targets, targets_p, targets_n = mixup_target(targets, self.num_classes, lam, self.label_smoothing, imgs.device)  # tuple or tensor
            info_tmix["targets_p"] = targets_p
            info_tmix["targets_n"] = targets_n
            return imgs, mixed_targets, info_tmix