"""
Projekt für ein Roboter Workshop
Auto mit 2 Rädern faehrt ohne gegen Hindernisse zu stossen.
Ein Ultraschallsensor misst die Entfernung zu Hindernissen.
Bei zu geringem Abstand zum Hindernis haelt der Robo, dreht
in eine beliebige Richtung und faehrt weiter wenn kein Hindernis
in der Naehe.
Benoetigte Teile:
- 2WD Robot Car
- Motortreiber für 2 Motore
- Ultraschallsensor HC-SR04 (inkl. Levelshifter)
- Raspberry Pi Pico / Wemos S2 mini
- Batterien (evtl. 5V Spannungsregler)
"""
# Aufgaben
# +++ 1) Messen mit dem Ultraschallentfernungssensor „HC-SR04“ in einer Dauerschleife
# +++ 2) Start / Stop der Motoren in Abhängigkeit der Entfernung
# +++ 3) Zufälliges drehen des Robos nach links oder rechts

# Micropython Bibliotheken und Klassen
import os   # Betriebssystem Funktionen, z.B. uname(), Infos zum Micropython board
import sys  # System Funktionen, z.B. exit()

from machine import Pin    # Pin-Klasse
from time import sleep     # Verzoegerung
from random import choice  # Zufallswahl

# Eigene Bibliotheken und Klassen
from hcsr04 import HCSR04  # Ultraschallsensor-Klasse
from motor import Motor    # Motor-Klasse

# Globale Variablen

# Motorenleistung/Geschwindigkeit, anpassen für Geradeauslauf
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
    # Status LED
    pin_led = 25
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
    # Status LED
    pin_led = 15
else:
    print("Pins sind für dieses Micropython board nicht definiert: ", board_name)
    sys.exit()

# Erzeuge Instanzen der Motor-Klasse (PWM aktiviert)
motor1 = Motor(pin_m1a, pin_m1b, pwm=True)
motor2 = Motor(pin_m2a, pin_m2b, pwm=True)
# Erzeuge Instanzen der Motor-Klasse
led = Pin(pin_led, Pin.OUT)

# Funktionen zum Steuern des Robos
def robo_stop():
    """ Stoppt das Roboter Auto """
    # +++ 2) +++ alle Motoren stop 


    # eine 1/2 Sekunde warten
    sleep(0.5)


def robo_go():
    """ Faehrt Roboter Auto forwaerts """
    # Fahre Robo vorwaerts
    motor1.forward(speed_m1)
    motor2.forward(speed_m2)


def robo_turn():
    """ Dreht Roboter in eine zufaellige Richtung """
    # +++ 3) +++ Drehe Robo in ein beliebige Richtung
    # Waehle zufaellig eine Drehrichtung
    richtung = 1
    if richtung:
        # Robo dreht in die eine Richtung
        motor1.forward(speed_m1)
        motor2.backward(speed_m2)

        # Robo dreht in die andere Richtung


    # Lass den Robo eine 1/4, 1/2 oder 3/4  Sekunde drehen
    delay = choice([0.25, 0.5, 0.75]) 
    sleep(delay)
    # alle Motoren stop
    robo_stop()

# Hier beginnt das Hauptprogramm
def start():
    """ Startet Roboter Auto """
    # Erzeuge eine Instanz der Distanzsensor-Klasse
    sensor = HCSR04(trigger_pin=pin_trigger, echo_pin=pin_echo, echo_timeout_us=10000)

    # Try-Catch-Block
    try:
        print("Robo faehrt...")
        led.on()
        # Endlosschleife...
        while True:
            # +++ 1) +++ Schreibe Sensormesswert (cm) auf die Konsole (kann spaeter wieder auskommentiert werden)
            sensor_value = sensor.distance_cm()


            # +++ 2) +++
            # Ist der Sensormesswert (cm) kleiner 40 cm?

                # +++ 2) +++
                # Alle Motoren stop wenn Sensorwert (cm) kleiner als 40 cm

                # +++ 3) +++
                # Drehe Robo in ein beliebige Richtung


                # +++ 2) +++
                # Andernfalls fahre Robo vorwaerts (Sensorwert (cm) kleiner als 40 cm)

    # Fangen eines Fehlers/Signals
    except KeyboardInterrupt:
        print("Programm abgebrochen.")
    # Dieser Block wird immer ausgefuehrt: zum Schluss muss man aufraeumen
    finally:
        # Motoren aus
        robo_stop()
        led.off()
        print("Programm beendet.")

# Manuelles Ausführen in der IDE
if __name__ == '__main__':
    start()
