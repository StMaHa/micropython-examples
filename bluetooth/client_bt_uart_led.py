import serial
import time
import os
import platform
import sys
'''
Connect to the BT-UART adapter

Windows:
- Get corresponding COM ports from Windows device manager
- List outgoing COM ports
Get-WmiObject Win32_PnPEntity |
Where-Object { $_.Name -like "*Bluetooth*" -and $_.Name -like "*COM*" -and $_.DeviceID -notlike "*LOCALMFG&0000*" } |
Select-Object Name, DeviceID

Linux:
- Setup outgoing Bluetooth serial device
pi@rpi:~/ bluetoothctl
> scan on
> pair XX:XX:XX:XX:XX:XX
> trust XX:XX:XX:XX:XX:XX
> connect XX:XX:XX:XX:XX:XX
> exit
sudo rfcomm bind 0 XX:XX:XX:XX:XX:XX
- Usually /dev/rfcomm0 after binding
'''
# Change to your outgoing COM port
PORT_WINDOWS = "COM5"        # Example: COM5 (Outgoing)
PORT_LINUX = "/dev/rfcomm0"
BAUD = 9600                  # Match your UART baud rate

if platform.system().lower() == "windows":
    port = PORT_WINDOWS
elif platform.system().lower() == "linux"
    port = PORT_LINUX
    # Check if device exists
    if not os.path.exists(port):
        print(f"Error! {port} not found. Did you bind the Bluetooth device?")
        print("Example: sudo rfcomm bind 0 XX:XX:XX:XX:XX:XX")
        sys.exit(1)
else:
    print(f"Error! Operating system '{platform.system()}' is not supported.")
    sys.exit(1)

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
    print(f"Connected to {PORT} at {BAUD} baud.")

    while True:
        for state in (b"on\n", b"off\n"):
            print(f"LED {state.decode().strip()}")
            ser.write(state)
            time.sleep(0.1)
            response = ser.readline().decode(errors="replace").strip()
            if response:
                print(f"RX: {response}")
            time.sleep(0.9)
except serial.SerialException as e:
    print(f"Serial error: {e}")
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Connection closed.")
