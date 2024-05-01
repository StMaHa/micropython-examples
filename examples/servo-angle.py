from servo import Servo  # Using library from folder 'drivers'
from time import sleep

pin_gpio = 28
servo = Servo(pin_gpio, frequency=50, servo_max_pulse_width=0.0025, servo_min_pulse_width=0.00065,
              servo_min_angle=0, servo_max_angle=180)
servo.enable_logging()

servo_angle_min = 0
servo_angle_mid = 90
servo_angle_max = 180

print("Turning servo by angle...")
try:
    while True:
        for angle in [servo_angle_min, servo_angle_mid, servo_angle_max, servo_angle_mid]:
            servo.angle(angle)
            sleep(1)
except KeyboardInterrupt:
    print("Program aborted.")
    servo.angle(servo_angle_mid)
    sleep(1)
    servo.stop()
