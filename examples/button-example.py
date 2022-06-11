from machine import Pin, Timer
from time import sleep

# Pins of ESP8266
#buttonPin = 0  # D3
#ledPin = 2     # D4

# Pins of ESP32
button_pin = 17  # IO17
led_pin = 16     # IO16
button_busy = False

button = Pin(button_pin, Pin.IN, Pin.PULL_UP)
led = Pin(led_pin, Pin.OUT)
led.off()

# Timer object
release_timer = Timer(1)

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
