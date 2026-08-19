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


async def uart_client():
    """
    Main BLE UART client function.
    
    Establishes a BLE connection to a UART peripheral and implements
    bidirectional communication:
    - Sends messages to the device
    - Receives and displays responses
    
    Flow:
    1. Scan and find target device
    2. Connect to device
    3. Discover UART characteristics
    4. Set up notification handler for incoming data
    5. Send messages in a loop
    
    Raises:
        KeyboardInterrupt: When user presses Ctrl+C
    """
    # Step 1: Find target device by name
    mac = await find_device_by_name(TARGET_NAME)
    if not mac:
        print("Device not found.\nMake sure the device is advertising and try again.")
        return

    # Step 2: Connect to the device
    print(f"Connecting to {TARGET_NAME}...")
    async with BleakClient(mac) as client:
        print("Connected\n")
        
        # Step 3: Auto-detect UART characteristic UUIDs
        rx_uuid, tx_uuid = await get_uart_uuids(client)
        
        # Verify both characteristics were found
        if not rx_uuid or not tx_uuid:
            print("Could not find UART characteristics")
            return

        # Step 4: Set up notification callback for incoming data
        # This function is called whenever the TX characteristic sends data
        def handle_rx(_, data):
            """Callback for received data from device."""
            print(f"RX: {data.decode()}")

        # Subscribe to TX notifications (incoming data from device)
        await client.start_notify(tx_uuid, handle_rx)

        # Step 5: Send messages in a loop
        print("Sending messages every second...\n")
        i = 0
        while True:
            i += 1
            msg = f"Hello World {i}"
            print(f"TX: {msg}")
            # Write to RX characteristic (sending data to device)
            await client.write_gatt_char(rx_uuid, msg.encode())
            # Wait 1 second before sending next message
            await asyncio.sleep(1)

if __name__ == "__main__":
    """Entry point - run the BLE UART client."""
    try:
        print("=" * 20)
        print("BLE UART Client")
        print("=" * 20)
        print()
        
        # Run the async client
        asyncio.run(uart_client())
    except KeyboardInterrupt:
        # User pressed Ctrl+C
        print("\n\nProgram terminated by user")
        print("Disconnected")
