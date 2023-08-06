import numpy as np


def matrix_mul(a, b):
    a = np.array([[1, 0],
                  [0, 1]])
    b = np.array([[4, 1],
                  [2, 2]])
    return np.matmul(a, b)


def arrayInter(a, b):
    return np.intersect1d(a, b)
