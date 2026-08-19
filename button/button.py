from machine import Pin

IO_LED = 2
IO_BUTTON = 4 

led = Pin(IO_LED, Pin.OUT)
button = Pin(IO_BUTTON, Pin.IN, Pin.PULL_UP)

while True:
    if button.value() == False:  # Taster gedrueckt, Signal ist '0' / GND
        led.on()
    else:
        led.off()