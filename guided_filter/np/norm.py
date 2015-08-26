# -*- coding: utf-8 -*-
## @package guided_filter.np.norm
#
#  Norm functions.
#  @author      tody
#  @date        2015/07/18

import numpy as np


## True if x is a vector.
def isVector(x):
    return x.size == x.shape[0]


## True if x is a matrix.
def isMatrix(x):
    return not isVector(x)


## Normalize vector.
def normalizeVector(x):
    norm = np.linalg.norm(x)
    y = x
    if norm > 0:
        y = np.ravel((1.0 / norm) * x)
    return y


## Normalize vectors (n x m matrix).
def normalizeVectors(x):
    norm = normVectors(x)
    nonZeroIDs = norm > 0
    x[nonZeroIDs] = (x[nonZeroIDs].T / norm[nonZeroIDs]).T
    return x


## Norm of vectors (n x m matrix).
def normVectors(x):
    return np.sqrt(l2NormVectors(x))


## L2 norm of vectors (n x m matrix).
#  n x 1 vector: call np.square.
#  n x m vectors: call np.einsum.
def l2NormVectors(x):
    if isVector(x):
        return np.square(x)
    else:
        return np.einsum('...i,...i', x, x)
