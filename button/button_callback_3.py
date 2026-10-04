from machine import Pin, Timer
from time import sleep

# Pins of ESP8266
#GPIO_BUTTON = 0  # D3
#GPIO_LED = 2     # D4

# Pins of ESP32
#GPIO_BUTTON = 17  # IO17
#GPIO_LED = 16     # IO16

# Pins of Raspberry Pi Pico
GPIO_BUTTON = 4  # GP4
GPIO_LED = 2     # GP2

button_busy = False

button = Pin(GPIO_BUTTON, Pin.IN, Pin.PULL_UP)
led = Pin(GPIO_LED, Pin.OUT)
led.off()

# Timer object
# release_timer = Timer(1)  # ESP32, hardware timer
release_timer = Timer(-1)   # Raspberry Pi Pico

# Timer-Callback-Funktion zum entprellen des Tasters
# Taster wird freigegeben
def release_button(timer):
    global button_busy
    print("Button released.")
    button_busy = False

# Callback-Funktion zum aendern des Roboterstatus (start/stop)
# Ausgeloest durch einen einfachen Tastendruck
def button_pressed(button):
    global button_busy
    global run_status
    global release_timer

    # Wegen dem Prellen des Tastern, muss ein wiederholtes Ausführen verhindert werden.
    if not button_busy:
        print("Button pressed.")
        # Taster gedrueckt merken
        button_busy = True
        # LED an/aus
        led.value(not led.value())
        # nach 300 ms Taster wieder freigeben
        release_timer.init(period=300, mode=Timer.ONE_SHOT, callback=release_button)  


if __name__ == "__main__":
    print("Start program...")
    button.irq(trigger=Pin.IRQ_FALLING, handler=button_pressed)
    while True:
        sleep(1)
