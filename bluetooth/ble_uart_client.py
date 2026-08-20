# https://docs.bleak.readthedocs.io/
"""
BLE UART Client for communicating with Nordic UART Service devices.

This module implements a Bluetooth Low Energy (BLE) client that connects to a
BLE UART server (like PICO_BLE_UART) using the Nordic UART Service (NUS).

The client:
1. Discovers the target device by name
2. Connects to the device
3. Auto-detects UART characteristic UUIDs
4. Sends messages to the device
5. Receives and displays responses

Requirements:
    pip install bleak

Example:
    python ble_uart_client.py
    # Wait for scan and connection
    # Type messages and receive responses
"""
import asyncio
from bleak import BleakScanner, BleakClient

# Target device name to connect to
TARGET_NAME = "PICO_BLE_UART"


async def find_device_by_name(name):
    """
    Scan for and find a BLE device by its advertised name.

    Performs a BLE scan and searches for a device with the specified name.
    Prints all discovered devices during scan.

    Args:
        name (str): The device name to search for (e.g., "PICO_BLE_UART")

    Returns:
        str: MAC address of the device if found, None otherwise

    Example:
        mac = await find_device_by_name("PICO_BLE_UART")
        if mac:
            print(f"Device found at {mac}")
    """
    print(f"Scanning for {name}...")
    device_address = None
    max_retry = 3
    for i in range(max_retry):  # Scan multiple times to increase chance of discovery
        devices = await BleakScanner.discover()
        for device in devices:
            print(f"Discovered: {device.name} - {device.address}")
            if device.name == name:
                print(f"Found {name} at {device.address}")
                device_address = device.address
                break
        if device_address:
            break
        else:
            await asyncio.sleep(1)  # Wait a bit before retrying
            if i < max_retry - 1:
                print("Scan complete. Retrying...")

    return device_address


async def get_uart_uuids(client):
    """
    Auto-detect UART characteristics from a connected BLE device.

    Scans the device's GATT services and identifies the RX and TX
    characteristics based on their properties:
    - RX (write): characteristic that accepts data from central
    - TX (notify): characteristic that sends data to central

    Nordic UART Service UUIDs:
    - Service: 6E400001-B5A3-F393-E0A9-E50E24DCCA9E
    - RX Char: 6E400002-B5A3-F393-E0A9-E50E24DCCA9E (write)
    - TX Char: 6E400003-B5A3-F393-E0A9-E50E24DCCA9E (notify)

    Args:
        client (BleakClient): Connected BLE client instance

    Returns:
        tuple: (rx_uuid, tx_uuid) - UUIDs of RX and TX characteristics,
               or (None, None) if not found

    Note:
        This works with any BLE UART service, not just Nordic NUS.
        It searches by characteristic properties, not by UUID.
    """
    rx_uuid = None  # Characteristic for receiving data (write property)
    tx_uuid = None  # Characteristic for transmitting data (notify property)

    # Iterate through all services and characteristics
    for service in client.services:
        for char in service.characteristics:
            if "write" in char.properties:
                rx_uuid = char.uuid
                print(f"Found RX characteristic: {rx_uuid}")
            if "notify" in char.properties:
                tx_uuid = char.uuid
                print(f"Found TX characteristic: {tx_uuid}")

    return rx_uuid, tx_uuid
