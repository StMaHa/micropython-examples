# MicroPython

**Content**
- [Find released states of this git repository](#releases)
- [How to get ALL latest sources from this git repository](#git_clone)
- [Flash MicroPython to Controller](#flash)
- [Example folder](#folder)

<a id="releases"></a>
## Find released states of this git repository
As things change from time to time, certain states, such as trainings, are frozen by tags/releases.  
[Releases](https://github.com/StMaHa/micropython-examples/releases)

<a id="git_clone"></a>
## How to get ALL latest sources from this git repository
```
git clone --recurse-submodules https://github.com/StMaHa/micropython-examples.git
```
If you miss to get the submodules, because you just cloned this repository...  
Change into directory 'micropython-examples'...
```
cd micropython-examples
git submodule update --init --recursive
```
<a id="flash"></a>
## Flash MicroPython to Controller
!!! Flashing by calling esptool with not sufficiant argumnets or by using thonny might result in failing controller functions !!!

- **Raspberry Pi Pico (W/2/2W) - RP2040/RP2350**
    - Press and hold Button 'BOOTSEL' while connecting to USB
    - An explorer window will open up
    - Use Thonny to install MicroPython  
    or  
    - Copy the uf2 file (e.g. RPI_PICO-20240222-v1.22.2.uf2) into this explorer window
    - The explorer window will close instantly

- **Wemos Lolin S2 mini - ESP32 S2** *(example on Windows OS using serial port COM7)*
    - python esptool.py --chip esp32s2 --port COM7 erase_flash
    - python esptool.py --chip esp32s2 --port COM7 write_flash -z 0x1000 LOLIN_S2_MINI-20240222-v1.22.2.bin

- **ESP8266** *(example on Linux OS)*
    - python esptool.py --chip=esp8266 --port=/dev/ttyUSB0 erase_flash
    - python esptool.py --chip=esp8266 --port=/dev/ttyUSB0 write_flash --flash_mode=dio --flash_size=4MB --flash_freq=keep 0x0 esp8266-xxx.bin

<a id="folder"></a>
## Example folder

Video: 4_mecanum_wheel_demo.mp4

### analog

### bluetooth
- Control Pico (2) W from PC/Raspberry Pi via Bluetooth Low Energy (BLE) 
  - ble_uart.py: Module/library with example for Pico
  - ble_uart_client.py: Client example controlling Pico

### button
- Switching LED with a button using callback

### hcsr04
- Distance measurement with HC-SR04

### led
- Blinking LED
- Fading LED using PWM

### motor
- Example for motors and robots
  - motor.py: Module/library
  - 4_mecanum_wheel_demo.py

### servo
- Turning servo motors

### wifi
- Web server
- Wifi client setup


---
---
# LICENSE
See the [LICENSE](LICENSE) file for license rights and limitations.
Submodules might have a different license.
