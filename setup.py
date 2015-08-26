# -*- coding: utf-8 -*-
## @package setup
#
#  setup utility package.
#  @author      tody
#  @date        2015/08/14

from setuptools import setup, find_packages
from guided_filter import __author__, __version__, __license__

setup(
        name = 'guided_filter',
        version = __version__,
        description = 'Simple python demos of Guided Image Filtering [He et al. 2010].',
        license = __license__,
        author = __author__,
        url = 'https://github.com/tody411/GuidedFilter.git',
        packages = find_packages(),
        install_requires = ['docopt'],
        )

