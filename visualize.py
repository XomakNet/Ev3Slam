import csv
import matplotlib.pyplot as plt

__author__ = 'Xomak'

with open('map.csv', 'r', newline='') as csvfile:
    cloud_reader = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    x = []
    y = []
    for row in cloud_reader:
        x.append(row[2])
        y.append(row[3])

plt.plot(x, y, 'ro')
plt.show()
