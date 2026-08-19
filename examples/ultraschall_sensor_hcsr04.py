from machine import Pin
from time import sleep
from hcsr04 import HCSR04


echoPin = 22
triggerPin = 21

print("Start program...")

sensor = HCSR04(trigger_pin=triggerPin, echo_pin=echoPin, echo_timeout_us=10000)

while True:
    distance = sensor.distance_cm()
    print('Distance:', distance, 'cm')
    sleep(1)

