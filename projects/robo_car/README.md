# RoboCar

**Micropython workshop to program a 2WD robo car.**  
Car with 2 wheels drives without hitting obstacles.  
An ultrasonic sensor measures the distance to obstacles.  
If the distance to the obstacle is too short, the robo stops,  
turns into random direction and continues driving if no obstacle  
is detected.

Needed parts:
- 2WD Robot Car
- Motor driver for 2 motors (e.g. L298N)
- Ultrasonic sensor HC-SR04 (incl. levelshifter)
- Raspberry Pi Pico / Wemos S2 mini
- Batteries (maybe 5V voltage regulator)

Copy needed files to root directory of the Micropython board:
- main.py
- robo_car.py (for exercises: robo_car_1.py, robo_car_2.py, robo_car_3.py)
- drivers/motor/motor.py
- drivers/hc-sr04/hcsr04.py

# LICENSE
See the [LICENSE](../../LICENSE) file for license rights and limitations.
Submodules might have a different license.
