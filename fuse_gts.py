# -*- coding:utf-8 -*-

import time
from tqdm import tqdm
import glob
import os
import cv2
import numpy as np


def fg_mask(dm):
    sz = dm.shape[:2]
    gray = cv2.cvtColor(dm, cv2.COLOR_BGR2GRAY)
    mask = 255 - cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,
                                       35 if min(sz) > 35 else int(min(sz) / 2) + 1, 7)
    canny = cv2.Canny(gray, 50, 100)
    mask = cv2.add(mask, canny)
    if np.sum(mask, dtype=np.float32) / 255 / (mask.shape[0] * mask.shape[1]) > 0.5:
        mask = 255 - mask
    # mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    # mask = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    # mask = cv2.GaussianBlur(mask, (3, 3), 0)
    mask = mask.astype(np.float32) / 255.0
    mask = cv2.merge([mask, mask, mask])
    return mask


def multiband(A, n):
    G = A.copy()
    gpA = [G]
    for i in range(n - 1):
        G = cv2.pyrDown(G)
        gpA.append(G)

    lpA = [gpA[n - 1].astype(np.float32)]
    for i in range(n - 1, 0, -1):
        GE = cv2.pyrUp(gpA[i])
        L = cv2.subtract(gpA[i - 1].astype(np.float32), GE.astype(np.float32))
        lpA.append(L)

    return lpA


def buildFromBands(lpA):
    ls_ = lpA[0]
    for i in range(1, len(lpA)):
        ls_ = cv2.pyrUp(ls_)
        ls_ = cv2.add(ls_, lpA[i])

    return np.clip(ls_, 0, 255).astype(np.uint8)


paths = "D:/data/doc_filter/table/*"
paths_gt = [
    "D:/data/doc_filter_offline/table",
    "D:/data/doc_filter_online/table"
]
path_out = "D:/data/doc_filter_out/table"

images = glob.glob(paths)
for fi, f in enumerate(images):
    im = cv2.imread(f)
    denoise = cv2.bilateralFilter(im, 7, 18, 35, borderType=cv2.BORDER_REFLECT_101)

    name = os.path.basename(f)
    gts = [cv2.imread(os.path.join(p, name)) for p in paths_gt]

    # bg是取最白的部分
    bg = np.maximum(gts[0], gts[1])
    # mask是文字的前景
    mask = fg_mask(denoise)

    e0 = cv2.Laplacian(gts[0], cv2.CV_32F)
    e1 = cv2.Laplacian(gts[1], cv2.CV_32F)
    mag0 = np.abs(e0) + 1e-8
    mag1 = np.abs(e1) + 1e-8
    sharpest = gts[0]
    sharp_msk = mag0 < mag1
    sharpest[sharp_msk] = gts[1][sharp_msk]

    bands_n = 3
    sz_choise = np.array([2 ** bands_n * j for j in range(2, int(4096 / (2 ** bands_n)))])
    idx0 = np.where(sz_choise >= im.shape[0])[0]
    idx1 = np.where(sz_choise >= im.shape[1])[0]
    if len(idx0) > 0:
        sz0 = sz_choise[min(idx0)]
    else:
        sz0 = sz_choise[-1]
    if len(idx1) > 0:
        sz1 = sz_choise[min(idx1)]
    else:
        sz1 = sz_choise[-1]
    # 求multiband
    ibands = multiband(cv2.resize(bg, (sz1, sz0), interpolation=cv2.INTER_CUBIC), bands_n)
    sbands = multiband(cv2.resize(sharpest, (sz1, sz0), interpolation=cv2.INTER_CUBIC), bands_n)
    high_freq = cv2.resize(mask, (sz1, sz0)) > 0
    ibands[-1][high_freq] = sbands[-1][high_freq]
    result = buildFromBands(ibands)

    cv2.namedWindow("sharpest", cv2.WINDOW_NORMAL)
    cv2.imshow("sharpest", sharpest)
    cv2.namedWindow("result", cv2.WINDOW_NORMAL)
    cv2.imshow("result", result)
    cv2.namedWindow("denoise", cv2.WINDOW_NORMAL)
    cv2.imshow("denoise", denoise)
    cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
    cv2.imshow("mask", mask)
    cv2.namedWindow("bg", cv2.WINDOW_NORMAL)
    cv2.imshow("bg", bg)
    for i, gt in enumerate(gts):
        cv2.namedWindow(str(i), cv2.WINDOW_NORMAL)
        cv2.imshow(str(i), gt)
    cv2.waitKey()
