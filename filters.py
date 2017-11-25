class PIDController:
    def __init__(self, kp: float, ki: float, kd: float, initial=0.0):
        self._kp = kp
        self._ki = ki
        self._kd = kd
        self._accumulator = 0.0
        self._prev = initial

    def filter(self, value: float) -> float:
        self._accumulator += value
        result = self._kp*value + self._ki*self._accumulator + self._kd*(value - self._prev)
        self._prev = value
        return result
