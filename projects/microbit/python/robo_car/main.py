# Imports go at the top
from microbit import *
from random import choice
from motor import Motor
from hcsr04 import HCSR04


# Motorenleistung/Geschwindigkeit, anpassen für Geradeauslauf
speed_m1 = 500
speed_m2 = 500
speed_max = 1023

# GPIOs zur Ansteuerung der Motoren
pin_m1a = pin8  # motor 1
pin_m1b = pin9  # motor 1
pin_m2a = pin12  # motor 2
pin_m2b = pin16  # motor 2
# GPIOs des Abstandssensors
pin_trigger = pin15
pin_echo = pin14

motor1 = Motor(pin_m1a, pin_m1b)
motor2 = Motor(pin_m2a, pin_m2b)
sensor = HCSR04(pin_trigger, pin_echo)


def robo_stop():
    motor1.stop()
    motor2.stop()
    sleep(500)


def robo_go():
    display.show(Image.ARROW_S)
    motor1.forward(speed_m1)
    motor2.forward(speed_m2)


def robo_turn():
    richtung = choice([0, 1])
    display.show(Image("00000:09090:99999:09090:00000"))
    if richtung:
        motor1.forward(speed_m1)
        motor2.backward(speed_m2)
    else:
        motor1.backward(speed_m1)
        motor2.forward(speed_m2)
    delay = choice([250, 500, 750])
    sleep(delay)
    robo_stop()


while True:
    sensor_value = sensor.distance_cm()
    if sensor_value < 0:
        continue
    print(sensor_value)

    if sensor_value < 40:
        robo_stop()
        robo_turn()
    else:
        robo_go()

