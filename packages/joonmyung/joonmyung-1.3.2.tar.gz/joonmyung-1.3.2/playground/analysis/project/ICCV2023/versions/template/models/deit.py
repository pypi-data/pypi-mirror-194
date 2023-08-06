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
import torch
import torch.nn as nn

from .SA.DESA import DESA
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


class Decoder_Block(nn.Module):
    def __init__(self, dim, num_heads,  mlp_ratio=4., qkv_bias=False, qk_scale=None, drop=0., attn_drop=0.,
                 drop_path=0., act_layer=nn.GELU, norm_layer=nn.LayerNorm):
        super().__init__()
        self.norm1 = norm_layer(dim)
        self.attn = DESA(dim, num_heads=num_heads, qkv_bias=qkv_bias, qk_scale=qk_scale, attn_drop=attn_drop, proj_drop=drop)

        self.drop_path = DropPath(drop_path) if drop_path > 0. else nn.Identity()
        self.norm2 = norm_layer(dim)
        mlp_hidden_dim = int(dim * mlp_ratio)
        self.mlp = Mlp(in_features=dim, hidden_features=mlp_hidden_dim, act_layer=act_layer, drop=drop)

    def forward(self, x, mask_token):
        T = x.shape[1]
        mask_token_ = mask_token
        mask_token, attn = self.attn(self.norm1(torch.cat([x, mask_token], dim=1)), token_num=T)
        mask_token = mask_token_ + self.drop_path(mask_token)
        mask_token = mask_token + self.drop_path(self.mlp(self.norm2(mask_token)))
        return mask_token, attn

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
        x_ = x
        x, attn = self.attn(self.norm1(x))
        x = x_ + self.drop_path(x)
        x = x + self.drop_path(self.mlp(self.norm2(x)))
        return x, attn

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
                 num_heads=12, mlp_ratio=4., qkv_bias=True, qk_scale=None, drop_rate=0., attn_drop_rate=0.,
                 drop_path_rate=0., hybrid_backbone=None, norm_layer=nn.LayerNorm, use_pos_embed=True,
                 **kwargs):
        super().__init__()
        self.norm_pix_loss = kwargs["norm_pix_loss"]
        self.cls_token_num = kwargs["cls_token_num"]
        self.mae_task_type = kwargs["mae_task_type"]
        self.tmix_type     = kwargs["tmix_type"]

        self.unmix_token_num   = kwargs["mae_task_type"][2]
        self.mae_avg_type      = kwargs["mae_task_type"][4]
        self.decoder_token_num = kwargs["mae_task_type"][6]
        self.mae_avg_token_num = 1 if self.mae_avg_type else 0
        self.info = {}


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

        self.pos_drop = nn.Dropout(p=drop_rate)

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

        # CLS Token
        if self.cls_token_num:
            self.cls_token = nn.Parameter(torch.zeros(1, self.cls_token_num, embed_dim))
            trunc_normal_(self.cls_token, std=.02)



        # MAE Decoder Specifics
        if self.mae_task_type[1]:
            decoder_embed_dim, decoder_num_heads, decoder_depth = kwargs["decoder_param"]  # [512, 4, 1]
            # self.mask_token = nn.Parameter(torch.zeros(1, 1, decoder_embed_dim))
            # torch.nn.init.normal_(self.mask_token, std=.02)

            if self.decoder_token_num:
                self.decoder_token = nn.Parameter(torch.zeros(2, 1, self.decoder_token_num, decoder_embed_dim))
                trunc_normal_(self.decoder_token, std=.02)

            if self.unmix_token_num:
                self.unmix_token = nn.Parameter(torch.zeros(1, self.unmix_token_num * 2, embed_dim))
                trunc_normal_(self.unmix_token, std=.02)

            self.decoder_embed = nn.Linear(embed_dim, decoder_embed_dim, bias=True)
            self.decoder_pos_embed = nn.Parameter(torch.zeros(1, self.patch_embed.num_patches, decoder_embed_dim), requires_grad=False)

            self.decoder_blocks = nn.ModuleList([
                Block(decoder_embed_dim, decoder_num_heads, mlp_ratio, qkv_bias=True, norm_layer=norm_layer)
                for _ in range(decoder_depth)])
            self.decoder_norm = norm_layer(decoder_embed_dim)
            if self.tmix_type == 1:
                self.decoder_pred = nn.Linear(decoder_embed_dim, patch_size ** 2 * 3, bias=True)  # decoder to patch

            decoder_pos_embed = self.get_2d_sincos_pos_embed(self.decoder_pos_embed.shape[-1], self.HW)
            self.decoder_pos_embed.data.copy_(torch.from_numpy(decoder_pos_embed).float().unsqueeze(0))



        self.initialize_weights()

    def initialize_weights(self):

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
        return {'pos_embed', 'selective_token'}

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


    def forward_encoder(self, x, analysis=0):
        x = self.patch_embed(x)
        if self.use_pos_embed:
            x = x + self.pos_embed
        x = self.pos_drop(x)

        if self.unmix_token_num:
            unmix_tokens = self.unmix_token.expand(x.shape[0], -1, -1)
            x = torch.cat((unmix_tokens, x), dim=1)

        if self.cls_token_num:
            cls_tokens = self.cls_token.expand(x.shape[0], -1, -1)
            x = torch.cat((cls_tokens, x), dim=1)


        attns = []
        for b, blk in enumerate(self.blocks):
            x, attn = blk(x)
            attns.append(attn.detach())
        if analysis in [1, 2]: self.info["encoder_attn"] = attns
        x = self.norm(x)

        return x[:, :self.cls_token_num], \
               x[:, self.cls_token_num:self.cls_token_num + 2 * self.unmix_token_num],\
               x[:, self.cls_token_num + 2 * self.unmix_token_num:]


    def forward_decoder(self, x, cls_tokens, unmix_tokens, tmix_info):
        mask = tmix_info["mask"]
        mask_p = tmix_info["mask_p"]
        mask_n = tmix_info["mask_n"]
        x = torch.cat([cls_tokens, unmix_tokens, x], dim=1)
        x = self.decoder_embed(x) # (32, 196(T) + 2(T_C), 192)

        cls_tokens, unmix_tokens, x = x[:, : self.cls_token_num], \
                                    x[:, self.cls_token_num : self.cls_token_num + 2 * self.unmix_token_num],\
                                    x[:, self.cls_token_num + 2 * self.unmix_token_num : ]

        x = x + self.decoder_pos_embed  # (32(2B), 196(T), 192(D))
        B, T, D = x.shape


        if self.mae_avg_type:
            if self.mae_avg_type == 1:
                avg_tokens_1 = torch.gather(x, dim=1, index=mask_p[:,0].reshape(B,-1,1).expand(-1, -1, D)) # (32(B), 1, 192(D)
                avg_tokens_2 = torch.gather(x, dim=1, index=mask_n[:,0].reshape(B,-1,1).expand(-1, -1, D)) # (32(B), 1, 192(D)
            elif self.mae_avg_type == 2:
                avg_tokens_1 = (x * mask).mean(dim=1, keepdim=True)
                avg_tokens_2 = (x * (1 - mask)).mean(dim=1, keepdim=True)
            elif self.mae_avg_type == 3:
                T_C = int(mask_p.shape[1] / 4)
                avg_tokens_1 = torch.gather(x, dim=1, index=mask_p[:, :T_C].reshape(B,-1,1).expand(-1, -1, D)).mean(dim=1, keepdim=True)
                avg_tokens_2 = torch.gather(x, dim=1, index=mask_n[:, :T_C].reshape(B,-1,1).expand(-1, -1, D)).mean(dim=1, keepdim=True)
            else:
                raise ValueError
            avg_tokens = torch.cat([avg_tokens_1, avg_tokens_2], dim=0)  # (64(2B), 1(T_M), 192(D))
            x = torch.cat([avg_tokens, x.repeat(2, 1, 1)], dim=1) # (64(2B), 1(T_M) + 2(T_C) + 196(T), 192(D))
        else:
            x = x.repeat(2, 1, 1)  # (64(2B), 196(T), 192(D))

        if self.cls_token_num:
            x = torch.cat([cls_tokens.repeat(2, 1, 1), x], dim=1) # (64(2B), 2(T_C) + 196(T), 192(D))

        if self.unmix_token_num:
            unmix_tokens = unmix_tokens.reshape(B, 2, self.unmix_token_num, D).transpose(0, 1).reshape(-1, self.unmix_token_num, D)
            x = torch.cat([unmix_tokens, x], dim=1)  # (64(2B), 2(T_U) + 2(T_C) + 196(T), 192(D))

        if self.decoder_token_num:
            decoder_tokens = self.decoder_token.expand(-1, B, -1, -1).reshape(-1, self.decoder_token_num, D) # (64(2B), 2(T_D), 192(D))
            x = torch.cat([decoder_tokens, x], dim=1) # (64(2B), 2(T_D) + 1(T_M) + 2(T_C) + 196(T), 192(D))

        attns = []
        for blk in self.decoder_blocks:
            x, attn = blk(x)
            attns.append(attn)
        x = self.decoder_norm(x) # (64(2B), 2(T_D) + 1(T_M) + 2(T_C) + 196(T), 192(D))
        self.info["decoder_attn"] = attns

        avg_tokens     = x[:,                                                                    : self.mae_avg_token_num]
        cls_tokens     = x[:, self.mae_avg_token_num                                             : self.mae_avg_token_num + self.cls_token_num]
        unmix_tokens   = x[:, self.mae_avg_token_num + self.cls_token_num                        : self.mae_avg_token_num + self.cls_token_num + self.unmix_token_num]
        decoder_tokens = x[:, self.mae_avg_token_num + self.cls_token_num + self.unmix_token_num : -T]
        patch_tokens   = x[:, -T                                                                 : ]
        

        pred = self.decoder_pred(patch_tokens) if self.tmix_type == 1 else patch_tokens # (200(B*2), 16(T), 512(D))

        return avg_tokens, cls_tokens, unmix_tokens, decoder_tokens, pred

    def forward_mae_loss(self, mae_target, mae_pred, unmix_tokens):
        B = mae_target.shape[0]

        if self.tmix_type == 1:
            mae_target = self.patchify(mae_target) # (128, 196, 768)
            if self.norm_pix_loss:
                mean = mae_target.mean(dim=-1, keepdim=True)
                var = mae_target.var(dim=-1, keepdim=True)
                mae_target = (mae_target - mean) / (var + 1.e-6)**.5

        if self.mae_task_type[2]:
            _, T, D = mae_pred.shape
            pred_AB = mae_pred.reshape(2, -1, T, D)
            unmix_tokens_AB = unmix_tokens.reshape(2, B, self.unmix_token_num, -1)
            target_A1 = torch.stack([mae_target, mae_target.flip(0)], dim=0)
            target_A2 = torch.stack([mae_target.flip(0), mae_target], dim=0)
            loss_mae_A1 = ((pred_AB - target_A1) ** 2).mean(dim=[0, 2, 3])
            loss_mae_A2 = ((pred_AB - target_A2) ** 2).mean(dim=[0, 2, 3])
            A1 = (loss_mae_A1 < loss_mae_A2).int()    # 32
            AB_1 = torch.stack([A1, (1 - A1)], dim=0).reshape(2, -1, 1, 1) # (2, 32(B), 1, 1)
            pred_1 = (pred_AB * AB_1).sum(dim=0)       # (32(B), 196(T), 768(D_E))
            pred_2 = (pred_AB * (1 - AB_1)).sum(dim=0) # (32(B), 196(T), 768(D_E))
            mae_pred = torch.cat([pred_1, pred_2], dim=0)

            unmix_tokens_1 = (unmix_tokens_AB * AB_1).sum(dim=0)       # (32(B), 1, 192(D_D))
            unmix_tokens_2 = (unmix_tokens_AB * (1 - AB_1)).sum(dim=0) # (32(B), 1, 192(D_D))
            unmix_tokens = torch.cat([unmix_tokens_1, unmix_tokens_2], dim=0)

            loss_mae     = (loss_mae_A1 * A1 + loss_mae_A2 * (1 - A1)).mean()
        else:
            loss_mae = ((mae_pred[:B] - mae_target) ** 2).mean() + ((mae_pred[B:] - mae_target.flip(0)) ** 2).mean()


        if self.tmix_type == 1:
            self.info["mae_pred_1"] =  self.unpatchify(mae_pred[:B])
            self.info["mae_pred_2"] =  self.unpatchify(mae_pred[B:])
        # drawImgPlot(unNormalize(torch.stack([self.info["mae_pred_1"], self.info["mae_pred_2"]], dim=1).reshape(-1, 3, 224, 224)[:6].detach(), "imagenet"), col=2)

        return loss_mae, unmix_tokens, mae_pred


    def forward(self, x, imgs=None, tmix_info={}, analysis=0):
        result, self.info = {}, {}
        cls_token, unmix_token, x = self.forward_encoder(x, analysis)

        output_all = self.head(cls_token.mean(dim=1)) if self.cls_token_num else self.head(x.mean(dim=1))
        result["output_all"] = output_all

        if not self.training and not analysis: # Evaluation/
            return output_all

        if analysis in [1, 2]: # TMIX
            if analysis == 2:
                self.info["encoder_features"] = x.detach()
            return self.info

        if "mask" in tmix_info.keys():
            if self.mae_task_type[1]:
                avg_tokens, cls_tokens, unmix_tokens, decoder_tokens, pred = self.forward_decoder(x, cls_token, unmix_token, tmix_info)
                mae_target = imgs if self.tmix_type == 1 else tmix_info["encoder_features"]
                loss_mae, unmix_tokens, mae_pred = self.forward_mae_loss(mae_target, pred, unmix_tokens)

                result["loss_mae"] = loss_mae

                if self.mae_task_type[2] and self.mae_task_type[3]:
                    u_1, u_2 = unmix_tokens.mean(dim=1)[:x.shape[0]], unmix_tokens.mean(dim=1)[x.shape[0]:]
                    result["output_part_unmix"] = self.head(torch.cat([u_1, u_2], dim=0))

                if self.mae_task_type[4] and self.mae_task_type[5]:
                    m_1, m_2 = avg_tokens.mean(dim=1)[:x.shape[0]], avg_tokens.mean(dim=1)[x.shape[0]:]
                    result["output_part_avg"] = self.head(torch.cat([m_1, m_2], dim=0))

                if self.mae_task_type[6] and self.mae_task_type[7]:
                    d_1, d_2 = decoder_tokens.mean(dim=1)[:x.shape[0]], decoder_tokens.mean(dim=1)[x.shape[0]:]
                    result["output_part_decoder"] = self.head(torch.cat([d_1, d_2], dim=0))

                if self.mae_task_type[8] and self.tmix_type == 2:
                    result["output_part_recon"] = self.head(mae_pred.mean(dim=1))

            x_1, x_2 = (x * tmix_info["mask"]).mean(dim=1), (x * (1 - tmix_info["mask"])).mean(dim=1)
            if self.mae_task_type[9]:  # Part Classification Loss
                result["output_part"] = self.head(torch.cat([x_1, x_2], dim=0))

            if self.mae_task_type[10]:
                result["loss_part_consis"] = ((x_1 - x_2.flip(0)) ** 2).mean()


        return result, self.info



    def get_2d_sincos_pos_embed(self, embed_dim, grid_size):
        grid_h = np.arange(grid_size, dtype=np.float32)
        grid_w = np.arange(grid_size, dtype=np.float32)
        grid = np.meshgrid(grid_w, grid_h)  # here w goes first
        grid = np.stack(grid, axis=0)

        grid = grid.reshape([2, 1, grid_size, grid_size])
        pos_embed = self.get_2d_sincos_pos_embed_from_grid(embed_dim, grid)
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