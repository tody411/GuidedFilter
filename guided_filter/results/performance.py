from guided_filter.datasets.google_image import dataFile

# -*- coding: utf-8 -*-
## @package guided_filter.results.performance
#
#  Simple performance test.
#  @author      tody
#  @date        2015/08/26

import os
import numpy as np

from guided_filter.io_util.image import loadRGB
from guided_filter.cv.image import to32F
from guided_filter.util.timer import timing_func, Timer
from guided_filter.core.filters import GuidedFilter, FastGuidedFilter


def performanceTestFilter(C_noise,  filter_name, filter, result):
    t = Timer()
    filter.filter(C_noise)
    t.stop()
    result[filter_name] = str(t)

def filterVariations(C_32F):
    sigmas = [10, 40, 80]
    filter_types = {"Simple": GuidedFilter, "Fast": FastGuidedFilter}

    filters = {}

    for type_name, filter in filter_types.items():
        for sigma in sigmas:
            filter_name = type_name + "_%s" % (sigma)
            filters[filter_name] = filter(C_32F, sigma_space=sigma)
    return filters

def performanceTest(image_file):
    image_name = os.path.basename(image_file)
    image_name = os.path.splitext(image_name)[0]

    C_8U = loadRGB(image_file)
    C_32F = to32F(C_8U)
    print "Image size: ", C_32F.shape[:2]

    h, w, cs = C_32F.shape

    C_noise = np.float32(C_32F + 0.3 * np.random.rand(h, w, cs))
    C_noise = np.clip(C_noise, 0.0, 1.0)

    filters = filterVariations(C_32F)
    result = {}
    for filter_name, filter in filters.items():
        performanceTestFilter(C_noise, filter_name, filter, result)

    for filter_name, performance in sorted(result.items()):
        print filter_name, performance

def performanceTests(data_names, data_ids):
    for data_name in data_names:
        print "Performance tests: %s" % data_name
        for data_id in data_ids:
            print "Data ID: %s" % data_id
            image_file = dataFile(data_name, data_id)
            performanceTest(image_file)

if __name__ == '__main__':
    data_names = ["apple", "flower", "tulip"]
    data_ids = [0, 1, 2]

    performanceTests(data_names, data_ids)