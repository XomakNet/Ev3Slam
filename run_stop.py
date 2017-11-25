from odometry import Odometry
from robot import Robot
from math import pi

host = '169.254.143.159'

robot = Robot(host)
robot.connect()

odometry = Odometry(robot.get_ev3().LargeMotor("outC"),
                    robot.get_ev3().LargeMotor("outB"),
                    6.0,
                    2.7,
                    6.0,
                    2 * pi / 5.0)

odometry.stop_driving()