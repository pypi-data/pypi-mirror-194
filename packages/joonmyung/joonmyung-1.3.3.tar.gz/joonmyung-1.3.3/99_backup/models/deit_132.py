# Copyright (c) 2015-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the CC-by-NC license found in the
# LICENSE file in the root directory of this source tree.
#

'''These modules are adapted from those of timm, see
https://github.com/rwightman/pytorch-image-models/blob/master/timm/models/vision_transformer.py
'''

from timm.models.layers import DropPath, to_2tuple, trunc_normal_
from einops import rearrange

import torch
import torch.nn as nn

from .SA.UNSA import UNSA
from .SA.MHSA import MHSA
import numpy as np


class Mlp(nn.Module):
    def __init__(self, in_features, hidden_features=None, out_features=None, act_layer=nn.GELU, drop=0.):
        super().__init__()
        out_features = out_features or in_features
        hidden_features = hidden_features or in_features
        self.fc1 = nn.Linear(in_features, hidden_features)
        self.act = act_layer()
        self.fc2 = nn.Linear(hidden_features, out_features)
        self.drop = nn.Dropout(drop)
        self.apply(self._init_weights)

    def _init_weights(self, m):
        if isinstance(m, nn.Linear):
            trunc_normal_(m.weight, std=.02)
            if isinstance(m, nn.Linear) and m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.LayerNorm):
            nn.init.constant_(m.bias, 0)
            nn.init.constant_(m.weight, 1.0)

    def forward(self, x):
        x = self.fc1(x)
        x = self.act(x)
        x = self.drop(x)
        x = self.fc2(x)
        x = self.drop(x)
        return x


class Block(nn.Module):

    def __init__(self, dim, num_heads,  mlp_ratio=4., qkv_bias=False, qk_scale=None, drop=0., attn_drop=0.,
                 drop_path=0., act_layer=nn.GELU, norm_layer=nn.LayerNorm):
        super().__init__()
        self.norm1 = norm_layer(dim)
        self.attn = MHSA(dim, num_heads=num_heads, qkv_bias=qkv_bias, qk_scale=qk_scale, attn_drop=attn_drop, proj_drop=drop)

        self.drop_path = DropPath(drop_path) if drop_path > 0. else nn.Identity()
        self.norm2 = norm_layer(dim)
        mlp_hidden_dim = int(dim * mlp_ratio)
        self.mlp = Mlp(in_features=dim, hidden_features=mlp_hidden_dim, act_layer=act_layer, drop=drop)

    def forward(self, x):
        x = x + self.drop_path(self.attn(self.norm1(x))[0])
        x = x + self.drop_path(self.mlp(self.norm2(x)))
        return x

class Unmix_Block(nn.Module):
    # taken from https://github.com/rwightman/pytorch-image-models/blob/master/timm/models/vision_transformer.py
    # with slight modifications to add CA and LayerScale
    def __init__(self, dim, num_heads, mlp_ratio=4., qkv_bias=False, qk_scale=None, drop=0., attn_drop=0.,
                 drop_path=0., act_layer=nn.GELU, norm_layer=nn.LayerNorm,
                 init_values=1e-4):
        super().__init__()
        self.norm1 = norm_layer(dim)
        self.attn = UNSA(dim, num_heads=num_heads, qkv_bias=qkv_bias, qk_scale=qk_scale, attn_drop=attn_drop, proj_drop=drop)
        self.drop_path = DropPath(drop_path) if drop_path > 0. else nn.Identity()
        self.norm2 = norm_layer(dim)
        mlp_hidden_dim = int(dim * mlp_ratio)
        self.mlp = Mlp(in_features=dim, hidden_features=mlp_hidden_dim, act_layer=act_layer, drop=drop)
        self.gamma_1 = nn.Parameter(init_values * torch.ones((dim)), requires_grad=True)
        self.gamma_2 = nn.Parameter(init_values * torch.ones((dim)), requires_grad=True)

    def forward(self, x, cls_token):
        cls_token_ = cls_token
        cls_token, attn = self.attn(self.norm1(torch.cat([x, cls_token], dim=1)), cls_token.shape[1])
        cls_token = cls_token_ + self.drop_path(self.gamma_1 * cls_token)
        cls_token = cls_token + self.drop_path(self.gamma_2 * self.mlp(self.norm2(cls_token)))
        return cls_token, attn

