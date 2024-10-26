# RoboCar

**Micropython project to program a 2WD robo car.**  
Car with 2 wheels drives without hitting obstacles.  
An ultrasonic sensor measures the distance to obstacles.  
If the distance to the obstacle is too short, the robo stops,  
turns into random direction and continues driving if no obstacle  
is detected.

Needed parts:
- 2WD Robot Car
- Motor driver for 2 motors (e.g. L298N)
- Ultrasonic sensor HC-SR04 (incl. level shifter) or HC-SR04P (3.3V)
- Raspberry Pi Pico
- Batteries (maybe 5V voltage regulator)

Copy needed files to root directory of the Micropython board:
- main.py
- robo_car.py (for exercises: robo_car_1.py, robo_car_2.py, robo_car_3.py)

Features which are possibly used by the robo can be tested separately by  
the following examples:  
- ultrasonic-sensor.py
- servo-control.py
- led-blink.py
- button-switch.py
- analog-input.py

These examples cover the basic IOs of a microcontroller like the Raspberry Pi Pico.  

The folder 'using_modules' contains an extended version of this project that  
uses modules to control the motors and access the ultrasonic sensor.

# LICENSE
See the [LICENSE](../../LICENSE) file for license rights and limitations.
Submodules might have a different license.
