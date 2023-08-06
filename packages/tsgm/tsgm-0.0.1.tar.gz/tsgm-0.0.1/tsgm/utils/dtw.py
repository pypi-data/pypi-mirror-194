import numpy as np
import tensorflow as tf
import typing as T

from tensorflow.python.types.core import TensorLike


def _traceback(D):
    i, j = np.array(D.shape) - 2
    p, q = [i], [j]
    while (i > 0) or (j > 0):
        tb = np.argmin((D[i, j], D[i, j + 1], D[i + 1, j]))
        if tb == 0:
            i -= 1
            j -= 1
        elif tb == 1:
            i -= 1
        else:  # (tb == 2):
            j -= 1
        p.insert(0, i)
        q.insert(0, j)
    return np.array(p), np.array(q)


def dtw(x: TensorLike, y: TensorLike, dist: T.Callable, warp: int = 1, w: float = np.inf, s: float = 1.0):
    """
    Computes Dynamic Time Warping (DTW) of two sequences. A modified version of https://github.com/pollen-robotics/dtw
    :param array x: N1*M array
    :param array y: N2*M array
    :param func dist: distance used as cost measure
    :param int warp: how many shifts are computed.
    :param int w: window size limiting the maximal distance between indices of matched entries |i, j|.
    :param float s: weight applied on off-diagonal moves of the path. As s gets larger, the warping path is increasingly biased towards the diagonal
    Returns the minimum distance, the cost matrix, the accumulated cost matrix, and the wrap path.
    """
    assert len(x)
    assert len(y)
    assert tf.math.is_inf(w) or (w >= abs(len(x) - len(y)))
    assert s > 0
    r, c = len(x), len(y)
    if not tf.math.is_inf(w):
        d0 = np.full((r + 1, c + 1), inf)
        for i in range(1, r + 1):
            d0[i, max(1, i - w) : min(c + 1, i + w + 1)] = 0
        d0[0, 0] = 0
    else:
        d0 = np.zeros((r + 1, c + 1))
        d0[0, 1:] = np.inf
        d0[1:, 0] = np.inf
    d1 = d0[1:, 1:]  # view
    for i in range(r):
        for j in range(c):
            if tf.math.is_inf(w) or (max(0, i - w) <= j <= min(c, i + w)):
                d1[i, j] = dist(x[i][None, :], y[j][None, :])[0, 0]
    d1_copy = d1.copy()
    jrange = range(c)
    for i in range(r):
        if not tf.math.is_inf(w):
            jrange = range(max(0, i - w), min(c, i + w + 1))
        for j in jrange:
            min_list = [d0[i, j]]
            for k in range(1, warp + 1):
                i_k = min(i + k, r)
                j_k = min(j + k, c)
                min_list += [d0[i_k, j] * s, d0[i, j_k] * s]
            d1[i, j] += min(min_list)
    if len(x) == 1:
        path = np.zeros(len(y)), range(len(y))
    elif len(y) == 1:
        path = range(len(x)), np.zeros(len(x))
    else:
        path = _traceback(d0)
    return d1[-1, -1], d1_copy, d1, path
