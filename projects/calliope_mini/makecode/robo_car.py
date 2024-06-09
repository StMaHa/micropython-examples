# Motorenleistung/Geschwindigkeit, anpassen für Geradeauslauf
speed_m1 = 700
speed_m2 = 700
speed_max = 1023

# GPIOs zur Ansteuerung der Motoren
pin_m1a = AnalogPin.P0  # motor 1
pin_m1b = AnalogPin.P1  # motor 1
pin_m2a = AnalogPin.P2  # motor 2
pin_m2b = AnalogPin.P3  # motor 2
# GPIOs des Abstandssensors
pin_trigger = DigitalPin.P17
pin_echo = DigitalPin.P16

serial.redirect_to_usb()
serial.set_baud_rate(BaudRate.BAUD_RATE115200)

class HCSR04:
    # echo_timeout_us is based in chip range limit (400cm)
    def __init__(self, trigger_pin, echo_pin, timeout_us=30000):  # timeout_us = 30000 = 500cm * 2 * 30us/cm
        self.echo_timeout_us = timeout_us
        # Init trigger pin (out)
        self.trigger = trigger_pin
        pins.digital_write_pin(self.trigger, 0)
        # Init echo pin (in)
        self.echo = echo_pin

    def _send_pulse_and_wait(self):
        pins.digital_write_pin(self.trigger, 0) # Stabilize the sensor
        control.wait_micros(5)
        # Send a 10us pulse to enable ultrasonic signal.
        pins.digital_write_pin(self.trigger, 1)
        control.wait_micros(10)
        pins.digital_write_pin(self.trigger, 0)
        # Measure ultrasonic echo
        pulse_time = pins.pulse_in(self.echo, PulseValue.HIGH, self.echo_timeout_us)
        return pulse_time

    def distance_cm(self):
        pulse_time = self._send_pulse_and_wait()
        distance = -1
        if pulse_time > 0:
            distance = int((pulse_time / 2) / 29.1)
        return distance


class MotorEx:
    def __init__(self, pin1: DigitalPin, pin2: DigitalPin):
        self.pin1 = pin1
        self.pin2 = pin2

    def forward(self, speed=speed_max):
        pins.analog_write_pin(self.pin1, 0)
        pins.analog_write_pin(self.pin2, speed)

    def backward(self, speed=speed_max):
        pins.analog_write_pin(self.pin1, speed)
        pins.analog_write_pin(self.pin2, 0)

    def stop(self):
        pins.analog_write_pin(self.pin1, speed_max)
        pins.analog_write_pin(self.pin2, speed_max)


class Robo:
    def __init__(self, motor1: MotorEx, speed_motor1, motor2: MotorEx, speed_motor2):
        self.motor1 = motor1
        self.motor2 = motor2
        self.speed_m1 = speed_motor1
        self.speed_m2 = speed_motor2
        self.turn_icon = images.create_image("""
                                            . . . . .
                                            . # . # .
                                            # # # # #
                                            . # . # .
                                            . . . . .
                                            """)

    def stop(self):
        self.motor1.stop()
        self.motor2.stop()
        pause(500)

    def go(self):
        basic.show_icon(IconNames.ARROW_SOUTH)
        self.motor1.forward(self.speed_m1)
        self.motor2.forward(self.speed_m2)

    def turn(self):
        self.turn_icon.show_image(0)
        richtung = Math.random_boolean()
        if richtung:
            self.motor1.forward(self.speed_m1)
            self.motor2.backward(self.speed_m2)
        else:
            self.motor1.backward(self.speed_m1)
            self.motor2.forward(self.speed_m2)
        delay = helpers.array_pick_random([250, 500, 750])
        pause(delay)
        self.stop()


def main():
    motor1 = MotorEx(pin_m1a, pin_m1b)
    motor2 = MotorEx(pin_m2a, pin_m2b)
    robo = Robo(motor1, speed_m1, motor2, speed_m2)
    sensor = HCSR04(pin_trigger, pin_echo)

    while True:
        sensor_value = sensor.distance_cm()
        if sensor_value < 0:
                continue
        serial.write_line(str(sensor_value))

        if sensor_value < 40:
            robo.stop()
            robo.turn()
        else:
            robo.go()

main()