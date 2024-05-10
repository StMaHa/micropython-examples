# MicroPython

### How to get ALL sources from this git repository
```
git clone --recurse-submodules https://github.com/StMaHa/micropython-examples.git
```
If you miss to get the submodules, because you just cloned this repository...  
Change into directory 'micropython-examples'...
```
cd micropython-examples
git submodule update --init --recursive
```

### Flash MicroPython to Controller
!!! Flashing by calling esptool with not sufficiant argumnets or by using thonny might result in failing controller functions !!!

- **ESP8266** *(example on Linux OS)*
    - python esptool.py --chip=esp8266 --port=/dev/ttyUSB0 erase_flash
    - python esptool.py --chip=esp8266 --port=/dev/ttyUSB0 write_flash --flash_mode=dio --flash_size=4MB --flash_freq=keep 0x0 esp8266-xxx.bin

- **Wemos Lolin S2 mini - ESP32 S2** *(example on Windows OS using serial port COM7)*
    - python esptool.py --chip esp32s2 --port COM7 erase_flash
    - python esptool.py --chip esp32s2 --port COM7 write_flash -z 0x1000 LOLIN_S2_MINI-20240222-v1.22.2.bin

- **Raspberry Pi Pico - RP2040**
    - Press and hold Button 'BOOTSEL' while connecting to USB
    - An explorer window will open up
    - Copy the uf2 file (RPI_PICO-20240222-v1.22.2.uf2) into this explorer window
    - The explorer window will close instantly


# LICENSE
See the [LICENSE](LICENSE) file for license rights and limitations.
Submodules might have a different license.
