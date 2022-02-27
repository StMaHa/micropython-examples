# MicroPython

**Flash MicroPython to Controller**<br>
!!! Flashing by calling esptool with not sufficiant argumnets or by using thonny might result in failing controller functions !!!
- ESP8266
  - esptool.py --chip=esp8266 --port=/dev/ttyUSB0 write_flash --flash_mode=dio --flash_size=4MB --flash_freq=keep 0x0 esp8266-xxx.bin
- ESP32
  - tbd
- RP2040
  - tbd

**How to get ALL sources from this git repository**
```
git clone --recurse-submodules https://github.com/StMaHa/micropython-examples.git
```

# LICENSE
See the [LICENSE](LICENSE) file for license rights and limitations.
Submodules might have a different license.
