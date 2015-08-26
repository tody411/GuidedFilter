# -*- coding: utf-8 -*-
## @package guided_filter.main
#
#  Main functions.
#  @author      tody
#  @date        2015/08/19
from guided_filter.datasets.google_image import createDatasets

from guided_filter.results.smooth_noise import runSmoothNoiseResults

if __name__ == '__main__':
    data_names = ["flower"]
    num_images = 3
    data_ids = range(num_images)

    createDatasets(data_names, num_images, update=False)
    runSmoothNoiseResults(data_names, data_ids)
