from machine import Pin            # Pin-Klasse
from machine import time_pulse_us  # Funktion um Echopuls zu messen
from time import sleep             # Verzoegerung in Sekunden
from utime import sleep_us         # Verzoegerung in Mikrosekunden

DISTANCE_TIME_OF_SOUND_AT_CM = 29.1
DISTANCE_MAX_RANGE_IN_CM = 500
DISTANCE_ECHO_PIN = 10
DISTANCE_TRIGGER_PIN = 11
DISTANCE_ECHO_TIMEOUT_US = int(DISTANCE_MAX_RANGE_IN_CM*2*DISTANCE_TIME_OF_SOUND_AT_CM)

distance_trigger = Pin(DISTANCE_TRIGGER_PIN, mode=Pin.OUT)
distance_echo = Pin(DISTANCE_ECHO_PIN, mode=Pin.IN, pull=Pin.PULL_DOWN)

def get_distance():
    distance_trigger.value(0)

    # Sende Puls von 10us
    sleep_us(5)
    distance_trigger.value(1)
    sleep_us(10)
    distance_trigger.value(0)
    # Hole Laenge des Echopuls
    pulse_time = time_pulse_us(distance_echo, 1, DISTANCE_ECHO_TIMEOUT_US)
    if pulse_time < 0:
        # Max Wert bei Fehlmessung
        pulse_time = DISTANCE_ECHO_TIMEOUT_US
    # Berechne Entfernung in cm
    distance_cm = (pulse_time / 2) / DISTANCE_TIME_OF_SOUND_AT_CM
    return distance_cm


while True:
    print(get_distance())
    sleep(0.1)