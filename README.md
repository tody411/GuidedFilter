
Guided Filter (Python)
====

Simple python demos of Guided Image Filtering [He et al. 2010].

The guided filter can perform edge-preserving smoothing filtering like the popular bilateral filter.
They used Self-Organizing Maps (**SOM**) to construct data-driven **color manifolds**.

Overview of their approach:

1. Color samples from image datasets.
2. Dimensionality reduction via **SOM**.
3. Applications: color editing, palettes, stylization, etc.

In this demo package, I only implemented **dimensionality reduction part** for a single image.

## Result
This program can generate color manifolds for the target images.
![apple_0](som_cm/results/apple_0.png)
![banana_0](som_cm/results/banana_0.png)
![flower_0](som_cm/results/flower_0.png)
![tulip_1](som_cm/results/tulip_1.png)
![sky_2](som_cm/results/sky_2.png)

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

As these modules are heavily dependent on NumPy modules, please install appropriate packages for your development environment (Python versions, 32-bit or 64bit).
For 64-bit Windows, you can download the binaries from [**Unofficial Windows Binaries for Python Extension Packages**](http://www.lfd.uci.edu/~gohlke/pythonlibs/).

<!-- This program also uses **docopt** for CLI.
**docopt** will be installed automatically through the following **pip** command for main modules. -->

### Install main modules

You can use **pip** command for installing main modules.
Please run the following command from the shell.

``` bash
  > pip install git+https://github.com/tody411/SOM-ColorManifolds.git
```

## Usage
### Package Structure
* som_cm: Main package.
    - main.py: Main module for testing.
    - results: Result images will be saved in the directory.

### Test SOM Demo
You can test the SOM with the following command from ```som_cm``` directory..
``` bash
  > python main.py
```

This command will start downloading test images via Google Image API then run the SOM module to generate result images.

<!-- ## API Document

API document will be managed by [doxygen](http://www.stack.nl/~dimitri/doxygen/) framework.
Online version is provided in the following link:
* [**inversetoon API Document**](http://tody411.github.io/InverseToon/index.html) (html)

For a local copy, please use the following doxygen command from *doxygen* directory.
``` bash
  > doxygen doxygen_config
``` -->

## Future tasks

* [ ] Implement background removal.

## License

The MIT License 2015 (c) tody