import csv
from collections import namedtuple

from math import cos, sin

__author__ = 'Xomak'


class MapBuilder:

    Position = namedtuple('Position', ('x', 'y', 'theta'))
    Observations = namedtuple('Observations', ('left', 'right'))
    Point = namedtuple('Point', ('x', 'y'))

    def __init__(self):
        self.left_obstacles = []
        self.right_obstacles = []
        self.path = []

    @classmethod
    def _rotate_point(cls, point, angle):
        rotated_x = point.x * cos(angle) - point.y * sin(angle)
        rotated_y = point.y * cos(angle) + point.x * sin(angle)
        return cls.Point(rotated_x, rotated_y)

    def push(self, position: Position, observations: Observations):
        left_obstacle = self.Point(position.x - observations.left, position.y)
        right_obstacle = self.Point(position.x + observations.left, position.y)

        left_obstacle_rotated = self._rotate_point(left_obstacle, position.theta)
        right_obstacle_rotated = self._rotate_point(right_obstacle, position.theta)

        self.left_obstacles.append(left_obstacle_rotated)
        self.right_obstacles.append(right_obstacle_rotated)
        self.path.append(self.Point(position.x, position.y))

    def write_to_file(self, filename):
        with open(filename, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for left, right, pos in zip(self.left_obstacles, self.right_obstacles, self.path):
                csv_writer([left.x, left.y, right.x, right.y, pos.x, pos.y])
