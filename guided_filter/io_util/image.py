# -*- coding: utf-8 -*-
## @package guided_filter.io_util.image
#
#  Image IO utility package.
#  @author      tody
#  @date        2015/07/18

import cv2
from guided_filter.cv.image import *


def loadGray(file_path):
    bgr = cv2.imread(file_path)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    return gray


def loadRGB(file_path):
    bgr = cv2.imread(file_path)
    if bgr is None:
        return None
    return bgr2rgb(bgr)


def loadRGBA(file_path):
    bgra = cv2.imread(file_path, -1)
    if bgra is None:
        return None
    return bgra2rgba(bgra)


def loadAlpha(file_path):
    bgra = cv2.imread(file_path, -1)
    return alpha(bgra)


def saveRGBA(file_path, img):
    bgra = rgba2bgra(img)
    cv2.imwrite(file_path, bgra)


def saveRGB(file_path, img):
    bgr = rgb2bgr(img)
    cv2.imwrite(file_path, bgr)


def saveGray(file_path, img):
    rgbImg = rgb(img)
    cv2.imwrite(file_path, rgbImg)


def saveImage(file_path, img):
    img_8U = to8U(img)

    if len(img_8U.shape) == 2:
        saveGray(file_path, img_8U)
        return

    if img_8U.shape[2] == 3:
        saveRGB(file_path, img_8U)
        return

    if img_8U.shape[2] == 4:
        saveRGBA(file_path, img_8U)
        return

