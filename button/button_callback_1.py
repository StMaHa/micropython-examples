from button.button_callback_2 import PIN_BUTTON
from machine import Pin
from time import sleep

# Pins of Raspberry Pi Pico
GPIO_BUTTON = 4  # GP4
GPIO_LED = 2     # GP2

button = Pin(GPIO_BUTTON, Pin.IN, Pin.PULL_UP)
led = Pin(GPIO_LED, Pin.OUT)
led.off()

def button_pressed(pin):
    led.toggle()
    #sleep(1)  # ignore bounce


if __name__ == "__main__":
    print("Start program...")
    button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)
    while True:
        sleep(1)
