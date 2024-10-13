from machine import Pin, ADC
from time import sleep

PIN_LED = 2
PIN_ANALOG = 26

led = Pin(PIN_LED, Pin.OUT)
photo_resistor = ADC(Pin(PIN_ANALOG))

while True:
    analog_value = photo_resistor.read_u16()
    print(analog_value)
    if analog_value < 20000:
        led.on()
    else:
       led.off()
    sleep(0.5)

    
    
