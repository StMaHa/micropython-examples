from machine import Pin
from time import sleep

PIN_LED = 2

led = Pin(PIN_LED, Pin.OUT)

for i in range(0, 10):
    led.on()
    sleep(1)
    led.off()
    sleep(1)


