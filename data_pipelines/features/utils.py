# -*- coding: utf-8 -*-
# @Author: Muhammad Umair
# @Date:   2022-07-07 16:59:00
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-07-26 14:45:03


import torch


def z_norm(x):
    """Obtain the z norm"""
    m = x.mean(dim=-2)
    s = x.std(dim=-2)
    return (x - m) / s


def z_norm_non_zero(x):
    """Obtain the z norm of all non zero values"""
    fnorm = []
    for i in range(x.shape[-1]):
        tmp_f = x[..., i]
        nz = tmp_f != 0
        m = tmp_f[nz].mean()
        s = tmp_f[nz].std()
        tmp_f[nz] = (tmp_f[nz] - m) / s
        fnorm.append(tmp_f)
    return torch.stack(fnorm, dim=-1)
