from math import pi, cos, sin
import csv

from scanning_sonar import ScanningSonar
import ev3dev.ev3 as ev3


__author__ = 'Xomak'

sonar = ev3.UltrasonicSensor('in2')
motor = ev3.MediumMotor('outA')

params = ScanningSonar.ScanParams(0, pi, 0.05, 0.7)

scanner = ScanningSonar(motor, sonar, params)
data = scanner.scan()


with open('map.csv', 'w', newline='') as csvfile:
    cloud_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for angle, distance in data.items():
        x = cos(angle) * distance
        y = sin(angle) * distance
        if distance < 100:
            cloud_writer.writerow([angle, distance, x, y])

