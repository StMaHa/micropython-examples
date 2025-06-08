from machine import Pin, ADC
from time import sleep

IO_LED = 2
IO_LDR = 26

led = Pin(IO_LED, Pin.OUT)
ldr = ADC(Pin(IO_LDR))

while True:
    ldr_adc_value = ldr.read_u16()
    ldr_voltage = ldr_adc_value * 3.3 / 65535
    print(ldr_adc_value, ldr_voltage)
    if ldr_voltage > 2.5:
        led.on()
    else:
       led.off()
    sleep(0.5)

    
    
