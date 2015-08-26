
# -*- coding: utf-8 -*-
## @package guided_filter.core.filters
#
#  guided_filter.core.filters utility package.
#  @author      tody
#  @date        2015/08/26

import numpy as np
import cv2

from guided_filter.cv.image import to32F


## Return if the input image is gray or not.
def _isGray(I):
    return len(I.shape) == 2


## Return down sampled image.
#  @param scale (w/s, h/s) image will be created.
#  @param shape I.shape[:2]=(h, w). numpy friendly size parameter.
def _downSample(I, scale=4, shape=None):
    if shape is not None:
        h, w = shape
        return cv2.resize(I, (w, h), interpolation=cv2.INTER_NEAREST)

    h, w = I.shape[:2]
    return cv2.resize(I, (w / scale, h / scale), interpolation=cv2.INTER_NEAREST)


## Return up sampled image.
#  @param scale (w*s, h*s) image will be created.
#  @param shape I.shape[:2]=(h, w). numpy friendly size parameter.
def _upSample(I, scale=2, shape=None):
    if shape is not None:
        h, w = shape
        return cv2.resize(I, (w, h), interpolation=cv2.INTER_LINEAR)

    h, w = I.shape[:2]
    return cv2.resize(I, (w * scale, h * scale), interpolation=cv2.INTER_LINEAR)


## Implementation Fast Guided Filter.
class FastGuidedFilter:
    def __init__(self, I, sigma_space=5, sigma_range=0.4, scale=4):
        I_32F = to32F(I)
        self._I = I_32F
        h, w = I.shape[:2]

        print "I", I.shape
        I_sub = _downSample(I_32F, scale)
        print "I_sub", I_sub.shape

        self._I_sub = I_sub
        sigma_space = int(sigma_space / scale)

        if _isGray(I):
            self._guided_filter = GuidedFilterGray(I_sub, sigma_space, sigma_range)
        else:
            self._guided_filter = GuidedFilterColor(I_sub, sigma_space, sigma_range)

    def filter(self, p):
        p_32F = to32F(p)
        print "p_32F", p_32F.shape
        shape_original = p.shape[:2]

        p_sub = _downSample(p_32F, shape=self._I_sub.shape[:2])

        print "p_sub", p_sub.shape
        if _isGray(p_sub):
            return self._filterGray(p_sub, shape_original)

        cs = p.shape[2]
        q = np.array(p_32F)

        for ci in range(cs):
            q[:, :, ci] = self._filterGray(p_sub[:, :, ci], shape_original)
        return q

    def _filterGray(self, p_sub, shape_original):
        ab_sub = self._guided_filter._computeAB(p_sub)
        ab = [_upSample(abi, shape=shape_original) for abi in ab_sub]
        return self._guided_filter._computeLinearModel(ab, self._I)


class GuidedFilter:
    def __init__(self, I, sigma_space=5, sigma_range=0.4):
        I_32F = to32F(I)

        if _isGray(I):
            self._guided_filter = GuidedFilterGray(I_32F, sigma_space, sigma_range)
        else:
            self._guided_filter = GuidedFilterColor(I_32F, sigma_space, sigma_range)

    def filter(self, p):
        return self._guided_filter.filter(p)


class GuidedFilterCommon:
    def __init__(self, guided_filter):
        self._guided_filter = guided_filter

    def filter(self, p):
        p_32F = to32F(p)
        if _isGray(p_32F):
            return self._filterGray(p_32F)

        cs = p.shape[2]
        q = np.array(p_32F)

        for ci in range(cs):
            q[:, :, ci] = self._filterGray(p_32F[:, :, ci])
        return q

    def _filterGray(self, p):
        ab = self._guided_filter._computeAB(p)
        return self._guided_filter._computeLinearModel(ab, self._guided_filter._I)


class GuidedFilterGray:
    def __init__(self, I, sigma_space=5, sigma_range=0.4):
        self._sigma_space = 2 * sigma_space + 1
        self._sigma_range = sigma_range
        self._I = to32F(I)
        self._initFilter()
        self._filter_common = GuidedFilterCommon(self)

    def filter(self, p):
        return self._filter_common.filter(p)

    def _initFilter(self):
        I = self._I
        r = self._sigma_space
        self._I_mean = cv2.blur(I, (r, r))
        I_mean_sq = cv2.blur(I ** 2, (r, r))
        self._I_var = I_mean_sq - self._I_mean ** 2

    def _computeAB(self, p):
        r = self._sigma_space
        p_mean = cv2.blur(p, (r, r))
        p_cov = p_mean - self._I_mean * p_mean
        a = p_cov / (self._I_var + self._sigma_range)
        b = p_mean - a * self._I_mean
        a_mean = cv2.blur(a, (r, r))
        b_mean = cv2.blur(b, (r, r))
        return a_mean, b_mean

    def _computeLinearModel(self, ab, I):
        a_mean, b_mean = ab
        return a_mean * I + b_mean


