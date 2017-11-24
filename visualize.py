import matplotlib.pyplot as plt
import numpy as np

__author__ = 'Xomak'


data = np.loadtxt('map.csv', delimiter=',')
data = data[data[:, 0].argsort()]

plt.plot(data[:, 2], data[:, 3], 'ro')
plt.show()
