import numpy as np
import matplotlib.pyplot as plt

__author__ = 'Xomak'


data = np.loadtxt('map.csv', delimiter=',')
plt.scatter(data[:, 0], data[:, 1])
plt.scatter(data[:, 2], data[:, 3])
plt.scatter(data[:, 4], data[:, 5])
plt.show()