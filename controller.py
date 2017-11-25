from ev3dev.ev3 import UltrasonicSensor
from odometry import Odometry
from filters import PIDController


class WheeledRobotController:
    def __init__(self, left_sonar: UltrasonicSensor, right_sonar: UltrasonicSensor, odometry: Odometry):
        self._left_sonar = left_sonar
        self._right_sonar = right_sonar
        self._odometry = odometry

    def run_closed_loop(self, kp: float, ki: float, kd: float, delta: float = 0.1):
        pid = PIDController(kp, ki, kd)

        while True:
            left_distance = self._left_sonar.distance_centimeters
            right_distance = self._right_sonar.distance_centimeters

            angle = pid.filter(left_distance - right_distance)

            self.drive(-math.radians(angle) / delta)

        self.stop()