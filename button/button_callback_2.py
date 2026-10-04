from machine import Pin
from time import sleep, ticks_ms, ticks_diff


DEBOUNCE_MS = 200

# Pins of Raspberry Pi Pico
GPIO_BUTTON = 4  # GP4
GPIO_LED = 2     # GP2

button = Pin(GPIO_BUTTON, Pin.IN, Pin.PULL_UP)  # GP4
led = Pin(GPIO_LED, Pin.OUT)                 # GP2
led.off()

last_press = ticks_ms()


def button_pressed(pin):
    global last_press
    now = ticks_ms()
    # ignore edges closer than DEBOUNCE_MS to the last accepted one
    if ticks_diff(now, last_press) > DEBOUNCE_MS:
        last_press = now
        led.toggle()


if __name__ == "__main__":
    print("Start program...")
    button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)
    while True:
        sleep(1)
