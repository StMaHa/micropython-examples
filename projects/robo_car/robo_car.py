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
DISTANCE_ECHO_IO = 10
DISTANCE_TRIGGER_IO = 11
DISTANCE_ECHO_TIMEOUT_US = int(DISTANCE_MAX_RANGE_IN_CM*2*DISTANCE_TIME_OF_SOUND_AT_CM)
# Motorenleistung/Geschwindigkeit, anpassen für Geradeauslauf
MOTOR_PWM_MAX_DUTY_CYLCE = 65535
MOTOR_PWM_FREQUENCY = 500
MOTOR_1_SPEED = 0.9
MOTOR_2_SPEED = 0.9
MOTOR_1_LINE_A_IO = 16  # Motor 1
MOTOR_1_LINE_B_IO = 17  # Motor 1
MOTOR_2_LINE_A_IO = 18  # Motor 2
MOTOR_2_LINE_B_IO = 19  # Motor 2
# Status LED
LED_ONBOARD_IO = "LED"  # 25
# Servo
IO_SERVO = 0
SERVO_ANGLE_MIN = 700000   # 700000 ns = 700 us = 0.7 ms
SERVO_ANGLE_MID = 1500000  # 1500000 ns = 1500 us = 1.5 ms
SERVO_ANGLE_MAX = 2300000  # 2300000 ns = 2300 us = 2.3 ms

# Globale Variablen

board_name = os.uname().sysname.strip().lower()
print("Micropython board:", board_name)

distance_trigger = Pin(DISTANCE_TRIGGER_IO, mode=Pin.OUT)
distance_echo = Pin(DISTANCE_ECHO_IO, mode=Pin.IN, pull=Pin.PULL_UP)

# Erzeuge Instanzen der Motor-Klasse
led = Pin(LED_ONBOARD_IO, Pin.OUT)

# Funktionen

# Demo-Funktion zum Steuern eines Servos (Optional)
def servo_turn():
    servo = PWM(Pin(IO_SERVO), freq=50)
    #servo.duty_ns(SERVO_ANGLE_MIN)
    #sleep(1)
    #servo.duty_ns(SERVO_ANGLE_MAX)
    #sleep(1)
    servo.duty_ns(SERVO_ANGLE_MID)
    sleep(1)
    servo.deinit()


class Motor:
    def __init__(self, pin1, pin2, speed):
        self.speed = speed
        self.pwm_pin1 = PWM(Pin(pin1, Pin.OUT), freq=MOTOR_PWM_FREQUENCY, duty_u16=0)
        self.pwm_pin2 = PWM(Pin(pin2, Pin.OUT), freq=MOTOR_PWM_FREQUENCY, duty_u16=0)

    # Funktionen zum Steuern des Robos
    def forward(self):
        self.pwm_pin1.duty_u16(0)
        self.pwm_pin2.duty_u16(int(MOTOR_PWM_MAX_DUTY_CYLCE * self.speed))  # Type cast zu Integer, variable speed ist vom typ Float

    def backward(self):
        self.pwm_pin1.duty_u16(int(MOTOR_PWM_MAX_DUTY_CYLCE * self.speed))  # Type cast zu Integer, variable speed ist vom typ Float
        self.pwm_pin2.duty_u16(0)

    def stop(self):
        self.pwm_pin1.duty_u16(0)
        self.pwm_pin2.duty_u16(0)


class Robo:
    def __init__(self, motor1, motor2):
        self.motor1 = motor1
        self.motor2 = motor2

    def stop(self):
        """ Stoppt das Roboter Auto """
        # +++ 2) +++ alle Motoren stop 
        self.motor1.stop()
        self.motor2.stop()
        # eine 1/2 Sekunde warten
        sleep(0.5)

    def go(self):
        """ Faehrt Roboter Auto forwaerts """
        # Fahre Robo vorwaerts
        self.motor1.forward()
        self.motor2.forward()

    def turn(self):
        """ Dreht Roboter in eine zufaellige Richtung """
        # servo_turn()  # Einkommentieren um einen Servo anzusteuern
        # +++ 3) +++ Drehe Robo in ein beliebige Richtung
        # Waehle zufaellig eine Drehrichtung
        richtung = choice([0, 1])
        if richtung:
            # Robo dreht in die eine Richtung
            self.motor1.forward()
            self.motor2.backward()
        else:
            # Robo dreht in die andere Richtung
            self.motor1.backward()
            self.motor2.forward()
        # Lass den Robo eine 1/4, 1/2 oder 3/4  Sekunde drehen
        delay = choice([0.25, 0.5, 0.75]) 
        sleep(delay)
        # alle Motoren stop
        self.stop()

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
    motor1 = Motor(MOTOR_1_LINE_A_IO, MOTOR_1_LINE_B_IO, MOTOR_1_SPEED)
    motor2 = Motor(MOTOR_2_LINE_A_IO, MOTOR_2_LINE_B_IO, MOTOR_2_SPEED)
    robo = Robo(motor1, motor2)

    """ Startet Roboter Auto """
    # Try-Catch-Block
    try:
        print("Robo faehrt...")
        servo_turn()
        led.on()
        # servo_turn()  # Einkommentieren um einen Servo anzusteuern
        # Endlosschleife...
        while True:
            # +++ 1) +++ Schreibe Entfernung (cm) auf die Konsole
            distance = get_distance()
            #print(distance)

            # +++ 2) +++
            # Ist die Entfernung (cm) kleiner 40 cm?
            if distance < 40:
                # +++ 2) +++
                # Alle Motoren stop wenn Entfernung (cm) kleiner als 40 cm
                robo.stop()
                # +++ 3) +++
                # Drehe Robo in ein beliebige Richtung
                robo.turn()
            else:
                # +++ 2) +++
                # Andernfalls fahre Robo vorwaerts (Sensorwert (cm) kleiner als 40 cm)
                robo.go()
            sleep(0.1)  # Wartezeit zwischen Entfernungsmessungen
    # Fangen eines Fehlers/Signals
    except KeyboardInterrupt:
        print("Programm abgebrochen.")
    # Dieser Block wird immer ausgefuehrt: zum Schluss muss man aufraeumen
    finally:
        # Motoren aus
        robo.stop()
        led.off()
        print("Programm beendet.")

# Manuelles Ausführen in der IDE
if __name__ == '__main__':
    start()
