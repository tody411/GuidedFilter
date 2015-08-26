# -*- coding: utf-8 -*-
## @package guided_filter.cv.image
#
#  OpenCV image functions.
#  @author      tody
#  @date        2015/07/30


import numpy as np
import cv2


## Convert image into uint8 type.
def to8U(img):
    if img.dtype == np.uint8:
        return img
    return np.clip(np.uint8(255.0 * img), 0, 255)


## Convert image into float32 type.
def to32F(img):
    if img.dtype == np.float32:
        return img
    return (1.0 / 255.0) * np.float32(img)


## RGB channels of the image.
def rgb(img):

    if len(img.shape) == 2:
        h, w = img.shape
        img_rgb = np.zeros((h, w, 3), dtype=img.dtype)
        for ci in range(3):
            img_rgb[:, :, ci] = img
        return img_rgb

    h, w, cs = img.shape
    if cs == 3:
        return img

    img_rgb = np.zeros((h, w, 3), dtype=img.dtype)

    cs = min(3, cs)

    for ci in range(cs):
        img_rgb[:, :, ci] = img[:, :, ci]
    return img_rgb


## Alpha channel of the image.
def alpha(img):
    if len(img.shape) == 2:
        return None

    cs = img.shape[2]
    if cs != 4:
        return None
    return img[:, :, 3]


## Set alpha for the image.
def setAlpha(img, a):
    h = img.shape[0]
    w = img.shape[1]

    img_rgb = None
    if len(img.shape) == 2:
        img_rgb = gray2rgb(img)
    else:
        img_rgb = img

    img_rgba = np.zeros((h, w, 4), dtype=img.dtype)
    img_rgba[:, :, :3] = img_rgb
    img_rgba[:, :, 3] = a
    return img_rgba


## RGB to Gray.
def rgb2gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    return gray


## Gray to RGB.
def gray2rgb(img):
    gray = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    return gray


## Gray to RGBA.
def gray2rgba(img):
    gray = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)
    return gray


## BGR to RGB.
def bgr2rgb(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return rgb


## BGRA to RGBA.
def bgra2rgba(img):
    a = alpha(img)
    rgba = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    if a is not None:
        rgba[:, :, 3] = a
    return rgba


## RGBA to BGRA.
def rgba2bgra(img):
    a = alpha(img)
    bgra = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
    bgra[:, :, 3] = a
    return bgra


## RGB to BGR.
def rgb2bgr(img):
    bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return bgr


## RGB to Lab.
def rgb2Lab(img):
    img_rgb = rgb(img)
    Lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)
    return Lab


## Lab to RGB.
def Lab2rgb(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_LAB2RGB)
    return rgb


def rgb2hsv(img):
    img_rgb = rgb(img)
    return cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)


## HSV to RGB.
def hsv2rgb(img):
    rgb = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    return rgb


## Merge channels.
def merge(channels):
    cs = 0
    h = 0
    w = 0
    for channel in channels:
        if len(channel.shape) == 2:
            cs += 1
        else:
            cs += channel.shape[2]

        h, w = channel.shape[0], channel.shape[1]

    img = np.zeros((h, w, cs))

    ci = 0
    for channel in channels:
        if len(channel.shape) == 2:
            img[:, :, ci] = channel[:, :]
            ci += 1
            continue

        for cci in range(channel.shape[2]):
            img[:, :, ci] = channel[:, :, cci]
            ci += 1

    return img


## Luminance value from Lab.
#  Lumiannce value will be in [0, 1]
def luminance(img):
    L = rgb2Lab(rgb(img))[:, :, 0]
    if L.dtype != np.uint8:
        return (1.0 / 100.0) * L
    return L
