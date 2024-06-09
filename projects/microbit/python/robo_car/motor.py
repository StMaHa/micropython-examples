from microbit import *

speed_max = 1023

class Motor:
    def __init__(self, pin1, pin2):
        self.pin1 = pin1
        self.pin2 = pin2

    def forward(self, speed):
        self.pin1.write_analog(0)
        self.pin2.write_analog(speed)

    def backward(self, speed):
        self.pin1.write_analog(speed)
        self.pin2.write_analog(0)

    def stop(self):
        self.pin1.write_analog(speed_max)
        self.pin2.write_analog(speed_max)