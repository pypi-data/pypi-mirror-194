from playground.analysis.lib_import import *
from tqdm import tqdm
import torch.nn as nn
import pandas as pd
import numpy as np
import torch
import os

# Section A. Setting
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
view = [False, True, True, False, False] # [IMAGE, ROLL_ATTN, ROLL_GRAD, OTHER]
evaluation = [False] # Evaluation
save_path, save, p, device = '/hub_data/joonmyung/conference/playgrounds/results/', False, True, 'cuda'
column_dtypes = {'targets'    :np.int64, 'confidences':np.float64,
                 'pred1'      :np.int64, 'pred2'      :np.int64, 'pred3'      :np.int64, 'pred4'      :np.int64, 'pred5'      :np.int64,
                 'acc1': np.int64, 'acc2': np.int64, 'acc3': np.int64, 'acc4': np.int64, 'acc5': np.int64}


# Section B. Data
dataset_name, server = "imagenet", "148"
data_path, _ = data2path(server, dataset_name)
dataset = JDataset(data_path, dataset_name, device=device)
loader = dataset.getAllItems()

# Section C. Model Load
# model_number, model_name = 0, "vit_small_patch16_224"
model_number, model_name = 1, "deit_tiny_patch16_224"
modelMaker = JModel(model_name, dataset.num_classes, model_number=model_number, device=device, p=p)
model, args = modelMaker.getModel()

criterion = nn.CrossEntropyLoss(reduction='none').cuda()
outputs, targets, losses, cls_attns, attns, attns_var, attns_dist, attns_sim, qkvs_dist, qkvs_sim = [], [], [], [], [], [], [], [], [], []

for batch_idx, (input, target) in enumerate(tqdm(loader)):
    input.requires_grad = True
    model(input)
    output = model(input)

    loss = criterion(output, target)


    outputs.append(output.detach().cpu())
    targets.append(target.detach().cpu())
    losses.append(loss.detach().cpu())

    cls_attns.append(to_np(torch.stack(attn)[:,:,:,0,1:]))
    attns.append(to_np(torch.stack(attn)))

    attns_var.append(torch.stack(attn_var))
    attns_dist.append(torch.stack(attn_dist))
    attns_sim.append(torch.stack(attn_sim))
    qkvs_dist.append(torch.stack(qkv_dist))
    qkvs_sim.append(torch.stack(qkv_sim))

    acc1, acc5 = accuracy(output.detach(), target, topk=(1, 5))
    top1.update(acc1.item(), input.size(0))
    top5.update(acc5.item(), input.size(0))

    if batch_idx == 3:
        break


del model
torch.cuda.empty_cache()

