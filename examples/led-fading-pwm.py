from machine import Pin, PWM
from time import sleep

# led_gpio = 25  # Onboard LED of Raspberry Pi Pico without Wifi
led_gpio = 2  # LED at GPIO2
led = Pin(led_gpio)
led_pwm = PWM(led)
led_pwm.freq(500)  # 2 ms = 2000 us = 2000000 ns

print("LED fading...")
led_duty_list = [0,10000, 50000, 100000, 500000, 1000000, 1500000, 2000000]
try:
    while True:
        for duty in led_duty_list:
            led_pwm.duty_ns(duty)
            sleep(0.2)
        for duty in reversed(led_duty_list):
            led_pwm.duty_ns(duty)
            sleep(0.2)
except KeyboardInterrupt:
    print("Program aborted.")
    led_pwm.duty_ns(0)
    led_pwm.deinit()
