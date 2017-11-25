import matplotlib.pyplot as plt
import numpy as np

__author__ = 'Xomak'


data = np.loadtxt('test.csv', delimiter=',')
#data = data[data[:, 0].argsort()]

plt.plot(data[:, 0], data[:, 1], 'ro')
plt.show()
