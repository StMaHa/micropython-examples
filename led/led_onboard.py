from machine import Pin
from time import sleep

led = Pin("LED", Pin.OUT)  # Pico GPIO25, Pico W GPIO00

for i in range(0, 10):
    led.toggle()
    sleep(1)