if analysis[0]:
    outputs, targets, losses, attns_var, attns_dist, attns_sim, qkvs_dist, qkvs_sim = torch.cat(outputs), torch.cat(targets), torch.cat(losses), torch.cat(attns_var, dim=1), torch.cat(attns_dist, dim=1), torch.cat(attns_sim, dim=1), torch.cat(qkvs_dist, dim=2), torch.cat(qkvs_sim, dim=2)
    acc1, acc5 = accuracy(outputs.detach(), targets, topk=(1, 5))
    print("top1 : {}, top5 : {}, acc1 : {}, acc5 : {}".format(top1.avg, top5.avg, acc1, acc5))



    # B. Collect Values
    #### B.1 Confidence
    m = nn.Softmax(dim=1)
    confidences = torch.gather(m(outputs), dim=1, index=targets.unsqueeze(1)).reshape(1,-1)

    #### B.2 Get Target, Pred1,2,3,...
    ks = 5
    corrects, preds = analysis(outputs.detach(), targets, topk=(1, ks))

    #### B.3 QKV Distance & Similarity
    q_dist, k_dist, v_dist = qkvs_dist.mean(dim=[3,4]).unbind(1) # (3(QKV), 12(L), (B))
    q_sim,  k_sim,  v_sim  =  qkvs_sim.mean(dim=[3,4]).unbind(1) # (3(QKV), 12(L), (B))
    L, B = q_dist.shape
    ds_c = ["{}_{}_{}".format(p, t, str(l).zfill(2)) for t in ['dist', 'sim'] for p in ['q', 'k', 'v'] for l in range(L)]
    ds_d = [q_dist, k_dist, v_dist, q_sim,  k_sim,  v_sim]

    #### B.4 Attention Distance & Similarity
    attn_dist = attns_dist.mean(dim=2)
    attn_sim = attns_sim.mean(dim=2)
    attn_var = attns_var.mean(dim=2)

    attn_c = ["attn_{}_{}".format(t, str(l).zfill(2)) for t in ['dist', 'sim', 'var'] for l in range(L)]
    attn_d = torch.cat([attn_dist, attn_sim, attn_var], dim=0)




    # C.1 Create Dataframe
    column_names  = ['targets', 'confidences', 'pred1', 'pred2', 'pred3', 'pred4', 'pred5'] + ds_c + attn_c
    data = to_np(torch.cat([targets.unsqueeze(0), confidences, preds] + ds_d + [attn_d], dim=0)).transpose()
    df = pd.DataFrame(data, columns=column_names, dtype=float)
    df = set_dtype(df, column_dtypes)
    df["label"] = df.apply(lambda x : get_label(x['targets'], imnet_label), axis=1)
    df = df[['label'] + column_names]
    # df.head()


    # C.2 Create Dataframe per class
    corrects_accum = torch.stack([corrects[:k+1].sum(dim=0) * 100 for k in range(ks)])
    column_names  = ['targets', 'confidences', 'correct1', 'correct2', 'correct3', 'correct4', 'correct5'] + ds_c + attn_c
    data = to_np(torch.cat([targets.unsqueeze(0), confidences, corrects_accum] + ds_d + [attn_d], dim=0)).transpose()
    data = data.reshape(-1, 50, len(column_names)).mean(axis=1)
    df_class = pd.DataFrame(data, columns=column_names)
    df_class = set_dtype(df_class, column_dtypes)
    df_class["label"] = df_class.apply(lambda x : get_label(x['targets'], imnet_label), axis=1)
    df_class = df_class[['label'] + column_names]
    df_class.sort_values(by=['correct1'])


    # C.3 Create Dataframe per Layer
    column_names = ["{}_{}".format(p, t) for t in ['dist', 'sim'] for p in ['q', 'k', 'v']] + \
                        ["attn_{}".format(t) for t in ['dist', 'sim', 'var']]
    data = to_np(torch.cat(ds_d + [attn_d])).mean(axis=1).reshape(-1, L).transpose()
    df_layer = pd.DataFrame(data, columns=column_names)
    df_layer


    print(1)
    attns = np.concatenate(attns, axis=1) # (12(L), 50000(S), 6(H), 196)
    L, B, H, T_q, T_k = attns.shape
    A = attns[:,:,:,:1,:1] # (12, 4400, 6,   1,   1)
    B = attns[:,:,:,:1,1:] # (12, 4400, 6,   1, 196)
    C = attns[:,:,:,1:,:1] # (12, 4400, 6, 196,   1)
    D = attns[:,:,:,1:,1:] # (12, 4400, 6, 196, 196)
    # np.expand_dims(np.eye(196), axis=(0,1,2))

    cls_ratio = np.stack((A.mean(axis=(1,2,3)).sum(axis=(1)), B.mean(axis=(1,2,3)).sum(axis=(1))), axis=0)
    patch_ratio = np.stack((C.sum(axis=4).mean(axis=(1,2,3)), D.sum(axis=4).mean(axis=(1,2,3))), axis=0)

    cls_attns = np.concatenate(cls_attns, axis=1) # (12(L), 50000(S), 6(H), 196)
    L, B, H, T = cls_attns.shape
    H_T, W_T = int(T ** 0.5), int(T ** 0.5)
    cls_attns = cls_attns.reshape(L, B, H, H_T, W_T)

    np.stack((C.sum(axis=4).mean(axis=(1, 2, 3)), D.sum(axis=4).mean(axis=(1, 2, 3))), axis=0)

if analysis[1]:
    pass



