# -*- coding: utf-8 -*-
## @package guided_filter.results.results
#
#  Results utility package.
#  @author      tody
#  @date        2015/08/20

import os

_root_dir = os.path.dirname(__file__)


## Result directory.
def resultDir():
    return _root_dir


def resultFile(image_name, image_ext=".png"):
    result_file = os.path.join(resultDir(), image_name + image_ext)
    return result_file

if __name__ == '__main__':
    print resultDir()
    print resultFile("testImage")