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
#Geschwindigkeit der Motoren
speed_m1 = 0.5
speed_m2 = 0.5

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
    # Status setzen, um den Robo anzuhalten oder zu starten
    # +++ 2) +++

# Callback-Funktion zum Beenden des Robo-Programms
# Ausgeloest durch einen langen Tastendruck
def deactivate_robo():
    global exit_status
    # Status wechseln, um das Robo-Programm zu beenden
    # +++ 2) +++

# Hier bgeinnt das Hauptprogramm
if __name__ == '__main__':
    # Erzeugen einer Instanz der Pin-Factory
    # +++ 1) oder 2) +++

    # Erzeugen einer Instanz der Motor-Klasse
    # aktivieren von PWM and zuweisen der Pin-Factory
    # +++ 3) +++

    # Erzeugen einer Instanz der Distanzsensor-Klasse
    # +++ 1) +++

    # Erzeugen einer Instanz der Button-Klasse
    # aktivieren des Pull-up Widerstands, definieren der Haltezeit fuer langen Tastendruck
    # +++ 2) +++

    # Erzeugen einer Instanz der LED-Klasse, zuweisen der Pin-Factory
    # +++ 2) +++

    # Der Button-Instanz die Callback-Funktion fuer einfachen Tastendruck zuweisen
    # +++ 2) +++
    # Der Button-Instanz die Callback-Funktion fuer langen Tastendruck zuweisen
    # +++ 2) +++

    # Try-Catch-Block
    try:
        # Schleife so lange durchlaufen bis das Programm beendet wird (langer Tastendruck)
        while not exit_status:
            # Schreibe Sensormesswert (cm) auf die Konsole (kann spaeter wieder auskommentiert werden)
            # +++ 1) +++

            # Wie ist der Programmstatus? Wecchseln durch Tastendruck
            if run_status:
                # wenn Robo faehrt
                # LED dauerhaft einschalten
                # +++ 2) +++

                # Ist der Sensormesswert (cm) kleiner 40 cm?
                # +++ 4) +++
                distance_cm = 100  # messe Entfernung
                if distance_cm < 40:
                    # alle Motoren stop
                    # +++ 4) +++

                    # eine 1/2 Sekunde warten
                    sleep(0.5)
                    # Waehle zufaellig eine Drehrichtung
                    #if choice([0, 1]):   # +++ 4) +++ einkommentieren
                        # Robo dreht mit 1/2 Leistung in die eine Richtung
                        # +++ 4) +++

                    #else:   # +++ 4) +++ einkommentieren
                        # Robo dreht mit 1/2 Leistung in die andere Richtung
                        # +++ 4) +++

                    # Lass den Robo eine 1/2 Sekunde drehen
                    sleep(0.5)
                    # alle Motoren stop
                    # +++ 4) +++

                    # eine 1/2 Sekunde warten
                    sleep(0.5)
                #else:   # +++ 3) +++ einkommentieren
                    # fahre Robo mit 1/2 Leistung vorwaerts
                    # +++ 3) +++

            else:
                # wenn Robo haelt
                # alle Motoren stop
                # +++ 3) +++

                # LED wechselt bei jedem Schleifen druchlauf den Zustand, sie blinkt
                # LED wechselt ihren Zustand
                # +++ 2) +++

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
