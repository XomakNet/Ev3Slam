from math import pi, cos, sin
from typing import List
from typing import Tuple

import numpy as np

__author__ = 'Xomak'


class MapConverter:

    def __init__(self, cell_size: float, columns: float, rows: float):
        self.rows = rows
        self.columns = columns
        self.cell_size = cell_size

    @property
    def width(self):
        return self.cell_size * self.columns

    @property
    def height(self):
        return self.cell_size * self.rows

    def _get_cell_x_y(self, x, y):
        if (0 <= x < self.width) and (0 <= y <= self.height):
            cell_x = int(x / self.cell_size)
            cell_y = int(y / self.cell_size)
            return cell_x, cell_y
        else:
            raise ValueError("Out of field")

    def proceed(self, sodar_data: List[Tuple], position: np.array):

        map_array = np.zeros((self.rows, self.columns), dtype=int)

        for row in sodar_data:
            relative_angle, distance = row[0], row[1]

            relative_x = - cos(relative_angle) * distance
            relative_y = sin(relative_angle) * distance

            rotation_angle = position[2] - pi/2

            rotated_x = relative_x * cos(rotation_angle) - relative_y * sin(rotation_angle)
            rotated_y = relative_y * cos(rotation_angle) + relative_x * sin(rotation_angle)

            shifted_x = rotated_x + position[0]
            shifted_y = rotated_y + position[1]

            cell_x, cell_y = self._get_cell_x_y(shifted_x, shifted_y)

            map_array[cell_y, cell_x] = 1

        return map_array

