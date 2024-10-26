"""
Projekt für ein Roboter Workshop
Auto mit 2 Rädern faehrt ohne gegen Hindernisse zu stossen.
Ein Ultraschallsensor misst die Entfernung zu Hindernissen.
Bei zu geringem Abstand zum Hindernis haelt der Robo, dreht
in eine beliebige Richtung und faehrt weiter wenn kein Hindernis
in der Naehe.
Benoetigte Teile:
- 2WD Robot Car
- Motortreiber für 2 Motoren
- Ultraschallsensor HC-SR04P (3.3V) oder HC-SR04 (inkl. Levelshifter)
- Raspberry Pi Pico
- Batterien (5V Spannungsregler)
"""
# Aufgaben
# +++ 1) Messen mit dem Ultraschallentfernungssensor „HC-SR04“ in einer Dauerschleife
# +++ 2) Start / Stop der Motoren in Abhängigkeit der Entfernung
# +++ 3) Zufälliges drehen des Robos nach links oder rechts

# Micropython Bibliotheken und Klassen
import os   # Betriebssystem Funktionen, z.B. uname(), Infos zum Micropython board
import sys  # System Funktionen, z.B. exit()

from machine import Pin            # Pin-Klasse
from machine import PWM            # PWM-Klasse
from machine import time_pulse_us  # Funktion um Echopuls zu messen
from time import sleep             # Verzoegerung in Sekunden
from random import choice          # Zufallswahl
from utime import sleep_us         # Verzoegerung in Mikrosekunden

# Konstanten

# GPIOs des Abstandssensors
DISTANCE_TIME_OF_SOUND_AT_CM = 29.1
DISTANCE_MAX_RANGE_IN_CM = 500
DISTANCE_ECHO_PIN = 10
DISTANCE_TRIGGER_PIN = 11
DISTANCE_ECHO_TIMEOUT_US = int(DISTANCE_MAX_RANGE_IN_CM*2*DISTANCE_TIME_OF_SOUND_AT_CM)
# Motorenleistung/Geschwindigkeit, anpassen für Geradeauslauf
MOTOR_PWM_MAX_DUTY_CYLCE = 65535
MOTOR_PWM_FREQUENCY = 500
MOTOR_SPEED_1 = 0.5
MOTOR_SPEED_2 = 0.55
MOTOR_LINE_1A_PIN = 16  # Motor 1
MOTOR_LINE_1B_PIN = 17  # Motor 1
MOTOR_LINE_2A_PIN = 18  # Motor 2
MOTOR_LINE_2B_PIN = 19  # Motor 2
# Status LED
LED_ONBOARD_PIN = 25
# Servo
SERVO_PIN = 0
SERVO_MID = 1300000  # 1350000 ns = 1350 us = 1.35 ms
SERVO_MIN = 800000   # 800000 ns = 800 us = 0.8 ms
SERVO_MAX = 1900000  # 1900000 ns = 1900 us = 1.9 ms

# Globale Variablen

board_name = os.uname().sysname.strip().lower()
print("Micropython board:", board_name)

# Initialisiere IOs
motor_line_1a = PWM(Pin(MOTOR_LINE_1A_PIN, Pin.OUT), freq=MOTOR_PWM_FREQUENCY, duty_u16=0)
motor_line_1b = PWM(Pin(MOTOR_LINE_1B_PIN, Pin.OUT), freq=MOTOR_PWM_FREQUENCY, duty_u16=0)
motor_line_2a = PWM(Pin(MOTOR_LINE_2A_PIN, Pin.OUT), freq=MOTOR_PWM_FREQUENCY, duty_u16=0)
motor_line_2b = PWM(Pin(MOTOR_LINE_2B_PIN, Pin.OUT), freq=MOTOR_PWM_FREQUENCY, duty_u16=0)

distance_trigger = Pin(DISTANCE_TRIGGER_PIN, mode=Pin.OUT)
distance_echo = Pin(DISTANCE_ECHO_PIN, mode=Pin.IN, pull=Pin.PULL_DOWN)

# Erzeuge Instanzen der Motor-Klasse
led = Pin(LED_ONBOARD_PIN, Pin.OUT)

# Funktionen

# Demo-Funktion zum Steuern eines Servos (Optional)
def servo_turn():
    servo = PWM(Pin(SERVO_PIN), freq=50)
    servo.duty_ns(SERVO_MIN)
    sleep(1)
    servo.duty_ns(SERVO_MAX)
    sleep(1)
    servo.duty_ns(SERVO_MID)
    sleep(1)
    servo.deinit()

# Funktionen zum Steuern des Robos
def motor_forward(pin1, pin2, speed):
    pin1.duty_u16(0)
    pin2.duty_u16(int(MOTOR_PWM_MAX_DUTY_CYLCE * speed))  # Type cast zu Integer, variable speed ist vom typ Float


def motor_backward(pin1, pin2, speed):
    pin1.duty_u16(int(MOTOR_PWM_MAX_DUTY_CYLCE * speed))  # Type cast zu Integer, variable speed ist vom typ Float
    pin2.duty_u16(0)


def motor_stop(pin1, pin2):
    pin1.duty_u16(0)
    pin2.duty_u16(0)


def robo_stop():
    """ Stoppt das Roboter Auto """
    # +++ 2) +++ alle Motoren stop 


    # eine 1/2 Sekunde warten
    sleep(0.5)


def robo_go():
    """ Faehrt Roboter Auto forwaerts """
    # Fahre Robo vorwaerts
    motor_forward(motor_line_1a, motor_line_1b, MOTOR_SPEED_1)
    motor_forward(motor_line_2a, motor_line_2b, MOTOR_SPEED_2)


def robo_turn():
    """ Dreht Roboter in eine zufaellige Richtung """
    # servo_turn()  # Einkommentieren um einen Servo anzusteuern
    # +++ 3) +++ Drehe Robo in ein beliebige Richtung
    # Waehle zufaellig eine Drehrichtung
    richtung = 1
    if richtung:
        # Robo dreht in die eine Richtung
        motor_forward(motor_line_1a, motor_line_1b, MOTOR_SPEED_1)
        motor_backward(motor_line_2a, motor_line_2b, MOTOR_SPEED_2)

        # Robo dreht in die andere Richtung


    # Lass den Robo eine 1/4, 1/2 oder 3/4  Sekunde drehen
    delay = choice([0.25, 0.5, 0.75]) 
    sleep(delay)
    # alle Motoren stop
    robo_stop()

# Funktion zum Messen der netfernung mit einem Ultraschallsensors
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

# Hier beginnt das Hauptprogramm
def start():
    """ Startet Roboter Auto """
    # Try-Catch-Block
    try:
        print("Robo faehrt...")
        led.on()
        # servo_turn()  # Einkommentieren um einen Servo anzusteuern
        # Endlosschleife...
        while True:
            # +++ 1) +++ Schreibe Entfernung (cm) auf die Konsole
            distance = get_distance()
            if distance >= DISTANCE_MAX_RANGE_IN_CM:  # ignoriere Fehlmessung
                continue


            # +++ 2) +++
            # Ist die Entfernung (cm) kleiner 40 cm?

                # +++ 2) +++
                # Alle Motoren stop wenn Entfernung (cm) kleiner als 40 cm

                # +++ 3) +++
                # Drehe Robo in ein beliebige Richtung


                # +++ 2) +++
                # Andernfalls fahre Robo vorwaerts (Sensorwert (cm) kleiner als 40 cm)

            sleep(0.1)  # Wartezeit zwischen Entfernungsmessungen
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
