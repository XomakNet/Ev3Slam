from collections import namedtuple
from math import pi
import time

import ev3dev.ev3 as ev3

__author__ = 'Xomak'


class ScanningSonar:

    ScanParams = namedtuple('ScanParams', ('start_position', 'end_position', 'step', 'scan_time'))
    POLLING_INTERVAL = 0.1

    def __init__(self, motor: ev3.Motor, sonar: ev3.UltrasonicSensor, range: ScanParams):
        self.range = range
        self.motor = motor
        self.sonar = sonar
        self.current_angle = None
        self._measured = None

    def _move_to_start(self):
        self._move(self.range.start_position)

    def _move(self, radians: float):
        tachos = radians / (2 * pi) * self.motor.count_per_rot
        self.motor.run_to_abs_pos(position_sp=tachos, stop_action='hold')

    def _blocking_move(self, radians: float):
        self._move(radians)
        while self.motor.STATE_HOLDING not in self.motor.state:
            time.sleep(self.POLLING_INTERVAL)
        self.current_angle = radians

    def _on_position(self):
        time.sleep(self.range.scan_time)
        self._measured[self.current_angle] = self.sonar.distance_centimeters

    def scan(self):
        self._measured = dict()

        if self.current_angle is None:
            self._blocking_move(self.range.start_position)
        if self.current_angle == self.range.end_position:
            # Inversed direction
            scan_range = range(self.range.end_position, self.range.start_position, -self.range.step)
        else:
            scan_range = range(self.range.start_position, self.range.end_position, self.range.step)

        for angle in scan_range:
            self._blocking_move(angle)
            self._on_position()

        return self._measured

