import numpy as np
from scipy.signal import convolve2d

matrix = (np.random.rand(10, 10) < 0.2).astype(int)
kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
neighbors = convolve2d(matrix, kernel, mode='same', boundary='wrap')
birth = np.isin(neighbors, [3]) & (matrix == 0)
survive = np.isin(neighbors, [2, 3]) & (matrix == 1)
matrix = (birth | survive).astype(int)
print(matrix.sum())
