import ev3dev.ev3 as ev3


class TwoSensorsPositionDetector:

    def __init__(self, left_sensor: ev3.UltrasonicSensor, right_sensor: ev3.UltrasonicSensor, calibration = None):
        self.sensors = {'left': left_sensor, 'right': right_sensor}
        self.calibration = None
        self.mean = None

    def get_error(self):
        error = self.sensors['right'].distance_centimeters - self.sensors['left'].distance_centimeters

        return error