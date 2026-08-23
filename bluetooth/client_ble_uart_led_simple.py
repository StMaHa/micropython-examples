"""Simple BLE UART client: toggle a device's LED on/off using bleak.

This is a minimal, self-contained example (no helper classes, no
notifications) that:
1. Scans for a BLE peripheral by its advertised name
2. Connects to it
3. Auto-discovers the UART write/read characteristics (UUIDs vary by
   module/vendor - e.g. the JDY-33-BLE does NOT use the standard Nordic
   UART Service UUIDs used by the MicroPython ble_uart.py example)
4. Repeatedly writes "on\\n" / "off\\n" text commands to toggle the LED
5. Optionally polls a readable characteristic for a response

Polling is used instead of notifications to keep the example as simple as
possible - just write, then (optionally) read.

Requirements:
    pip install bleak
"""
import asyncio
from bleak import BleakScanner, BleakClient

# The advertised name used by the BLE peripheral we want to find.
TARGET_NAME = "JDY-33-BLE"


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


async def main():
    """Scan, connect, and toggle the LED on/off every second (polling)."""
    print(f"Scanning for {TARGET_NAME}...")
    device = await BleakScanner.find_device_by_name(TARGET_NAME, timeout=10.0)
    if device is None:
        print(f"Device '{TARGET_NAME}' was not found. Make sure it is advertising.")
        return

    print(f"Found {TARGET_NAME} at {device.address}")
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

        try:
            while True:
                for state in ("on\n", "off\n"):
                    print(f"Turn LED {state.strip()}")
                    await client.write_gatt_char(write_uuid, state.encode())
                    await asyncio.sleep(1)
                    # Polling not working
                    #response = await client.read_gatt_char(notify_uuid)
                    #print("RX:", response)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
        print("Disconnected")
