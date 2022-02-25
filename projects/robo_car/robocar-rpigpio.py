#!/usr/bin/python

import RPi.GPIO as GPIO
import time
import random

pin_m1a = 16
pin_m1b = 20
pin_m2a = 19
pin_m2b = 26
pin_trigger = 24
pin_echo = 23
pin_status = 17
pin_button = 25
status = False


def setup():
      GPIO.setmode(GPIO.BCM)
      GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      GPIO.setup(pin_status, GPIO.OUT)
      GPIO.setup(pin_m1a, GPIO.OUT)
      GPIO.setup(pin_m1b, GPIO.OUT)
      GPIO.setup(pin_m2a, GPIO.OUT)
      GPIO.setup(pin_m2b, GPIO.OUT)
      GPIO.setup(pin_trigger, GPIO.OUT)
      GPIO.setup(pin_echo, GPIO.IN)


def check_status():
   global status
   if status:
      if not GPIO.input(pin_button):
         status = False
         robo_stop()
         t1 = time.time()
         while(time.time() < (t1 + 3)):
            if GPIO.input(pin_button):
               return(True)
         return(False)
   else:
      while not status:
         GPIO.output(pin_status, GPIO.LOW)
         time.sleep(0.5)
         GPIO.output(pin_status, GPIO.HIGH)
         time.sleep(0.5)
         if not GPIO.input(pin_button):
            status = True
            robo_forward()
   time.sleep(0.5)
   return(True)


def measure():
      GPIO.output(pin_trigger, GPIO.LOW)
      time.sleep(0.5)
      GPIO.output(pin_trigger, GPIO.HIGH)
      time.sleep(0.00001)
      GPIO.output(pin_trigger, GPIO.LOW)
      while GPIO.input(pin_echo) == 0:
            pulse_start_time = time.time()
      while GPIO.input(pin_echo) == 1:
            pulse_end_time = time.time()
      pulse_duration = pulse_end_time - pulse_start_time
      return round(pulse_duration * 17150, 2)


def motor_right(state_pina, state_pinb):
      GPIO.output(pin_m1a, state_pina)
      GPIO.output(pin_m1b, state_pinb)

def motor_left(state_pina, state_pinb):
      GPIO.output(pin_m2a, state_pina)
      GPIO.output(pin_m2b, state_pinb)


def robo_stop():
      motor_left(GPIO.LOW, GPIO.LOW)
      motor_right(GPIO.LOW, GPIO.LOW)


def robo_forward():
      motor_left(GPIO.LOW, GPIO.HIGH)
      motor_right(GPIO.HIGH, GPIO.LOW)


def robo_turn_right():
      motor_left(GPIO.HIGH, GPIO.LOW)
      motor_right(GPIO.HIGH, GPIO.LOW)
      time.sleep(random.choice([1, 2]) * 250 / 1000)


def robo_turn_left():
      motor_left(GPIO.LOW, GPIO.HIGH)
      motor_right(GPIO.LOW, GPIO.HIGH)
      time.sleep(random.choice([1, 2]) * 250 / 1000)


if __name__ == '__main__':
    try:
        setup()
        robo_stop()
        while check_status():
            if status:
                distance = measure()
                #print(distance)
                if distance < 40 or distance > 1000:
                    robo_stop()
                    time.sleep(0.5)
                    direction = random.choice([0, 1])
                    if direction:
                        robo_turn_right()
                    else:
                        robo_turn_left()
                    time.sleep(0.5)
                robo_forward()
    except KeyboardInterrupt:
        print("Programm abgebrochen.")
    finally:
        print("Programm beendet.")
        GPIO.cleanup()
