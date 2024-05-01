from machine import Pin
from time import sleep

# led_gpio = 25  # Onboard LED of Raspberry Pi Pico without Wifi
led_gpio = 2  # LED at GPIO2
led = Pin(led_gpio, Pin.OUT)

print("LED blinking...")
try:
    while True:
        led.on()    
        sleep(1)
        led.off()
        sleep(1)
except KeyboardInterrupt:
    print("Program aborted.")
    led.off()
