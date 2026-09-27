'''
Connect to the BT-UART adapter
- JDY-31:    BT CLassic only
- JDY-33:    BT CLassic (JDY-33-SPP) and BLE (JDY-33-BLE)

Windows:
- The outgoing Bluetooth COM port is auto-detected via WMI (see
  find_bluetooth_com_port() below), equivalent to:
Get-WmiObject Win32_PnPEntity |
Where-Object { $_.Name -like "*Bluetooth*" -and $_.Name -like "*COM*" -and $_.DeviceID -notlike "*LOCALMFG&0000*" } |
Select-Object Name, DeviceID
- The remote device's MAC address (MAC_ADDRESS below) is used to pick the
  right entry from the DeviceID (e.g. "...7&2C4CDBC8&0&E0ABAC019A95_C...")
  when more than one Bluetooth serial port is present.
- Requires: pip install wmi pywin32
- If auto-detection fails, PORT_WINDOWS below is used as a fallback.

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
import keyboard
import os
import platform
import serial
import sys
import time
import wmi

# Fallback COM port, used if auto-detection (see find_bluetooth_com_port) fails
MAC_ADDRESS = "E0ABAC019A95"  # Replace with your BT-UART device's MAC address
PORT_WINDOWS = "COM5"         # Example: COM5 (Outgoing)
PORT_LINUX = "/dev/rfcomm0"
BAUDRATE = 9600               # Match your UART baud rate

KEY_DICT = {
    # up / forward
    "up": "up",     
    "nach-oben": "up",
    # down / backward
    "down": "dn",
    "nach-unten": "dn",
    # left / turn left
    "left": "lt",   
    "nach-links": "lt",
    # right / turn right
    "right": "rt",
    "nach-rechts": "rt",
    # stop
    "end": "sp",
    "ende": "sp",
    "clear": "sp",
    "enter": "run",
    # escape / exit / cancel
    "esc": "esc"
}

serial_port = None


def find_bluetooth_com_port(mac_address=None):
    com_port = None
    normalized_mac = None

    if mac_address is None:
        mac_address = MAC_ADDRESS
    normalized_mac = mac_address.replace(":", "").upper()

    conn = wmi.WMI()
    for entry in conn.Win32_PnPEntity():
        if not entry.Name or "Bluetooth" not in entry.Name or "COM" not in entry.Name:
            continue
        if not entry.DeviceID or "LOCALMFG&0000" in entry.DeviceID:
            continue
        if normalized_mac and normalized_mac not in entry.DeviceID.upper():
            continue
        # entry.Name looks like "Standard Serial over Bluetooth link (COM5)"
        port = entry.Name.split("(COM")[1].split(")")[0]
        if port:
            com_port = f"COM{port}"
            break
        else:
            com_port = PORT_WINDOWS  # Fallback

    return com_port


def get_serial_port():
    port = None

    if platform.system().lower() == "windows":
        port = find_bluetooth_com_port(MAC_ADDRESS)
        if not port:
            print(f"Warning! No Bluetooth outgoing COM port found for MAC {MAC_ADDRESS}.")
    elif platform.system().lower() == "linux":
        port = PORT_LINUX
        # Check if device exists
        if not os.path.exists(port):
            print(f"Error! {port} not found. Did you bind the Bluetooth device?")
            print("Example: sudo rfcomm bind 0 XX:XX:XX:XX:XX:XX")
    else:
        print(f"Error! Operating system '{platform.system()}' is not supported.")

    return port


def send_command(cmd):
    global serial_port
    serial_port.write(cmd.encode())

# Key press event handler function (callback function)
def on_key_press(event):
    if event.name in KEY_DICT:
        send_command(KEY_DICT[event.name])

# Key release event handler function (callback function)
def on_key_release(event):
    global serial_port
    send_command("dn")

# Key action event handler function (callback function)
def on_key_action(event):
    if event.event_type == keyboard.KEY_DOWN:
        on_key_press(event)
    elif event.event_type == keyboard.KEY_UP:
        on_key_release(event)


def main():
    global serial_port

    try:
        port = get_serial_port()
        serial_port = serial.Serial(port, BAUDRATE, timeout=1)
        print(f"Connected to {port} at {BAUDRATE} baud.")

        print("\nPress arrow keys to move, ESC to exit.")
        # on_press and on_release cannot work together, only one callback is possible
        #keyboard.on_press(on_key_press)
        #keyboard.on_release(on_key_release)
        keyboard.hook(on_key_action)
        keyboard.wait('esc')

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        if serial_port and serial_port.is_open:
            serial_port.close()
            print("Connection closed.")


if __name__ == "__main__":
    main()