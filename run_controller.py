from odometry import Odometry
from robot import Robot
from controller import WheeledRobotController
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

controller = WheeledRobotController(robot.get_ev3().UltrasonicSensor("in2"),
                                    robot.get_ev3().UltrasonicSensor("in4"),
                                    odometry)
controller.run_closed_loop(kp=1.0,
                           ki=0.0,
                           kd=0.0,
                           switch_threshold=2000.0,
                           switch_angle=pi/4.0,
                           switch_distance=30.0,
                           delta=2.0)
