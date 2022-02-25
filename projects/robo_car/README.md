# Example and exercise to build a robot car
(2WD Smart Robot Car Chassis)

# Python
## Example using *RPi.GPIO* (robocar-rpigpio.py)
## Exercise using *gpiozero* (robocar-gpiozero_1.py)
Python script uses daemon of *pigpio*, therefore start daemon *pigpiod*:\
(Enable daemon *pigpiod* to start automatically at system start.)
```
$ sudo systemctl start pigpiod
$ sudo systemctl enable pigpiod
$ python3 motor_pwm.py
```

# LICENSE
See the [LICENSE](../LICENSE.md) file for license rights and limitations.