class PatchEmbed(nn.Module):
    """ Image to Patch Embedding, from timm
    """
    def __init__(self, input_size=224, patch_size=16, in_chans=3, embed_dim=768):
        super().__init__()
        input_size = to_2tuple(input_size)
        patch_size = to_2tuple(patch_size)
        num_patches = (input_size[1] // patch_size[1]) * (input_size[0] // patch_size[0])
        self.input_size = input_size
        self.patch_size = patch_size
        self.num_patches = num_patches

        self.proj = nn.Conv2d(in_chans, embed_dim, kernel_size=patch_size, stride=patch_size)
        self.apply(self._init_weights)
    def forward(self, x):
        B, C, H, W = x.shape
        assert H == self.input_size[0] and W == self.input_size[1], \
            f"Input image size ({H}*{W}) doesn't match model ({self.input_size[0]}*{self.input_size[1]})."
        x = self.proj(x).flatten(2).transpose(1, 2)
        return x
    def _init_weights(self, m):
        if isinstance(m, nn.Linear):
            trunc_normal_(m.weight, std=.02)
            if isinstance(m, nn.Linear) and m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.LayerNorm):
            nn.init.constant_(m.bias, 0)
            nn.init.constant_(m.weight, 1.0)


class HybridEmbed(nn.Module):
    """ CNN Feature Map Embedding, from timm
    """
    def __init__(self, backbone, input_size=224, feature_size=None, in_chans=3, embed_dim=768):
        super().__init__()
        assert isinstance(backbone, nn.Module)
        input_size = to_2tuple(input_size)
        self.input_size = input_size
        self.backbone = backbone
        if feature_size is None:
            with torch.no_grad():
                training = backbone.training
                if training:
                    backbone.eval()
                o = self.backbone(torch.zeros(1, in_chans, input_size[0], input_size[1]))[-1]
                feature_size = o.shape[-2:]
                feature_dim = o.shape[1]
                backbone.train(training)
        else:
            feature_size = to_2tuple(feature_size)
            feature_dim = self.backbone.feature_info.channels()[-1]
        self.num_patches = feature_size[0] * feature_size[1]
        self.proj = nn.Linear(feature_dim, embed_dim)
        self.apply(self._init_weights)

    def forward(self, x):
        x = self.backbone(x)[-1]
        x = x.flatten(2).transpose(1, 2)
        x = self.proj(x)
        return x


