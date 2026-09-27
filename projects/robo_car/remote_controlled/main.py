# Module
from machine import Pin, PWM, time_pulse_us, UART
from time import sleep
from utime import sleep_us
from random import choice

# Konstanten
GPIO_US_ECHO = 10
GPIO_US_TRIGGER = 11
GPIO_MOTOR_A_1 = 16  # linker Motor
GPIO_MOTOR_A_2 = 17  # linker Motor
GPIO_MOTOR_B_1 = 18  # rechter Motor
GPIO_MOTOR_B_2 = 19  # rechter Motor
MOTOR_A_SPEED = 0.7  # 90% = 90/100
MOTOR_B_SPEED = 0.7  # 90% = 90/100

MOTOR_PWM_FREQ = 500
MAX_DUTY_CYCLE = 65535  # MAX Wert von u16 (16 bit ohne Vorzeichen)

US_MAX_RANGE_CM = 400
TIME_OF_SOUND = 0.03432  # us / cm
US_ECHO_TIMEOUT = int(US_MAX_RANGE_CM * 2 / TIME_OF_SOUND)

UART_ID = 0
UART_BAUDRATE = 9600
UART_TX = 12
UART_RX = 13

# Globale Variablen / Instanzen
auto_mode = True  # Robo faehrt von alleine
echo_pin = Pin(GPIO_US_ECHO, Pin.IN)
trigger_pin = Pin(GPIO_US_TRIGGER, Pin.OUT)

motor_a_1_pin = Pin(GPIO_MOTOR_A_1, Pin.OUT)
motor_a_2_pin = Pin(GPIO_MOTOR_A_2, Pin.OUT)
motor_b_1_pin = Pin(GPIO_MOTOR_B_1, Pin.OUT)
motor_b_2_pin = Pin(GPIO_MOTOR_B_2, Pin.OUT)

motor_a_1_pwm = PWM(motor_a_1_pin, freq=MOTOR_PWM_FREQ, duty_u16=0)
motor_a_2_pwm = PWM(motor_a_2_pin, freq=MOTOR_PWM_FREQ, duty_u16=0)
motor_b_1_pwm = PWM(motor_b_1_pin, freq=MOTOR_PWM_FREQ, duty_u16=0)
motor_b_2_pwm = PWM(motor_b_2_pin, freq=MOTOR_PWM_FREQ, duty_u16=0)

# Methoden
def motor_on(motor_pwm1, motor_pwm2, speed):
    '''
    Schaltet einen Motor mit einer gegeben Geschwindigkeit ein.
    Ein Motor hat 2 Anschlüsse: motor_pwm1, motor_pwm2 
    Ist die Geschwindigkeit 0 so ist der Motor aus.
    '''
    motor_pwm1.duty_u16(int(MAX_DUTY_CYCLE * speed))
    motor_pwm2.duty_u16(0)
    
    
def robo_go():
    '''
    Schaltet beide Motoren ein und lässt den Robo vorwärts fahren.
    '''
    motor_on(motor_a_1_pwm, motor_a_2_pwm, MOTOR_A_SPEED)  # Motor A
    motor_on(motor_b_1_pwm, motor_b_2_pwm, MOTOR_B_SPEED)  # Motor B


def robo_stop():
    '''
    Schaltet beide Motoren aus und der der Robo stoppt.
    '''
    motor_on(motor_a_1_pwm, motor_a_2_pwm, 0) 
    motor_on(motor_b_1_pwm, motor_b_2_pwm, 0)
    sleep(0.5)


def robo_turn_left():
    motor_on(motor_a_2_pwm, motor_a_1_pwm, MOTOR_A_SPEED)  # Motor A
    motor_on(motor_b_1_pwm, motor_b_2_pwm, MOTOR_B_SPEED)  # Motor B


def robo_turn_right():
    motor_on(motor_a_1_pwm, motor_a_2_pwm, MOTOR_A_SPEED)  # Motor A
    motor_on(motor_b_2_pwm, motor_b_1_pwm, MOTOR_B_SPEED)  # Motor B


def robo_turn():
    '''
    Lässt beide Motoren entgegengesetzt laufen um den Robo zu drehen.
    Die Drehrichtung ist zufällig.
    Die Drehweite wird über die Zeit gesteuert.
    Die Drehweite und somit die Zeit ist zufällig.
    '''
    direction = choice([0, 1])  # List von 0 und 1, links und rechts
    if direction:
        robo_turn_left()
    else:
        robo_turn_right()
    turn_time = choice([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
    sleep(turn_time)  # Robo dreht 0.1, 0.2, 0.3, 0.4, 0.5 ODER 0.6 Sekunden...
    robo_stop()  # ... und stoppt.
        

def get_distance():
    '''
    Methode missed die Entfernung zu einem Hindernis
    und gibt die Entfernung in cm zurück.
    '''
    trigger_pin.value(0)
    sleep_us(10)
    trigger_pin.value(1)
    sleep_us(10)
    trigger_pin.value(0)
    pulse_time = time_pulse_us(echo_pin, 1, US_ECHO_TIMEOUT)
    if pulse_time <= 0:
        pulse_time = US_ECHO_TIMEOUT
    distance_cm = pulse_time / 2 * TIME_OF_SOUND
    return distance_cm

def uart_rx_idle(uart: UART):
    global auto_mode
    if uart.any() > 0:             # check if received anything
        data = uart.read()           # read from UART
        data = data.strip()          # remove white spaces and line breaks
        data = data.decode('utf-8')  # convert bytes to string as UTF-8
        data = data.lower()          # convert to lower case
        print(data)
        if data == "run":
            auto_mode = True
        if data == "sp" or data == "dn" or data == "connected":
            robo_stop()
            auto_mode = False
        if data == "rt":
            robo_turn_right()
            auto_mode = False
        if data == "lt":
            robo_turn_left()
            auto_mode = False
        if data == "up":
            robo_go()
            auto_mode = False

try:
    bt_uart = UART(UART_ID, baudrate=UART_BAUDRATE, tx=Pin(UART_TX), rx=Pin(UART_RX))
    bt_uart.irq(handler=uart_rx_idle, trigger=UART.IRQ_RXIDLE, hard=False)

    # Hauptschleife  
    while True:
        if auto_mode:
            # Messe Entfernung
            distance = get_distance()
            # Ausgabe der Entfernung in Thonny Shell
            print(distance)
            
            # Wenn Entfernung < 40 cm
            if distance < 40:
                # Stoppe Robo
                robo_stop()
                # Drehe Robo
                robo_turn()
            else:
                # Andefalls Fahre
                robo_go()
            # verlangsame Entfernungsmessung um Fehlmessungen zu verringern
            sleep(0.1)
except KeyboardInterrupt:
    robo_stop()
