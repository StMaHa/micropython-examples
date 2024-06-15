# Imports go at the top
from calliopemini import *
from random import choice
from hcsr04 import HCSR04


# Motorenleistung/Geschwindigkeit, anpassen für Geradeauslauf
speed_m1 = 800
speed_m2 = 800
speed_max = 1023
distance_limit = 40

# GPIOs des Abstandssensors
pin_trigger = pin_A1_RX
pin_echo = pin_A1_TX

sensor = HCSR04(pin_trigger, pin_echo)


def robo_stop():
    pin_M_MODE.write_digital(1)
    pin_M0_DIR.write_digital(1)
    pin_M1_DIR.write_digital(1)
    pin_M0_SPEED.write_analog(0)
    pin_M1_SPEED.write_analog(0)
    sleep(500)


def robo_go():
    display.show(Image.ARROW_N)
    pin_M_MODE.write_digital(1)
    pin_M0_DIR.write_digital(1)
    pin_M1_DIR.write_digital(1)
    pin_M0_SPEED.write_analog(speed_m1)
    pin_M1_SPEED.write_analog(speed_m2)

def robo_turn():
    display.show(Image("00000:09090:99999:09090:00000"))
    pin_M_MODE.write_digital(1)
    pin_M0_SPEED.write_analog(speed_m1)
    pin_M1_SPEED.write_analog(speed_m2)

    richtung = choice([0, 1])
    if richtung:
        pin_M0_DIR.write_digital(0)
        pin_M1_DIR.write_digital(1)
    else:
        pin_M0_DIR.write_digital(1)
        pin_M1_DIR.write_digital(0)
    delay = choice([250, 500, 750])
    sleep(delay)
    robo_stop()


while True:
    sensor_value = sensor.distance_cm()
    if sensor_value < 0:
        continue
    print(sensor_value)

    if sensor_value < distance_limit:
        robo_stop()
        robo_turn()
    else:
        robo_go()
