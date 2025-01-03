from machine import Pin,PWM
from time import sleep

IO_SERVO = 0
SERVO_ANGLE_MIN = 700000   # 700000 ns = 700 us = 0.7 ms
SERVO_ANGLE_MID = 1500000  # 1500000 ns = 1500 us = 1.5 ms
SERVO_ANGLE_MAX = 2300000  # 2300000 ns = 2300 us = 2.3 ms

pwm = PWM(Pin(IO_SERVO))  # oder  PWM(Pin(PIN_SERVO), freq=50)
pwm.freq(50)  # 0.02s = 20ms = 20000us = 20000000ns

try:
    while True:
        pwm.duty_ns(SERVO_ANGLE_MID)
        sleep(1)
        pwm.duty_ns(SERVO_ANGLE_MIN)
        sleep(1)
        pwm.duty_ns(SERVO_ANGLE_MID)
        sleep(1)
        pwm.duty_ns(SERVO_ANGLE_MAX)
        sleep(1)
except:
    pwm.duty_ns(SERVO_ANGLE_MID)  # back to middle when program terminates
    sleep(1)
