from ev3dev.ev3 import UltrasonicSensor
from odometry import Odometry
from filters import PIDController
from math import pi, atan2
from time import sleep


class WheeledRobotController:
    def __init__(self, left_sonar: UltrasonicSensor, right_sonar: UltrasonicSensor, odometry: Odometry):
        self._left_sonar = left_sonar
        self._right_sonar = right_sonar
        self._odometry = odometry

    @property
    def odometry(self):
        return self._odometry

    def run_closed_loop(self,
                        kp: float,
                        ki: float,
                        kd: float,
                        switch_threshold: float,
                        switch_angle: float,
                        switch_distance: float,
                        delta: float = 0.1):
        pid = None

        while True:
            left_distance = self._left_sonar.distance_centimeters
            right_distance = self._right_sonar.distance_centimeters

            if left_distance > switch_threshold:
                self._odometry.autonomous_rotation(switch_angle, switch_distance, pi / 2.0 - switch_angle)
                pid = None
            elif right_distance > switch_threshold:
                self._odometry.autonomous_rotation(-switch_angle, switch_distance, -(pi / 2.0 - switch_angle))
                pid = None
            else:
                if pid is None:
                    pid = PIDController(kp, ki, kd)

                err = atan2(left_distance - right_distance, 1.0)

                angle = pid.filter(err)

                self._odometry.start_driving(angle, delta)
                sleep(delta)