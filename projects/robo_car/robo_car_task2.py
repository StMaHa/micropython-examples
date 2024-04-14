# Aufgaben
# +++ 1) Messen mit dem Ultraschallentfernungssensor „HC-SR04“ in einer Dauerschleife
# +++ 2) Start / Stop der Motoren in Abhängigkeit der Entfernung
# +++ 3) Zufälliges drehen des Robos nach links oder rechts

# Bibliotheken und Klassen
import os
import sys

from machine import Pin
from time import sleep
from random import choice

from hcsr04 import HCSR04
from motor import Motor

# Globale Variablen

# Motorenleistung
speed_m1 = 0.5
speed_m2 = 0.5

board_name = os.uname().sysname.strip().lower()
print("Micropython board:", board_name)

# Definitionen der GPIOs
if board_name == 'rp2':
    # Pinnummern beziehen sich auf Raspberry Pi Pico
    # GPIOs zur Ansteuerung der Motoren
    pin_m1a = 12  # motor 1
    pin_m1b = 13  # motor 1
    pin_m2a = 14  # motor 2
    pin_m2b = 15  # motor 2
    # GPIOs des Abstandssensors
    pin_trigger = 1
    pin_echo = 0
elif board_name == 'esp32':
    # Pinnummern beziehen sich auf Wemos S2 mini
    # GPIOs zur Ansteuerung der Motoren
    pin_m1a = 37  # motor 1
    pin_m1b = 38  # motor 1
    pin_m2a = 39  # motor 2
    pin_m2b = 40  # motor 2
    # GPIOs des Abstandssensors
    pin_trigger = 17
    pin_echo = 16
else:
    print("Pins sind für dieses Micropython board nicht definiert: ", board_name)
    sys.exit()

# Hier bgeinnt das Hauptprogramm
def start():
    # Erzeuge eine Instanz der Motor-Klasse
    # aktivieren von PWM
    motor1 = Motor(pin_m1a, pin_m1b, pwm=True)
    motor2 = Motor(pin_m2a, pin_m2b, pwm=True)

    # Erzeuge eine Instanz der Distanzsensor-Klasse
    sensor = HCSR04(trigger_pin=pin_trigger, echo_pin=pin_echo, echo_timeout_us=10000)

    # Try-Catch-Block
    try:
        print("Robo started...")
        # +++ 1) +++
        # Endlosschleife...
        # Schreibe Sensormesswert (cm) auf die Konsole (kann spaeter wieder auskommentiert werden)
        while True:
            # Schreibe Sensormesswert (cm) auf die Konsole (kann spaeter wieder auskommentiert werden)
            # +++ 2) +++ Auskommentieren
            print(sensor.distance_cm())

            # +++ 2) +++
            # Messe Entfernung und starte bzw. stoppe die Motoren
            # Ist der Sensormesswert (cm) kleiner 40 cm?

                # +++ 2) +++
                # alle Motoren stop wenn Sensorwert (cm) kleiner als 40 cm


                # +++ 2) +++
                # eine 1/2 Sekunde warten

                # +++ 3) +++
                # Waehle zufaellig eine Drehrichtung

                    # Robo dreht in die eine Richtung



                    # Robo dreht in die andere Richtung


                # Lass den Robo eine 1/2 Sekunde drehen

                # alle Motoren stop


                # eine 1/2 Sekunde warten


                # +++ 2) +++
                # Andernfalls fahre Robo vorwaerts (Sensorwert (cm) kleiner als 40 cm)


    # Fangen eines Fehlers/Signals
    except KeyboardInterrupt:
        print("Programm abgebrochen.")
    # Dieser Block wird immer ausgefuehrt: zum Schluss muss man aufraeumen
    finally:
        # Motoren aus
        motor1.stop()
        motor2.stop()
        print("Programm beendet.")

# Manuelles Ausführen in der IDE
if __name__ == '__main__':
    start()
