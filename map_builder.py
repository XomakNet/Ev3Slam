import csv
from collections import namedtuple

from math import cos, sin, pi

from common.utils import Pose

__author__ = 'Xomak'


class MapBuilder:

    SonarsData = namedtuple('SonarsData', ('left', 'right'))
    Point = namedtuple('Point', ('x', 'y'))

    @classmethod
    def rotate_point_over(cls, point_to_rotate: Point, key_point: Point, angle: float):

        point_to_rotate = cls.Point(point_to_rotate.x - key_point.x,
                                    point_to_rotate.y - key_point.y)

        c = cos(angle)
        s = sin(angle)

        point_to_rotate = cls.Point(point_to_rotate.x * c - point_to_rotate.y * s,
                                    point_to_rotate.x * s + point_to_rotate.y * c)

        point_to_rotate = cls.Point(point_to_rotate.x + key_point.x,
                                    point_to_rotate.y + key_point.y)

        return point_to_rotate

    def __init__(self):
        self.points = []

    def push_point(self, point):
        self.points.append(point)

    def push(self, position: Pose, sonars: SonarsData):
        #total_dst = sonars.left.x + sonars.right.x + 15
        left_point = self.Point(position.x - sonars.left, position.y)
        right_point = self.Point(position.x + sonars.right, position.y)

        angle = position.theta - pi/2
        vehicle_point = self.Point(position.x, position.y)

        left_point = self.rotate_point_over(left_point, vehicle_point, angle)
        right_point = self.rotate_point_over(right_point, vehicle_point, angle)

        self.points.append(left_point)
        self.points.append(right_point)

    def write_to_file(self, filename):
        with open(filename, 'w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for point in self.points:
                csv_writer.writerow([point.x, point.y])
