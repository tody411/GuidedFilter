from guided_filter.datasets.google_image import dataFile

# -*- coding: utf-8 -*-
## @package guided_filter.results.performance
#
#  Simple performance test.
#  @author      tody
#  @date        2015/08/26

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

from guided_filter.io_util.image import loadRGB
from guided_filter.cv.image import to32F
from guided_filter.util.timer import timing_func, Timer
from guided_filter.core.filters import GuidedFilter, FastGuidedFilter
from guided_filter.results.results import resultFile


## Bilateral filter class with the same interface with GuidedFilter class.
#
#  Input I for the constructor will be discarded.
class BilateralFilter:
    def __init__(self, I, radius=5, epsilon=0.2):
        self._epsilon = epsilon
        self._radius = radius

    def filter(self, I):
        return cv2.bilateralFilter(I, 0, self._epsilon, self._radius)


## Peformance test for the input image and the target filter.
def performanceTestFilter(C_noise, filter):
    t = Timer()
    filter.filter(C_noise)
    t.stop()
    return t.seconds()


## Generate filter variations for the target filter class, sigmas.
def generateFilterVariations(C_32F, filter_class, sigmas):
    filters = []
    for sigma in sigmas:
        filters.append(filter_class(C_32F, radius=sigma))
    return filters


## Performance test for the target sigmas.
def performanceTestSigmas(C_32F, sigmas, filter_types, ax):
    h, w, cs = C_32F.shape

    C_noise = np.float32(C_32F + 0.3 * np.random.rand(h, w, cs))
    C_noise = np.clip(C_noise, 0.0, 1.0)

    for type_name, filter_class_color in filter_types.items():
        filter_class, color = filter_class_color
        filters = generateFilterVariations(C_32F, filter_class, sigmas)
        times = []

        for filter in filters:
            times.append(performanceTestFilter(C_noise, filter))

        ax.plot(sigmas, times, label=type_name, color=color)

    ax.set_xlabel('radius $r$')
    ax.set_ylabel('time (secs)')
    ax.legend(bbox_to_anchor=(0.88, 0.8), loc=2)


## Performance test for the image file.
def performanceTest(image_file):
    C_8U = loadRGB(image_file)
    C_32F = to32F(C_8U)

    h, w = C_32F.shape[:2]
    image_size_str = "Image size: %s x %s" %(w, h)

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 8))
    fig.subplots_adjust(left=0.1, right=0.7, top=0.86, hspace=0.4)

    fig.suptitle("Peformance of guided filter\n%s" % image_size_str)

    filter_types = {"Bilateral Filter": (BilateralFilter, "r"),
                    "Guided Filter": (GuidedFilter, "g"),
                    "Fast Guided Filter": (FastGuidedFilter, "b")}

    sigmas = range(3, 31, 2)
    axes[0].set_title('For small radius $r$')

    performanceTestSigmas(C_32F, sigmas, filter_types, axes[0])

    sigmas = range(10, 100, 5)

    filter_types = {"Guided Filter": (GuidedFilter, "g"),
                    "Fast Guided Filter": (FastGuidedFilter, "b")}

    axes[1].set_title('For large radius $r$')
    performanceTestSigmas(C_32F, sigmas, filter_types, axes[1])

    result_name = "performance"
    result_file = resultFile(result_name)
    plt.savefig(result_file)


## Performance tests for the data names, IDs.
def performanceTests(data_names, data_ids):
    for data_name in data_names:
        print "Performance tests: %s" % data_name
        for data_id in data_ids:
            print "Data ID: %s" % data_id
            image_file = dataFile(data_name, data_id)
            performanceTest(image_file)

if __name__ == '__main__':
    data_names = ["flower"]
    data_ids = [0]

    performanceTests(data_names, data_ids)