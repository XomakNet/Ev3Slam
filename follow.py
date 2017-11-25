import ev3dev.ev3 as ev3

from common.follower import Follower
from common.line_detectors import TwoSensorsPositionDetector

__author__ = 'Xomak'


left_sonar = ev3.UltrasonicSensor(address='in2')
right_sonar = ev3.UltrasonicSensor(address='in4')
left_motor = ev3.LargeMotor('outB')
right_motor = ev3.LargeMotor('outC')

line_detector = TwoSensorsPositionDetector(left_sonar, right_sonar)

follower = Follower(right_motor, left_motor, line_detector, 'data/pid_and_speed.json', update_pid=True)
follower.follow()