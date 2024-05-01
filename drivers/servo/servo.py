from machine import Pin, PWM
from time import sleep

#
# Python module for Servo
#
class Servo:

    def __init__(self, pin_gpio,  # gpio pin of micropython board
                 frequency=50,    # standard frequency for servos
                 servo_min_pulse_width=0.001, servo_max_pulse_width=0.002,  # standard values for servos
                 servo_min_angle=0, servo_max_angle=180):
        "Init method / constructor of Servo class"
        self._logging = False
        self._frequency = frequency
        self._servo_max_pulse_width = servo_max_pulse_width
        self._servo_min_pulse_width = servo_min_pulse_width
        self._servo_max_angle = servo_max_angle
        self._servo_min_angle = servo_min_angle
        # Prepare servo angle calculation (based on y = m * x + b -> pulse = m * angle + b)
        #   servo_min_pulse_width = m * servo_min_angle + b
        #   servo_max_pulse_width = m * servo_max_angle + b
        # Calculate servo pulse per angle: m = (pulse1 - pulse2) / (angle1 - angle2)
        self._servo_pulse_per_angle = (self._servo_max_pulse_width - self._servo_min_pulse_width) / (self._servo_max_angle - self._servo_min_angle)
        # Calculate servo pulse offset: b = pulse2 - m * angle2
        self._servo_pulse_offset = self._servo_max_pulse_width - self._servo_pulse_per_angle * self._servo_max_angle
        # Initialize PWM
        self.__pin = Pin(pin_gpio)
        self._servo = PWM(self.__pin, freq=self._frequency)
        

    def _log(self, text):
        "Writes text to console"
        if self._logging:
            print(text)

    def enable_logging(self, enable=True):
        "Enables/disable logging"
        self._logging = enable

    def frequency(self, frequency):
        "Changes the PWM frequency"
        self._frequency = frequency
        self._servo.freq(frequency)  

    def angle(self, angle):
        "Changes servo angle"
        if(angle < self._servo_min_angle or angle > self._servo_max_angle):
            raise ValueError("Angle is out of range. Should be between {} and {} degree.".format(self._servo_min_angle, self._servo_max_angle))
        # Calculate duty cycle
        pulse = self._servo_pulse_per_angle * angle + self._servo_pulse_offset  # calculate pulse width in ns: y = mx + b 
        period = 1 / self._frequency  # period in seconds
        duty_cycle = 100 * pulse / period  # duty cycle in percentage
        self._log("Duty cylce in percentage [%]: " + str(duty_cycle))
        duty_cycle_ns = int(1000000000 * period * duty_cycle / 100)
        self._servo.duty_ns(duty_cycle_ns)

    def stop(self):
        "Stops PWM output"
        self._servo.deinit()


if __name__ == '__main__':
    print("This module is library only!")
