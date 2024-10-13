from machine import Pin

PIN_LED = 2
PIN_BUTTON = 4 

led = Pin(PIN_LED, Pin.OUT)
button = Pin(PIN_BUTTON, Pin.IN, Pin.PULL_UP)

while True:
    if button.value() == False:  # Taster gedrueckt, Signal ist '0' / GND
        led.on()
    else:
        led.off()