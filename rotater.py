from collections import namedtuple
import time
from math import pi, cos, sin

import ev3dev.ev3 as ev3

__author__ = 'Xomak'


class Rotater:

    TACHO_COUNT_PER_ROTATION = 360
    RPM_TO_RADIANS = 0.104719755
    RPS_TO_RADIANS = 2 * pi
    WHEEL_RADIUS = 2.75
    WHEEL_DISTANCE = 14.5 / 2
    SONAR_ENABLED_ANGLE = 45

    Pose = namedtuple('Pose', ('x', 'y', 'theta'))
    ControlInput = namedtuple('ControlInput', ('left', 'right'))

    def __init__(self, left_motor: ev3.LargeMotor, right_motor: ev3.LargeMotor,
                 speed: int = 400, rotate_constant: int = 170):
        self.rotate_constant = rotate_constant
        self.speed = speed
        self.right_motor = right_motor
        self.left_motor = left_motor
        self.pose = self.Pose(0, 0, -pi/2)
        self.last_update = time.time()
        self.control_input = None

    def recalculate_pose(self, new_control_input):
        current_time = time.time()
        if self.control_input is not None:
            self.pose = self.transition_function(self.pose, self.control_input, current_time - self.last_update)
        self.last_update = current_time
        self.control_input = new_control_input

    def set_wheel_speeds(self, left_speed, right_speed):
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)
        control_input = self.ControlInput(left_speed, right_speed)
        self.recalculate_pose(control_input)

    def turn_right(self):
        self.left_motor.speed_sp = self.speed
        self.right_motor.speed_sp = self.speed
        self.left_motor.run_to_rel_pos(position_sp=self.rotate_constant, stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=-self.rotate_constant, stop_action='brake')

    def turn_left(self):
        self.left_motor.speed_sp = self.speed
        self.right_motor.speed_sp = self.speed
        self.left_motor.run_to_rel_pos(position_sp=-self.rotate_constant, stop_action='brake')
        self.right_motor.run_to_rel_pos(position_sp=self.rotate_constant, stop_action='brake')

    def is_running(self):
        return self.left_motor.STATE_RUNNING in self.left_motor.state \
               or self.right_motor.STATE_RUNNING in self.right_motor.state

    @classmethod
    def transition_function(cls, state: Pose, control: ControlInput, time_delta: float):
        x = state.x
        y = state.y
        theta_radians = state.theta  # Theta in radians

        left_motor_speed = control[0] / cls.TACHO_COUNT_PER_ROTATION * cls.RPS_TO_RADIANS
        right_motor_speed = control[1] / cls.TACHO_COUNT_PER_ROTATION * cls.RPS_TO_RADIANS

        velocity = cls.WHEEL_RADIUS / 2 * (left_motor_speed + right_motor_speed)

        # Angular velocity in radians/s
        angular_velocity = cls.WHEEL_RADIUS / (2 * cls.WHEEL_DISTANCE) * (
            left_motor_speed - right_motor_speed)

        new_angle_radians = theta_radians + time_delta * angular_velocity

        x += time_delta * velocity * cos(new_angle_radians)
        y += time_delta * velocity * sin(new_angle_radians)

        return cls.Pose(x, y, new_angle_radians)
