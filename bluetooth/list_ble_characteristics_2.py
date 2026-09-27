"""Get BLE UART characteristics using module bleak.

Requirements:
    pip install bleak
"""
import asyncio
from bleak import BleakScanner, BleakClient

# The advertised name used by the BLE peripheral we want to find.
TARGET_NAME = "JDY-33-BLE"


def list_ble_characteristics(peripheral):
    """List all BLE characteristics (with their properties) of every service.

    This is not limited to UART - it prints every characteristic so that the
    writable/notifiable UART ones can be identified visually, since different
    BLE UART modules use different (non-standard) UUIDs for their UART
    characteristics instead of the Nordic UART Service UUIDs.
    """
    for service in peripheral.services:
        for char in service.characteristics:
            uuid = char.uuid
            properties = char.properties
            print(uuid, properties)


async def ble_connect(ble_device_name):
    """Scan for ble_device_name and connect the matching peripheral."""
    client = None
    print(f"Scanning for {ble_device_name}...")
    ble_device = await BleakScanner.find_device_by_name(ble_device_name, timeout=5.0)

    if ble_device:
        print(f"Found {ble_device_name} at {ble_device.address}")
        client = BleakClient(ble_device)
        await client.connect()
        print("Connected\n")
    else:
        print(f"Device '{ble_device_name}' was not found. Make sure it is advertising.")

    return client


async def main():
    """Connect, and show BLE UART characteristics."""
    try:
        ble_device = await ble_connect(TARGET_NAME)
        if ble_device:
            list_ble_characteristics(ble_device)
    finally:
        if ble_device and ble_device.is_connected:
            await ble_device.disconnect()
            print("\nDisconnected")


if __name__ == "__main__":
    asyncio.run(main())
