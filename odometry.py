from math import atan2, sqrt, pi, fabs
from ev3dev.ev3 import *
from time import sleep


class Odometry:
    def __init__(self,
                 left_motor: LargeMotor,
                 right_motor: LargeMotor,
                 wheel_base_half: float,
                 wheel_radius: float,
                 v: float,
                 w: float,
                 x: float=0.0,
                 y: float=0.0,
                 theta: float=0.0):
        self._left_motor = left_motor
        self._right_motor = right_motor
        self._wheel_base_half = wheel_base_half
        self._wheel_radius = wheel_radius
        self._x = x
        self._y = y
        self._theta = theta
        self._w = w
        self._v = v

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def theta(self) -> float:
        return self._theta

    def drive_to(self, new_x: float, new_y: float, new_theta: float):
        alpha = atan2(new_y - self._y, new_x - self._x)
        beta = alpha - self._theta

        dt = fabs(beta / self._w)

        if beta >= 0:
            w = self._w
        else:
            w = -self._w

        self._drive_to(0.0, w, dt)
        sleep(dt)

        distance = sqrt((new_x - self._x) ** 2 + (new_y - self._y) ** 2)

        dt = distance / self._v
        self._drive_to(self._v, 0.0, dt)
        sleep(dt)

        gamma = new_theta - alpha
        dt = fabs(gamma / self._w)

        if gamma >= 0:
            w = self._w
        else:
            w = -self._w

        self._drive_to(0.0, w, dt)
        sleep(dt)

        self._x = new_x
        self._y = new_y
        self._theta = new_theta

    def _drive_to(self, v: float, w: float, dt: float):
        wl = (v - w * self._wheel_base_half) / self._wheel_radius
        wr = (v + w * self._wheel_base_half) / self._wheel_radius

        wl = wl * self._left_motor.count_per_rot / (2 * pi)
        wr = wr * self._right_motor.count_per_rot / (2 * pi)

        self._left_motor.speed_sp = wl
        self._left_motor.run_to_rel_pos(position_sp=wl*dt)

        self._right_motor.speed_sp = wr
        self._right_motor.run_to_rel_pos(position_sp=wr*dt)
