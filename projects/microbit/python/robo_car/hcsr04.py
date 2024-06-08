from microbit import *
from machine import time_pulse_us

class HCSR04:
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin, echo_pin, timeout_us=30000):  # timeout_us = 30000 = 500cm * 2 * 30us/cm
        self.echo_timeout_us = timeout_us
        # Init trigger pin (out)
        self.trigger_pin = trigger_pin
        self.trigger_pin.write_digital(0)
        # Init echo pin (in)
        self.echo_pin = echo_pin

    def _send_pulse_and_wait(self):
        self.trigger_pin.write_digital(0) # Stabilize the sensor
        sleep(0.005)
        # Send a 10us pulse to enable ultrasonic signal.
        self.trigger_pin.write_digital(1)
        sleep(0.01)
        self.trigger_pin.write_digital(0)
        # Measure ultrasonic echo
        pulse_time = time_pulse_us(self.echo_pin, 1, self.echo_timeout_us)
        if pulse_time <= 0:
            MAX_RANGE_IN_CM = 500 # it's really ~400, but I've read people say they see it working up to ~460
            pulse_time = int(MAX_RANGE_IN_CM * 29.1) # 1cm each 29.1us
        return pulse_time

    def distance_cm(self):
        pulse_time = self._send_pulse_and_wait()
        distance = (pulse_time / 2) / 29.1
        return distance