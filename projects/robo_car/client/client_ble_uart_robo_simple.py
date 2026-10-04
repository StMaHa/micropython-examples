"""Simple BLE UART client: toggle a device's LED on/off using simplepyble.

This is a minimal, self-contained example (no helper classes, no asyncio)
that:
1. Scans for a BLE peripheral by its advertised name
2. Connects to it
3. Controls Robo by sending commands

simplepyble is a synchronous, C++-backed library, so unlike bleak no
asyncio/await loop is needed.

Note: simplepyble is licensed under the Business Source License 1.1
(free for non-commercial use; a commercial license is required for
commercial use). See https://www.simpleble.org for details.

Requirements:
    pip install simplepyble keyboard
"""
import keyboard
import robo_constants as robo
import simplepyble
import sys


# The advertised name used by the BLE peripheral we want to find.
TARGET_NAME = robo.BLE_TARGET_NAME

# Global variables
write_ble_char = None
notify_ble_char = None
ble_device = None

is_key_pressed = False

def ble_connect(ble_device_name):
    """Scan for ble_device_name and connect the matching peripheral."""
    ble_device = None

    adapters = simplepyble.Adapter.get_adapters()
    if not adapters:
        print("Error! No Bluetooth adapters found.")
        return
    adapter = adapters[0]

    print(f"Scanning for {ble_device_name}...")
    # Scan for all available devices
    adapter.scan_for(5000)
    # Get all found devices
    peripherals = adapter.scan_get_results()
    # Search for the required device 
    for peripheral in peripherals:
        if peripheral.identifier() == ble_device_name:
            ble_device = peripheral
            break

    return ble_device


def send_command(cmd):
    """Write a text command using the discovered write characteristic."""
    global ble_device
    data = f"{cmd}\n".encode()
    ble_device.write_command(robo.BLE_UUID_SERVICE, robo.BLE_UUID_WRITE, data)

# Key press event handler function (callback function)
def on_key_press(event):
    global is_key_pressed
    # Ignore the key press if another key is already being processed
    if is_key_pressed:
        return
    is_key_pressed = True
    if event.name in robo.KEY_DICT:
        send_command(robo.KEY_DICT[event.name])

# Key release event handler function (callback function)
def on_key_release(event):
    global is_key_pressed
    # Mark that no key is being processed anymore
    is_key_pressed = False
    send_command("sp")

# Key action event handler function (callback function)
def on_key_action(event):
    if event.event_type == keyboard.KEY_DOWN:
        on_key_press(event)
    elif event.event_type == keyboard.KEY_UP:
        on_key_release(event)


def handle_rx(data):
    """Print a notification received from the BLE UART device."""
    print(f"RX: {data.decode(errors='replace')}")


def main(target_name):
    """Scan, connect, and forward key presses to the BLE UART peripheral."""
    global ble_device

    try:
        ble_device = ble_connect(target_name)
        if ble_device:
            print(f"Found {target_name} at {ble_device.address()}")
            ble_device.connect()
            print("Connected\n")
        else:
            print(f"Device '{target_name}' was not found. Make sure it is advertising.")
            return

        if robo.BLE_UUID_NOTIFY:
            # Listen for responses before sending the first message so that
            # early notifications are not missed.
            ble_device.notify(robo.BLE_UUID_SERVICE, robo.BLE_UUID_NOTIFY, handle_rx)

        print("\nPress arrow keys to move, ESC to exit.")
        # on_press and on_release cannot work together, only one callback is possible
        #keyboard.on_press(on_key_press)
        #keyboard.on_release(on_key_release)
        keyboard.hook(on_key_action)
        keyboard.wait('esc')

        print("Program terminated.")
    finally:
        ble_device.disconnect()
        print("\nDisconnected")


if __name__ == "__main__":
    ble_device_name = TARGET_NAME  # default name
    if len(sys.argv) > 1:  # First value is the script name
        ble_device_name = sys.argv[1]
    print(f"{sys.argv[0]} {ble_device_name}\n")
    try:
        main(ble_device_name)
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
