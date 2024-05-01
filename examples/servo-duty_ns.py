from machine import Pin, PWM
from time import sleep

servo_gpio = 28  # LED at GPIO28
servo = Pin(servo_gpio)
servo_pwm = PWM(servo)
servo_pwm.freq(50)  # 20 ms = 20000 us = 20000000 ns
# Servo standard values
servo_left = 1000000  # 5% of 20000000 ns
servo_mid = 1500000  # 7.5% of 20000000 ns
servo_right = 2000000  # 10% of 20000000 ns

print("Servo turning...")
led_duty_list = [servo_left, servo_mid, servo_right, servo_mid]
try:
    while True:
        for duty in led_duty_list:
            servo_pwm.duty_ns(duty)
            sleep(1)
except KeyboardInterrupt:
    print("Program aborted.")
    servo_pwm.duty_ns(servo_mid)
    servo_pwm.deinit()