from motor import Motor
from machine import Pin
from time import sleep

# Globale Variablen
speed_motor_fr = 1
speed_motor_fl = 1
speed_motor_br = 1
speed_motor_bl = 1

# GPIOs zur Ansteuerung der Motoren
pin_mfr_a = 40  # motor vorne rechts
pin_mfr_b = 39  # motor vorne rechts
pin_mfl_a = 38  # motor vorne links
pin_mfl_b = 37  # motor vorne links
pin_mbr_a = 36  # motor hinten rechts
pin_mbr_b = 35  # motor hinten rechts
pin_mbl_a = 34  # motor hinten links
pin_mbl_b = 33  # motor hinten links

motor_fr = Motor(pin_mfr_a, pin_mfr_b)
motor_fl = Motor(pin_mfl_a, pin_mfl_b)
motor_br = Motor(pin_mbr_a, pin_mbr_b)
motor_bl = Motor(pin_mbl_a, pin_mbl_b)

# forward
motor_fr.forward(speed_motor_fr)
motor_fl.forward(speed_motor_fl)
motor_br.forward(speed_motor_br)
motor_bl.forward(speed_motor_bl)
sleep(1)
motor_fr.stop()
motor_fl.stop()
motor_br.stop()
motor_bl.stop()
sleep(1)
# right
motor_fr.forward(speed_motor_fr)
motor_fl.backward(speed_motor_fl)
motor_br.backward(speed_motor_br)
motor_bl.forward(speed_motor_bl)
sleep(2)
motor_fr.stop()
motor_fl.stop()
motor_br.stop()
motor_bl.stop()
sleep(1)
# backward
motor_fr.backward(speed_motor_fr)
motor_fl.backward(speed_motor_fl)
motor_br.backward(speed_motor_br)
motor_bl.backward(speed_motor_bl)
sleep(1)
motor_fr.stop()
motor_fl.stop()
motor_br.stop()
motor_bl.stop()
sleep(1)
# left
motor_fr.backward(speed_motor_fr)
motor_fl.forward(speed_motor_fl)
motor_br.forward(speed_motor_br)
motor_bl.backward(speed_motor_bl)
sleep(2)
motor_fr.stop()
motor_fl.stop()
motor_br.stop()
motor_bl.stop()
sleep(1)

# turn right
motor_fr.forward(speed_motor_fr)
motor_fl.backward(speed_motor_fl)
motor_br.forward(speed_motor_br)
motor_bl.backward(speed_motor_bl)
sleep(2)
motor_fr.stop()
motor_fl.stop()
motor_br.stop()
motor_bl.stop()
sleep(1)

# turn left
motor_fr.backward(speed_motor_fr)
motor_fl.forward(speed_motor_fl)
motor_br.backward(speed_motor_br)
motor_bl.forward(speed_motor_bl)
sleep(2)
motor_fr.stop()
motor_fl.stop()
motor_br.stop()
motor_bl.stop()
sleep(1)