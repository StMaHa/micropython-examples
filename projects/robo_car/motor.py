from machine import Pin
from time import sleep

PIN_MOTOR_A_1 = 16
PIN_MOTOR_A_2 = 17

motor_a_1 = Pin(PIN_MOTOR_A_1, Pin.OUT)
motor_a_2 = Pin(PIN_MOTOR_A_2, Pin.OUT)

for i in range(0, 5):
    motor_a_1.on()
    motor_a_2.off()
    sleep(2)
    motor_a_1.off()
    motor_a_2.on()
    sleep(2)

motor_a_1.off()
motor_a_2.off()
