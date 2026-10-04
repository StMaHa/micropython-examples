"""Simple BLE UART client: toggle a device's LED on/off using bleak.

This is a minimal, self-contained example (no helper classes, no
notifications) that:
1. Scans for a BLE peripheral by its advertised name
2. Connects to it
3. Auto-discovers the UART write/read characteristics (UUIDs vary by
   module/vendor - e.g. the JDY-33-BLE does NOT use the standard Nordic
   UART Service UUIDs used by the MicroPython ble_uart.py example)
4. Controls Robo by sending commands

Requirements:
    pip install bleak keyboard
"""
import asyncio
import keyboard
import robo_constants as robo
import sys
from bleak import BleakScanner, BleakClient

# The advertised name used by the BLE peripheral we want to find.
TARGET_NAME = robo.BLE_TARGET_NAME

client = None
write_uuid = None
notify_uuid = None


def find_uart_characteristics(client):
    """Find the writable and readable UART characteristics.

    Different BLE UART modules use different (non-standard) UUIDs for
    their characteristics, so we discover them at runtime instead of
    hardcoding the Nordic UART Service UUIDs.
    """
    write_uuid = None
    notify_uuid = None

    for service in client.services:
        for char in service.characteristics:
            if char.uuid.startswith("0000a2"):  # Ignore meta-information and configuration properties
                continue
            if not write_uuid and ("write" in char.properties):
                write_uuid = char.uuid
            if "notify" in char.properties:
                notify_uuid = char.uuid

    print(f"Using write characteristic: {write_uuid}")
    print(f"Using notify characteristic:  {notify_uuid}")

    return write_uuid, notify_uuid


async def send_command(cmd):
    global client, write_uuid
    await client.write_gatt_char(write_uuid, cmd.encode())


# Key press event handler function (callback function)
def on_key_press(event):
    if event.name in robo.KEY_DICT:
        asyncio.run(send_command(robo.KEY_DICT[event.name]))

# Key release event handler function (callback function)
def on_key_release(event):
     asyncio.run(send_command("dn"))

# Key action event handler function (callback function)
def on_key_action(event):
    if event.event_type == keyboard.KEY_DOWN:
        on_key_press(event)
    elif event.event_type == keyboard.KEY_UP:
        on_key_release(event)


async def main(target_name):
    """Scan, connect, and toggle the LED on/off every second (polling)."""
    global client, write_uuid, notify_uuid

    print(f"Scanning for {target_name}...")
    device = await BleakScanner.find_device_by_name(target_name, timeout=10.0)
    if device is None:
        print(f"Device '{target_name}' was not found. Make sure it is advertising.")
        return

    print(f"Found {target_name} at {device.address}")
    async with BleakClient(device) as client:
        print("Connected\n")

        write_uuid, notify_uuid = find_uart_characteristics(client)

        # Define a callback to handle incoming notifications from the BLE UART device.
        def handle_rx(_, data):
            """Print a notification received from the BLE UART device."""
            # Bleak supplies the characteristic and the received bytes.
            print(f"RX: {data.decode(errors='replace')}")

        # Listen for responses before sending the first message so that
        # early notifications are not missed.
        await client.start_notify(notify_uuid, handle_rx)

        print("\nPress arrow keys to move, ESC to exit.")
        # on_press and on_release cannot work together, only one callback is possible
        #keyboard.on_press(on_key_press)
        #keyboard.on_release(on_key_release)
        keyboard.hook(on_key_action)
        keyboard.wait('esc')

        print("Program terminated.")


if __name__ == "__main__":
    ble_device_name = TARGET_NAME  # default name
    if len(sys.argv) > 1:  # First value is the script name
        ble_device_name = sys.argv[1]
    print(f"{sys.argv[0]} {ble_device_name}\n")
    try:
        asyncio.run(main(ble_device_name))
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
        print("Disconnected")
