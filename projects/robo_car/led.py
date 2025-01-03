from machine import Pin
from time import sleep

IO_LED = 2

led = Pin(IO_LED, Pin.OUT)

for i in range(0, 10):
    led.on()
    sleep(1)
    led.off()
    sleep(1)