class GuidedFilterColor:
    def __init__(self, I, sigma_space=5, sigma_range=0.2):
        self._sigma_space = 2 * sigma_space + 1
        self._sigma_range = sigma_range
        self._I = to32F(I)
        self._initFilter()
        self._filter_common = GuidedFilterCommon(self)

    def filter(self, p):
        return self._filter_common.filter(p)

    def _initFilter(self):
        I = self._I
        r = self._sigma_space
        eps = self._sigma_range

        Ir, Ig, Ib = I[:, :, 0], I[:, :, 1], I[:, :, 2]

        self._Ir_mean = cv2.blur(Ir, (r, r))
        self._Ig_mean = cv2.blur(Ig, (r, r))
        self._Ib_mean = cv2.blur(Ib, (r, r))

        Irr_var = cv2.blur(Ir ** 2, (r, r)) - self._Ir_mean ** 2 + eps
        Irg_var = cv2.blur(Ir * Ig, (r, r)) - self._Ir_mean * self._Ig_mean
        Irb_var = cv2.blur(Ir * Ib, (r, r)) - self._Ir_mean * self._Ib_mean
        Igg_var = cv2.blur(Ig * Ig, (r, r)) - self._Ig_mean * self._Ig_mean + eps
        Igb_var = cv2.blur(Ig * Ib, (r, r)) - self._Ig_mean * self._Ib_mean
        Ibb_var = cv2.blur(Ib * Ib, (r, r)) - self._Ib_mean * self._Ib_mean + eps

        Irr_inv = Igg_var * Ibb_var - Igb_var * Igb_var
        Irg_inv = Igb_var * Irb_var - Irg_var * Ibb_var
        Irb_inv = Irg_var * Igb_var - Igg_var * Irb_var
        Igg_inv = Irr_var * Ibb_var - Irb_var * Irb_var
        Igb_inv = Irb_var * Irg_var - Irr_var * Igb_var
        Ibb_inv = Irr_var * Igg_var - Irg_var * Irg_var

        I_cov = Irr_inv * Irr_var + Irg_inv * Irg_var + Irb_inv * Irb_var
        Irr_inv /= I_cov
        Irg_inv /= I_cov
        Irb_inv /= I_cov
        Igg_inv /= I_cov
        Igb_inv /= I_cov
        Ibb_inv /= I_cov

        self._Irr_inv = Irr_inv
        self._Irg_inv = Irg_inv
        self._Irb_inv = Irb_inv
        self._Igg_inv = Igg_inv
        self._Igb_inv = Igb_inv
        self._Ibb_inv = Ibb_inv

    def _computeAB(self, p):
        r = self._sigma_space
        I = self._I
        Ir, Ig, Ib = I[:, :, 0], I[:, :, 1], I[:, :, 2]

        p_mean = cv2.blur(p, (r, r))

        Ipr_mean = cv2.blur(Ir * p, (r, r))
        Ipg_mean = cv2.blur(Ig * p, (r, r))
        Ipb_mean = cv2.blur(Ib * p, (r, r))

        Ipr_cov = Ipr_mean - self._Ir_mean * p_mean
        Ipg_cov = Ipg_mean - self._Ig_mean * p_mean
        Ipb_cov = Ipb_mean - self._Ib_mean * p_mean

        ar = self._Irr_inv * Ipr_cov + self._Irg_inv * Ipg_cov + self._Irb_inv * Ipb_cov
        ag = self._Irg_inv * Ipr_cov + self._Igg_inv * Ipg_cov + self._Igb_inv * Ipb_cov
        ab = self._Irb_inv * Ipr_cov + self._Igb_inv * Ipg_cov + self._Ibb_inv * Ipb_cov
        b = p_mean - ar * self._Ir_mean - ag * self._Ig_mean - ab * self._Ib_mean

        ar_mean = cv2.blur(ar, (r, r))
        ag_mean = cv2.blur(ag, (r, r))
        ab_mean = cv2.blur(ab, (r, r))
        b_mean = cv2.blur(b, (r, r))

        return ar_mean, ag_mean, ab_mean, b_mean

    def _computeLinearModel(self, ab, I):
        ar_mean, ag_mean, ab_mean, b_mean = ab

        Ir, Ig, Ib = I[:, :, 0], I[:, :, 1], I[:, :, 2]

        q = (ar_mean * Ir +
             ag_mean * Ig +
             ab_mean * Ib +
             b_mean)

        return q
