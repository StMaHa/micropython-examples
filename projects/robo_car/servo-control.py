from machine import Pin,PWM
from time import sleep

PIN_SERVO = 0
MID = 1350000  # 1350000 ns = 1350 us = 1.35 ms
MIN = 800000   # 800000 ns = 800 us = 0.8 ms
MAX = 1900000  # 1900000 ns = 1900 us = 1.9 ms

pwm = PWM(Pin(PIN_SERVO))  # oder  PWM(Pin(PIN_SERVO), freq=50)
pwm.freq(50)  # 0.02s = 20ms = 20000us = 20000000ns

while True:
    pwm.duty_ns(MID)
    sleep(1)
    pwm.duty_ns(MIN)
    sleep(1)
    pwm.duty_ns(MID)
    sleep(1)
    pwm.duty_ns(MAX)
    sleep(1)