class VisionTransformer(nn.Module):
    """ Vision Transformer with support for patch or hybrid CNN input stage
    """
    def __init__(self, input_size=224, patch_size=16, in_chans=3, num_classes=1000, embed_dim=48, depth=12,
                 num_heads=12, mlp_ratio=4., qkv_bias=False, qk_scale=None, drop_rate=0., attn_drop_rate=0.,
                 drop_path_rate=0., hybrid_backbone=None, norm_layer=nn.LayerNorm, use_pos_embed=True,
                 **kwargs):
        super().__init__()
        self.cls_token_YN  = kwargs["cls_token_YN"]
        self.cls_token_num = kwargs["cls_token_num"]
        self.mae_mask_type = kwargs["mae_mask_type"]
        self.info = {}
        self.analysis = True

        self.num_classes = num_classes
        self.num_features = self.embed_dim = embed_dim  # num_features for consistency with other models
        self.use_pos_embed = use_pos_embed


        if hybrid_backbone is not None:
            self.patch_embed = HybridEmbed(
                hybrid_backbone, input_size=input_size, in_chans=in_chans, embed_dim=embed_dim)
        else:
            self.patch_embed = PatchEmbed(
                input_size=input_size, patch_size=patch_size, in_chans=in_chans, embed_dim=embed_dim)
        num_patches = self.patch_embed.num_patches
        self.num_patches = num_patches
        self.HW = int(num_patches**.5)

        # self.pos_drop = nn.Dropout(p=drop_rate)

        if self.use_pos_embed:
            self.pos_embed = nn.Parameter(torch.zeros(1, num_patches, embed_dim))
            trunc_normal_(self.pos_embed, std=.02)

        dpr = [x.item() for x in torch.linspace(0, drop_path_rate, depth)]  # stochastic depth decay rule
        self.blocks = nn.ModuleList([
            Block(
                dim=embed_dim, num_heads=num_heads, mlp_ratio=mlp_ratio, qkv_bias=qkv_bias, qk_scale=qk_scale,
                drop=drop_rate, attn_drop=attn_drop_rate, drop_path=dpr[i], norm_layer=norm_layer
                )
            for i in range(depth)])
        self.norm = norm_layer(embed_dim)

        # Classifier head
        self.feature_info = [dict(num_chs=embed_dim, reduction=0, module='head')]
        self.head = nn.Linear(embed_dim, num_classes) if num_classes > 0 else nn.Identity()


        if self.cls_token_YN:
            self.cls_token = nn.Parameter(torch.zeros(1, self.cls_token_num * 2, embed_dim))
            trunc_normal_(self.cls_token, std=.02)

        # OURS
        unmix_depth = kwargs["unmix_depth"]  # [512, 4, 1]
        self.unmix_blocks = nn.ModuleList([
            Unmix_Block(
                dim=embed_dim, num_heads=num_heads, mlp_ratio=mlp_ratio, qkv_bias=qkv_bias, qk_scale=qk_scale,
                drop=0.0, attn_drop=0.0, drop_path=0.0, norm_layer=norm_layer, )
            for _ in range(unmix_depth)])

        # MAE Decoder Specifics
        decoder_embed_dim, decoder_num_heads, decoder_depth = kwargs["decoder_param"]  #  [512, 4, 1]


        self.mask_token = nn.Parameter(torch.zeros(1, 1, decoder_embed_dim))
        self.decoder_embed = nn.Linear(embed_dim, decoder_embed_dim, bias=True)
        self.decoder_pos_embed = nn.Parameter(torch.zeros(1, self.patch_embed.num_patches + self.cls_token_num, decoder_embed_dim), requires_grad=False) if self.cls_token_YN \
                            else nn.Parameter(torch.zeros(1, self.patch_embed.num_patches, decoder_embed_dim), requires_grad=False)

        self.decoder_blocks = nn.ModuleList([
            Block(decoder_embed_dim, decoder_num_heads, mlp_ratio, qkv_bias=True, norm_layer=norm_layer)
            for _ in range(decoder_depth)])
        self.decoder_norm = norm_layer(decoder_embed_dim)
        self.decoder_pred = nn.Linear(decoder_embed_dim, patch_size ** 2 * 3, bias=True)  # decoder to patch

        self.mixed_ratio_type = kwargs["mixed_ratio_type"]
        self.norm_pix_loss = kwargs["norm_pix_loss"]
        self.mae_loss_type = kwargs["mae_loss_type"]

        self.initialize_weights()

    def initialize_weights(self):
        decoder_pos_embed = self.get_2d_sincos_pos_embed(self.decoder_pos_embed.shape[-1], self.HW, cls_token=True)
        self.decoder_pos_embed.data.copy_(torch.from_numpy(decoder_pos_embed).float().unsqueeze(0))

        # timm's trunc_normal_(std=.02) is effectively normal_(std=0.02) as cutoff is too big (2.)
        torch.nn.init.normal_(self.cls_token, std=.02)
        torch.nn.init.normal_(self.mask_token, std=.02)

        # initialize nn.Linear and nn.LayerNorm
        self.apply(self._init_weights)

    def _init_weights(self, m):
        if isinstance(m, nn.Linear):
            trunc_normal_(m.weight, std=.02)
            if isinstance(m, nn.Linear) and m.bias is not None:
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.LayerNorm):
            nn.init.constant_(m.bias, 0)
            nn.init.constant_(m.weight, 1.0)

    @torch.jit.ignore
    def no_weight_decay(self):
        return {'pos_embed', 'cls_token', 'selective_token'}

    def get_classifier(self):
        return self.head

    def reset_classifier(self, num_classes, global_pool=''):
        self.num_classes = num_classes
        self.head = nn.Linear(self.embed_dim, num_classes) if num_classes > 0 else nn.Identity()

    def patchify(self, imgs):
        """
        imgs: (N, 3, H, W)
        x: (N, L, patch_size**2 *3)
        """
        p = self.patch_embed.patch_size[0]
        assert imgs.shape[2] == imgs.shape[3] and imgs.shape[2] % p == 0

        h = w = imgs.shape[2] // p
        x = imgs.reshape(shape=(imgs.shape[0], 3, h, p, w, p))
        x = torch.einsum('nchpwq->nhwpqc', x)
        x = x.reshape(shape=(imgs.shape[0], h * w, p ** 2 * 3))
        return x

    def unpatchify(self, x):
        """
        x: (N, L, patch_size**2 *3)
        imgs: (N, 3, H, W)
        """
        p = self.patch_embed.patch_size[0]
        h = w = int(x.shape[1] ** .5)
        assert h * w == x.shape[1]

        x = x.reshape(shape=(x.shape[0], h, w, p, p, 3))
        x = torch.einsum('nhwpqc->nchpwq', x)
        imgs = x.reshape(shape=(x.shape[0], 3, h * p, h * p))
        return imgs


    def forward_encoder(self, imgs, mask=None):
        x, mixed_imgs, indices, lam = imgs, None, None, 1.0
        x = self.patch_embed(x)
        if self.use_pos_embed:
            x = x + self.pos_embed
        # x = self.pos_drop(x)

        if self.training or self.analysis:
            x, mask, indices, lam = self.masking(x, mask)
            mixed_imgs = self.unpatchify(mask * self.patchify(imgs) + (1 - mask) * self.patchify(imgs)[indices])

        for b, blk in enumerate(self.blocks):
            x = blk(x)
        x = self.norm(x)
        self.info["mixed_imgs"] = mixed_imgs
        self.info["mask"] = mask
        self.info["indices"] = indices
        self.info["lam"] = lam
        return x, mask, indices, lam

    def forward_unmixup(self, x):
        attns, cls_token = [], self.cls_token.expand(x.shape[0], -1, -1)
        for b, blk in enumerate(self.unmix_blocks):
            cls_token, attn = blk(x, cls_token)
            attns.append(attn) # L * (128(B), 3(H), 2(T_C), 196(D))

        if self.mae_mask_type == 0:
            attn = attns[-1].sum(dim=1) # (128(B) 2(T_C), 196(D))
        elif self.mae_mask_type == 1:
            attn = rollout(attns, 0.1, "mean", start=0, pool_seq=True)
        else:
            raise ValueError
        attn_a, attn_b = attn[:, :self.cls_token_num].sum(dim=1), attn[:, self.cls_token_num:].sum(dim=1) # (128(B), 196(T))
        mask_a = ((attn_a - attn_b) > 0).unsqueeze(-1).int()


        return cls_token, mask_a, torch.stack([attn_a, attn_b], dim=1)
               # attn_a.reshape(-1, self.HW, self.HW), attn_b.reshape(-1, self.HW, self.HW)


    def forward_decoder(self, x, cls_token, mask_a):
        # B, T, D =
        x = self.decoder_embed(torch.cat([cls_token, x], dim =1))  # (128(B), 2(T_C) + 196(T), 512(D))
        cls_token_a, cls_token_b, x = x[:, :self.cls_token_num], x[:, self.cls_token_num:self.cls_token_num * 2], x[:, self.cls_token_num * 2:]
        mask_tokens = self.mask_token.expand(x.shape[0], x.shape[1], -1)

        x = torch.cat([mask_a * x + (1 - mask_a) * mask_tokens, (1 - mask_a) * x + mask_a * mask_tokens])
        cls_token = torch.cat([cls_token_a, cls_token_b], dim=0) # (128 * 2(B), 1(T_C), 512(D))
        x = torch.cat([cls_token, x], dim=1) # # (128(B) * 2, 1(T_C) + 196(T), 512(D))
        x = x + self.decoder_pos_embed
        for blk in self.decoder_blocks:
            x = blk(x)
        x = self.decoder_norm(x)

        # predictor projection
        x = self.decoder_pred(x) # (200(B*2), 16(T), 512(D))
        if self.cls_token_YN:
            x = x[:, self.cls_token_num:]
        return x # (200(B * 2), 16(T), 192(D))

    def forward_loss(self, imgs, pred, mask_pred_a, mask_1, attn, cls_token, indices):

        target = self.patchify(imgs) # (128, 196, 768)
        B, T, D = target.shape
        if self.norm_pix_loss:
            mean = target.mean(dim=-1, keepdim=True)
            var = target.var(dim=-1, keepdim=True)
            target = (target - mean) / (var + 1.e-6)**.5

        pred = pred.reshape(2, -1, T, D).transpose(0,1) # (128(B), 2, 196(T), 768(D))
        ab_match = ((1 - mask_1 ^ mask_pred_a).sum(dim=[1, 2]) > (self.num_patches // 2)).type(torch.int64).reshape(-1, 1, 1) # (128, 1, 1)
        cls_token_1, cls_token_2 = torch.gather(cls_token, 1,     ab_match.repeat(1, 1, cls_token.shape[2])), \
                                   torch.gather(cls_token, 1, 1 - ab_match.repeat(1, 1, cls_token.shape[2]))
        pred_1, pred_2           = torch.gather(pred, 1,     ab_match.unsqueeze(-1).repeat(1, 1, T, D)).squeeze(), \
                                   torch.gather(pred, 1, 1 - ab_match.unsqueeze(-1).repeat(1, 1, T, D)).squeeze()
        mask_pred_1              = torch.gather(torch.stack([mask_pred_a, 1 - mask_pred_a], dim=1), 1, ab_match.unsqueeze(-1).repeat(1, 1, T, 1)).squeeze(1) # ERROR FIX
        attn_1, attn_2           = torch.gather(attn, 1,     ab_match.repeat(1, 1, attn.shape[2])).squeeze(), \
                                   torch.gather(attn, 1, 1 - ab_match.repeat(1, 1, attn.shape[2])).squeeze()
        mask_acc = ((1 - mask_1 ^ mask_pred_1).sum(dim=[1, 2]) / self.num_patches).mean() # ERROR FIX
        loss_mae = ((attn_1 - mask_1.squeeze(-1)) ** 2).mean() + ((attn_2 - (1-mask_1).squeeze(-1)) ** 2).mean()



        if self.mae_loss_type == 0:
            loss_mae_1 = (((pred_1 - target) ** 2) * (1 - mask_pred_1)).mean(dim=(2)).sum() / (1 - mask_pred_1).sum()
            loss_mae_2 = (((pred_2 - target[indices]) ** 2) * (mask_pred_1)).mean(dim=(2)).sum() / mask_pred_1.sum()
        elif self.mae_loss_type == 1:
            loss_mae_1 = ((pred_1 - target) ** 2).mean()
            loss_mae_2 = ((pred_2 - target[indices]) ** 2).mean()
        else:
            raise ValueError

        self.info["mae_target"] = self.unpatchify(target)
        self.info["mae_pred_1"] = self.unpatchify(pred_1 * (1 - mask_pred_1) + target * mask_pred_1)
        self.info["mae_pred_2"] = self.unpatchify(pred_2 * mask_pred_1 + target[indices] * (1 - mask_pred_1))
        self.info["mae_pred_mask_1"] = self.unpatchify(pred_1 * (1 - mask_pred_1) + mask_pred_1)
        self.info["mae_pred_mask_2"] = self.unpatchify(pred_2 * mask_pred_1 + (1 - mask_pred_1))
        self.info["mae_target_mask_1"] = self.unpatchify(target * mask_pred_1 + (1 - mask_pred_1))
        self.info["mae_target_mask_2"] = self.unpatchify(target.flip(0) * (1 - mask_pred_1) + mask_pred_1)
        self.info["mask_acc"] = mask_acc
        self.info["mask_pred_1"] = mask_pred_1

        return torch.cat([cls_token_1, cls_token_2], dim=0), loss_mae, loss_mae_1, loss_mae_2

    def masking(self, x, mask=None): # (128, 196, 192)
        B, T, D = x.shape
        if self.mixed_ratio_type == 1:
            T_mixup_keep = int(T * ((0.75 - 0.25) * torch.rand(1) + 0.25))
        elif self.mixed_ratio_type == 2:
            T_mixup_keep = int(T * max(0.25, min(0.75, np.random.beta(1.0, 1.0))))
        else:
            T_mixup_keep = int(T * 0.5)
        # T_mixup_keep = (T * np.random.beta(self.mixed_ratio_type, self.mixed_ratio_type, size=1)).astype(int)
        mask = torch.zeros(B, T, device="cuda").scatter_(1, torch.topk(torch.randn(B, T, device="cuda"), T_mixup_keep, dim=1)[1], 1).unsqueeze(dim=-1).int() \
                    if mask is None else mask # (128(B), 196(T), 1(D))
        lam = T_mixup_keep / T

        indices = torch.randperm(B, device="cuda") if not self.analysis else torch.flip(torch.arange(B), dims=[0])
        x = mask * x + (1 - mask) * x[indices]
        return x, mask, indices, lam

    def forward(self, imgs, mask=None):
        x, mask, indices, lam = self.forward_encoder(imgs, mask)

        output = self.head(x.mean(dim=1))
        if not (self.training or self.analysis): return output

        cls_token, mask_a, attn = self.forward_unmixup(x)

        pred = self.forward_decoder(x, cls_token, mask_a)
        cls_token, loss_mask, loss_mae_1, loss_mae_2 = self.forward_loss(imgs, pred, mask_a, mask, attn, cls_token, indices)
        output_12 = self.head(cls_token)


        return output, output_12, loss_mask, loss_mae_1, loss_mae_2, self.info

    def get_2d_sincos_pos_embed(self, embed_dim, grid_size, cls_token=False):
        grid_h = np.arange(grid_size, dtype=np.float32)
        grid_w = np.arange(grid_size, dtype=np.float32)
        grid = np.meshgrid(grid_w, grid_h)  # here w goes first
        grid = np.stack(grid, axis=0)

        grid = grid.reshape([2, 1, grid_size, grid_size])
        pos_embed = self.get_2d_sincos_pos_embed_from_grid(embed_dim, grid)
        if cls_token:
            pos_embed = np.concatenate([np.zeros([1, embed_dim]), pos_embed], axis=0)
        return pos_embed

    def get_2d_sincos_pos_embed_from_grid(self, embed_dim, grid):
        assert embed_dim % 2 == 0

        # use half of dimensions to encode grid_h
        emb_h = self.get_1d_sincos_pos_embed_from_grid(embed_dim // 2, grid[0])  # (H*W, D/2)
        emb_w = self.get_1d_sincos_pos_embed_from_grid(embed_dim // 2, grid[1])  # (H*W, D/2)

        emb = np.concatenate([emb_h, emb_w], axis=1)  # (H*W, D)
        return emb

    def get_1d_sincos_pos_embed_from_grid(self, embed_dim, pos):
        """
        embed_dim: output dimension for each position
        pos: a list of positions to be encoded: size (M,)
        out: (M, D)
        """
        assert embed_dim % 2 == 0
        omega = np.arange(embed_dim // 2, dtype=np.float)
        omega /= embed_dim / 2.
        omega = 1. / 10000 ** omega  # (D/2,)

        pos = pos.reshape(-1)  # (M,)
        out = np.einsum('m,d->md', pos, omega)  # (M, D/2), outer product

        emb_sin = np.sin(out)  # (M, D/2)
        emb_cos = np.cos(out)  # (M, D/2)

        emb = np.concatenate([emb_sin, emb_cos], axis=1)  # (M, D)
        return emb

    def interpolate_pos_embed(self, model, checkpoint_model):
        if 'pos_embed' in checkpoint_model:
            pos_embed_checkpoint = checkpoint_model['pos_embed']
            embedding_size = pos_embed_checkpoint.shape[-1]
            num_patches = model.patch_embed.num_patches
            num_extra_tokens = model.pos_embed.shape[-2] - num_patches
            # height (== width) for the checkpoint position embedding
            orig_size = int((pos_embed_checkpoint.shape[-2] - num_extra_tokens) ** 0.5)
            # height (== width) for the new position embedding
            new_size = int(num_patches ** 0.5)
            # class_token and dist_token are kept unchanged
            if orig_size != new_size:
                print("Position interpolate from %dx%d to %dx%d" % (orig_size, orig_size, new_size, new_size))
                extra_tokens = pos_embed_checkpoint[:, :num_extra_tokens]
                # only the position tokens are interpolated
                pos_tokens = pos_embed_checkpoint[:, num_extra_tokens:]
                pos_tokens = pos_tokens.reshape(-1, orig_size, orig_size, embedding_size).permute(0, 3, 1, 2)
                pos_tokens = torch.nn.functional.interpolate(
                    pos_tokens, size=(new_size, new_size), mode='bicubic', align_corners=False)
                pos_tokens = pos_tokens.permute(0, 2, 3, 1).flatten(1, 2)
                new_pos_embed = torch.cat((extra_tokens, pos_tokens), dim=1)
                checkpoint_model['pos_embed'] = new_pos_embed