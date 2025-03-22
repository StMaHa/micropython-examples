# Simple robo car example

from machine import Pin            # Pin-Klasse
from machine import PWM            # PWM-Klasse
from machine import time_pulse_us  # Funktion um Echopuls zu messen
from time import sleep             # Verzoegerung in Sekunden
from random import choice          # Zufallswahl
from utime import sleep_us         # Verzoegerung in Mikrosekunden

# Konstanten
# GPIOs des Abstandssensors
DISTANCE_TIME_OF_SOUND_PER_CM = 29.1
DISTANCE_MAX_RANGE_IN_CM = 400
DISTANCE_ECHO_PIN = 10
DISTANCE_TRIGGER_PIN = 11
DISTANCE_ECHO_TIMEOUT_US = int(DISTANCE_MAX_RANGE_IN_CM*2*DISTANCE_TIME_OF_SOUND_PER_CM)
# GPIOs der Motor Pins
MOTOR_1_PIN1 = 16
MOTOR_1_PIN2 = 17
MOTOR_2_PIN1 = 18
MOTOR_2_PIN2 = 19

MOTOR_1_SPEED = 1
MOTOR_2_SPEED = 1

# Instanzen
# Instanziiere Motor 1 Pins


# Instanziiere Motor 2 Pins


# Instanziiere Sensor Pins



# Methoden / Funktionen
def motor_forward(pin1, pin2):
    pass  # dummy code
    # Motor dreht forwärts




def motor_backward(pin1, pin2):
    pass  # dummy code
    # Motor dreht rückwärts




def motor_stop(pin1, pin2):
    pass  # dummy code
    # Motor halt




def robo_go():
    pass  # dummy code
    # Motor 1 dreht forwärts

    # Motor 2 dreht forwärts



def robo_turn():
    pass  # dummy code
    # Motor 1 dreht forwärts

    # Motor 2 dreht rückwärts



def robo_stop():
    pass  # dummy code
    # Stop Motor 1

    # Stop Motor 2

    # Warte 1/2 Sekunde



def get_distance():
    pass  # dummy code
    # Setze Triggerpin definiert auf 0

    # Warte ein paar us (5us)

    # Sende Puls von 10us



    # Messe Laenge des Echopuls

    # Echopuls ist negativ bei einer fehlerhaften Messung

        # Max Wert bei Fehlmessung

    # Berechne Entfernung in cm
    # Echopuls entspricht der Zeit zum Hindernis und zurück


# Hier beginnt das Hauptprogramm
def start():
    # Endlosschleife
    while True:
        # Messe Entfernung



        # Ist die Entfernung (cm) kleiner 40 cm?

            # Alle Motoren stop wenn Entfernung (cm) kleiner als 40 cm

            # Drehe Robo in ein beliebige Richtung


            # Andernfalls fahre Robo vorwaerts (Sensorwert (cm) kleiner als 40 cm)

        sleep(0.1)  # Wartezeit zwischen Entfernungsmessungen



# Manuelles Ausführen in der IDE
if __name__ == '__main__':
    start()
