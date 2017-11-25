from odometry import Odometry
from robot import Robot
from math import pi

host = '169.254.251.238'

robot = Robot(host)
robot.connect()

odometry = Odometry(robot.get_ev3().LargeMotor("outC"),
                    robot.get_ev3().LargeMotor("outB"),
                    6.0,
                    2.7,
                    6.0,
           2 * pi / 5.0)
odometry.drive_to(-30.0, 0.0, 0)
odometry.drive_to(-30.0, 30.0, 0)
odometry.drive_to(-60.0, 60.0, pi)