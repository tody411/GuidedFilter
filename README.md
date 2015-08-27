
Guided Imaged Filtering Demo (Python)
====

Simple python demos of Guided Image Filtering [He et al. 2010].

The guided filter can perform edge-preserving smoothing filtering like the popular bilateral filter.

In this demo package, I also implemented **Fast Guided Filter** [He et al. 2015].

## Result

### Simple guided filter test for noise image:

1. Noise image from original image.
2. Guided filter smooth the noise image like bilateral filter.
    * Guidance image: Noise image.
    * Epsilon (regularization term similar to the sigma in the color space): Constant 0.05.
    * Radius (similar to the sigma in the coordinate space): [5, 10, 20]

![flower_1](guided_filter/results/flower_1.png)

### Performance

Compare the performance of the following filters:

* Bilateral filter: OpenCV implementation.
* Guided filter [He et al. 2010]: Implemented in this package.
* Fast guided filter [He et al. 2015]: Implemented in this package.

![performance](guided_filter/results/performance.png)

Compared with the bilateral filter, guided filters are **independent of filtering sigma for coordinates**.
Fast guided filter leads to a speed up of 4x in this implementation.

## Installation

*Note*: This program was only tested on **Windows** with **Python2.7**.
**Linux** and **Mac OS** are not officially supported,
but the following instructions might be helpful for installing on those environments.

### Dependencies
Please install the following required python modules.

* **NumPy**
* **SciPy**
* **matplotlib**
* **OpenCV**

As these modules are heavily dependent on NumPy modules, please install appropriate packages for your development environment (Python versions, 32-bit or 64-bit).
For 64-bit Windows, you can download the binaries from [**Unofficial Windows Binaries for Python Extension Packages**](http://www.lfd.uci.edu/~gohlke/pythonlibs/).

<!-- This program also uses **docopt** for CLI.
**docopt** will be installed automatically through the following **pip** command for main modules. -->

### Install main modules

You can use **pip** command for installing main modules.
Please run the following command from the shell.

``` bash
  > pip install git+https://github.com/tody411/GuidedFilter.git
```

## Usage
### Package Structure
* guided_filter: Main package.
    - main.py: Main module for testing.
    - results: Result images will be saved in the directory.

### Test Guided Filter Demo
You can test the Guided Filter with the following command from ```guided_filter``` directory..
``` bash
  > python main.py
```

This command will start downloading test images via Google Image API then run the ```guided_filter``` module to generate result images.

<!-- ## API Document

API document will be managed by [doxygen](http://www.stack.nl/~dimitri/doxygen/) framework.
Online version is provided in the following link:
* [**inversetoon API Document**](http://tody411.github.io/InverseToon/index.html) (html)

For a local copy, please use the following doxygen command from *doxygen* directory.
``` bash
  > doxygen doxygen_config
``` -->

<!-- ## Future tasks

* [ ] Performance tests. -->

## License

The MIT License 2015 (c) tody