# Bluetooth

**Content**
- [Bluetooth Classic](#bt_classic)
- [Bluetooth Low Energy (BLE)](#ble)


<a id="bt_classic"></a>
## Bluetooth Classic

**Devices:**
- Rapsberry Pi Pico W/2W
- JDY-31
- JDY-33 (Dual-Modus Bluetooth)


### Linux as master connects to device
Setup outgoing Bluetooth serial device  
Replace XX:XX:XX:XX:XX:XX by the MAC address correspnds to the device name
```
pi@rpi:~/ bluetoothctl
> scan on
> pair XX:XX:XX:XX:XX:XX
> trust XX:XX:XX:XX:XX:XX
> connect XX:XX:XX:XX:XX:XX
> exit
sudo rfcomm bind 0 XX:XX:XX:XX:XX:XX
```


### Windows as master connects to device
Connect manually
  - Settings > Bluetooth & devices > Devices
  - Add device > Bluetooth > Show all devices

Get corresponding COM ports from Windows device manager

List **outgoing** COM ports using Powershell:
```
Get-WmiObject Win32_PnPEntity |
Where-Object { $_.Name -like "*Bluetooth*" -and $_.Name -like "*COM*" -and $_.DeviceID -notlike "*LOCALMFG&0000*" } |
Select-Object Name, DeviceID
```


## Mobile Phone (e.g. Android) as master connects to device
Connect manually  
App will use the system connection


<a id="ble"></a>
## Bluetooth Low Energy (BLE)
**Devices:**
- Raspberry Pi Pico W/2W (Onboard WIFI/BT)
- JDY-33 (Dual-Modus Bluetooth, slave only)


### Linux/Windows as master connects to device
 
Python module **bleak** is capable of connecting to BLE devices.  
https://bleak.readthedocs.io/

**Installation**
```
pip install bleak
```

## Mobile Phone (e.g. Android) as master connects to device
App might support scanning for devices

---
---
# LICENSE
See the [LICENSE](LICENSE) file for license rights and limitations.
Submodules might have a different license.
