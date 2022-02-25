# Aufgaben
#
# +++ 1) +++
# Messen mit einem Ultraschallentfernungssensor (HC-SR04).
#   Hilfe? Suchen im Internet: HC-RS04 gpiozero
# +++ 2) +++
# Ansteuerung einer LED mit Taster. (LED leuchtet -> Robo faehrt, LED blinkt -> Robo im Stand-By)
#   Hilfe? Suchen im Internet: LED gpiozero, BUTTON gpiozero
# +++ 3) +++
# Ansteuerung der Motoren
#   Hilfe? Suchen im Internet: MOTOR gpiozero
# +++ 4) +++
# Ansteuerung der Motoren in Abhaengigkeit der Entfernung

# Bibliotheken und Klassen
from gpiozero import LED, Button, DistanceSensor, Motor
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
from random import choice

# Globale Variablen
# GPIOs zur Ansteuerung der Motoren
pin_m1a = 16  # motor 1
pin_m1b = 20  # motor 1
pin_m2a = 19  # motor 2
pin_m2b = 26  # motor 2
# GPIOs des Abstanzsensors
pin_trigger = 24
pin_echo = 23
# GPIO der Status-LED
pin_status = 17
# GPIO des Tasters
pin_button = 25
# Programmsteuerung
exit_status = False
run_status = False

# Callback-Funktion zum aendern des Roboterstatus (start/stop)
# Ausgeloest durch einen einfachen Tastendruck
def start_stop_robo():
    global run_status
    # Status wechseln, um das Robo-Programm zu beenden
    # +++ 2) +++
    run_status = not run_status

# Callback-Funktion zum Beenden des Robo-Programms
# Ausgeloest durch einen langen Tastendruck
def deactivate_robo():
    global exit_status
    # Status setzen, um den Robo anzuhalten oder zu starten
    # +++ 2) +++
    exit_status = True

# Hier bgeinnt das Hauptprogramm
if __name__ == '__main__':
    # Erzeugen einer Instanz der Pin-Factory
    # +++ 1) oder 2) +++
    factory = PiGPIOFactory()

    # Erzeugen einer Instanz der Motor-Klasse
    # aktivieren von PWM and zuweisen der Pin-Factory
    # +++ 3) +++
    motor1 = Motor(pin_m1a, pin_m1b, pwm=True, pin_factory = factory)
    motor2 = Motor(pin_m2a, pin_m2b, pwm=True, pin_factory = factory)

    # Erzeugen einer Instanz der Distanzsensor-Klasse
    # +++ 1) +++
    sensor = DistanceSensor(echo = pin_echo, trigger = pin_trigger, pin_factory = factory)

    # Erzeugen einer Instanz der Button-Klasse
    # aktivieren des Pull-up Widerstands, definieren des Haltezeit und zuweisen der Pin-Factory
    # +++ 2) +++
    button = Button(pin_button, pull_up = True, hold_time = 2, pin_factory = factory)

    # Erzeugen einer Instanz der LED-Klasse, zuweisen der Pin-Factory
    # +++ 2) +++
    led = LED(pin_status, pin_factory = factory)

    # Der Button-Instanz die Callback-Funktion fuer einfachen Tastendruck zuweisen
    # +++ 2) +++
    button.when_pressed = start_stop_robo
    # Der Button-Instanz die Callback-Funktion fuer langen Tastendruck zuweisen
    # +++ 2) +++
    button.when_held = deactivate_robo

    # Try-Catch-Block
    try:
        # Schleife so lange durchlaufen bis das Programm beendet wird (langer Tastendruck)
        while not exit_status:
            # Schreibe Sensormesswert (cm) auf die Konsole (kann spaeter wieder auskommentiert werden)
            # +++ 1) +++
            #print(sensor.distance * 100)

            # Wie ist der Programmstatus? Wecchseln durch Tastendruck
            if run_status:
                # wenn Robo faehrt
                # LED dauerhaft einschalten
                # +++ 2) +++
                led.on()
                # Ist der Sensormesswert (cm) kleiner 40 cm?
                # +++ 4) +++
                distance_cm = sensor.distance * 100  # messe Entfernung
                if distance_cm < 40:
                    # alle Motoren stop
                    # +++ 4) +++
                    motor1.stop()
                    motor2.stop()
                    # eine 1/2 Sekunde warten
                    sleep(0.5)
                    # Waehle zufaellig eine Drehrichtung
                    if choice([0, 1]):   # +++ 4) +++ einkommentieren
                        # Robo dreht mit 1/2 Leistung in die eine Richtung
                        # +++ 4) +++
                        motor1.forward(0.5)
                        motor2.backward(0.5)
                    else:   # +++ 4) +++ einkommentieren
                        # Robo dreht mit 1/2 Leistung in die andere Richtung
                        # +++ 4) +++
                        motor1.backward(0.5)
                        motor2.forward(0.5)
                    # Lass den Robo eine 1/2 Sekunde drehen
                    sleep(0.5)
                    # alle Motoren stop
                    # +++ 4) +++
                    motor1.value = 0
                    motor2.value = 0
                    # eine 1/2 Sekunde warten
                    sleep(0.5)
                else:   # +++ 3) +++ einkommentieren
                    # fahre Robo mit 1/2 Leistung vorwaerts
                    # +++ 3) +++
                    motor1.forward(0.5)
                    motor2.forward(0.5)
            else:
                # wenn Robo haelt
                # alle Motoren stop
                # +++ 3) +++
                motor1.stop()
                motor2.stop()
                # LED wechselt bei jedem Schleifen druchlauf den Zustand, sie blinkt
                # LED wechselt ihren Zustand
                # +++ 2) +++
                led.toggle()
                # eine 1/2 Sekunde warten
                sleep(0.5)
    # Fangen eines Fehlers/Signals
    except KeyboardInterrupt:
        print("Programm abgebrochen.")
    # Dieser Block wird immer ausgefuehrt: zum Schluss muss man aufraeumen
    finally:
        # LED aus
        led.off()
        # Motoren aus
        motor1.stop()
        motor2.stop()
        print("Programm beendet.")
