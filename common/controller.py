from collections import namedtuple
from enum import Enum

import time

from common.pid import PIDRegulator
from common.utils import get_json_from_file
from map_builder import MapBuilder
from rotater import Rotater

__author__ = 'Xomak'

class State:
    def __init__(self, controller):
        self.controller = controller


class Controller:

    Motors = namedtuple('Motors', ('left', 'right'))
    Sonars = namedtuple('Sonars', ('left', 'right', 'front'))

    def __init__(self, sonars: Sonars, motors: Motors):
        self.sonars = sonars
        self.rotater = Rotater(motors.left, motors.right)
        self.pid_and_speed_file = 'data/pid_and_speed.json'
        self.pid_and_speed_params = None
        self._update_params()
        self.last_state_change = None
        self.state = Walking(self)
        self.map = MapBuilder()

    def _get_sonar_value(self, sonar):
        val = None
        for i in range(0, 5):
            if val is None:
                val = sonar.distance_centimeters
            else:
                val += sonar.distance_centimeters
        return val/5

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state
        self.last_state_change = time.time()

    def timeout_expired(self):
        return time.time() - self.last_state_change > 0.9

    def _update_params(self):
        try:
            self.pid_and_speed_params = get_json_from_file(self.pid_and_speed_file)
        except Exception:
            print("Error reading PID params.")

    def run(self):
        while True:
            self.state.cycle()


class Walking(State):

    def __init__(self, controller):
        super().__init__(controller)
        self.speed_bounds = [0, 960]
        self.pid_regulator = PIDRegulator()

    def _limit_speed(self, speed):
        if speed < self.speed_bounds[0]:
            speed = self.speed_bounds[0]
        if speed > self.speed_bounds[1]:
            speed = self.speed_bounds[1]
        return speed

    def cycle(self):
        self.pid_regulator.p = self.controller.pid_and_speed_params['p']
        self.pid_regulator.i = self.controller.pid_and_speed_params['i']
        self.pid_regulator.d = self.controller.pid_and_speed_params['d']

        corridor_width = self.controller.pid_and_speed_params['corridor_width']

        left_value = self.controller.sonars.left.distance_centimeters
        right_value = self.controller.sonars.right.distance_centimeters

        left_turn = left_value > corridor_width
        right_turn = right_value > corridor_width

        #if 1 != 1 and (left_turn or right_turn):
        if (left_turn or right_turn) and self.controller.timeout_expired():
            turn = 0
            if left_turn:
                turn = TurnAction.TURN_LEFT
            if right_turn:
                turn = TurnAction.TURN_RIGHT
            self.controller.map.write_to_file('test.csv')
            self.controller.state = TurnBeginning(self.controller, turn)
        elif self.controller.sonars.front.distance_centimeters < 5:
            self.controller.state = Finished(self.controller)
        else:
            error = left_value - right_value
            delta = self.pid_regulator.proceed(error)

            base_speed = self.controller.pid_and_speed_params['speed']
            left_speed = self._limit_speed(base_speed - delta)
            right_speed = self._limit_speed(base_speed + delta)

            self.controller.rotater.set_wheel_speeds(left_speed, right_speed)
            self.controller.map.push(self.controller.rotater.pose, MapBuilder.SonarsData(left_value, right_value))
            print(self.controller.rotater.pose)


class TurnBeginning(State):

    def __init__(self, controller, turn_type):
        super().__init__(controller)
        self.turn_type = turn_type
        self.initial_distance = self.front_distance
        base_speed = self.controller.pid_and_speed_params['speed']
        self.controller.rotater.set_wheel_speeds(base_speed, base_speed)
        print("Turn beginning")

    @property
    def front_distance(self):
        return self.controller._get_sonar_value(self.controller.sonars.front)

    def cycle(self):
        if self.front_distance < self.initial_distance / 2 - 10:
            self.controller.state = TurnAction(self.controller, self.turn_type)


class TurnAction(State):

    TURN_RIGHT = 1
    TURN_LEFT = 2

    def __init__(self, controller, turn_type):
        super().__init__(controller)
        if turn_type == self.TURN_RIGHT:
            self.controller.rotater.turn_right()
        if turn_type == self.TURN_LEFT:
            self.controller.rotater.turn_left()
        print("Turn action")

    def cycle(self):
        if not self.controller.rotater.is_running():
            self.controller.state = AfterTurnAction(self.controller)


class AfterTurnAction(State):

    def __init__(self, controller):
        super().__init__(controller)
        base_speed = self.controller.pid_and_speed_params['speed']
        self.controller.rotater.set_wheel_speeds(base_speed, base_speed)
        print("After turn")

    def cycle(self):
        corridor_width = self.controller.pid_and_speed_params['corridor_width']
        left_value = self.controller._get_sonar_value(self.controller.sonars.left)
        right_value = self.controller._get_sonar_value(self.controller.sonars.right)
        print("{}, {}".format(left_value, right_value))

        if left_value < corridor_width\
                and right_value < corridor_width \
                and self.controller.timeout_expired():
            self.controller.state = Walking(self.controller)


class Finished(State):

    def __init__(self, controller):
        super().__init__(controller)
        print("Finished")

    def cycle(self):
        pass