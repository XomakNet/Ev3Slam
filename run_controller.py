from common.controller import Controller
import ev3dev.ev3 as ev3

__author__ = 'Xomak'

left_motor = ev3.LargeMotor('outB')
right_motor = ev3.LargeMotor('outC')

left_sonar = ev3.UltrasonicSensor('in1')
right_sonar = ev3.UltrasonicSensor('in3')
front_sonar = ev3.UltrasonicSensor('in2')

sonars = Controller.Sonars(left_sonar, right_sonar, front_sonar)
motors = Controller.Motors(left_motor, right_motor)

controller = Controller(sonars, motors)
controller.run()