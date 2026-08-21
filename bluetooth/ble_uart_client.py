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


class BLEUARTClient:
    """Manage a BLE UART connection and its UART characteristics."""

    def __init__(self, target_name):
        self.target_name = target_name
        self.device_address = None
        self.client = None
        self.rx_uuid = None
        self.tx_uuid = None
        self.read_uuid = None
        self._notifications_started = False

    async def find_device_by_name(self):
        """Scan for and find the configured BLE device by name."""
        print(f"Scanning for {self.target_name}...")
        device_address = None
        max_retry = 3
        for retry in range(max_retry):
            devices = await BleakScanner.discover()
            for device in devices:
                print(f"Discovered: {device.name} - {device.address}")
                if device.name == self.target_name:
                    print(f"Found {self.target_name} at {device.address}")
                    device_address = device.address
                    break
            if device_address:
                break
            await asyncio.sleep(1)
            if retry < max_retry - 1:
                print("Scan complete. Retrying...")
        return device_address

    async def get_uart_uuids(self):
        """Find RX write and TX notify characteristics on the device."""
        rx_uuid = None
        tx_uuid = None
        read_uuid = None
        for service in self.client.services:
            for char in service.characteristics:
                if "write" in char.properties:
                    rx_uuid = char.uuid
                    print(f"Found RX characteristic: {rx_uuid}")
                if "notify" in char.properties:
                    tx_uuid = char.uuid
                    print(f"Found TX characteristic: {tx_uuid}")
                if "read" in char.properties:
                    read_uuid = char.uuid
        self.read_uuid = read_uuid
        return rx_uuid, tx_uuid

    async def __aenter__(self):
        """Connect when entering an async context."""
        if not await self.connect():
            raise ConnectionError(
                f"Device {self.target_name} was not found"
            )
        return self

    async def __aexit__(self, _, __, ___):
        """Disconnect when leaving an async context."""
        await self.stop_notify()
        await self.disconnect()

    async def connect(self):
        """Find the target, connect to it, and discover its UART UUIDs."""
        self.device_address = await self.find_device_by_name()
        if not self.device_address:
            return False

        print(f"Connecting to {self.target_name}...")
        self.client = BleakClient(self.device_address)
        await self.client.connect()
        print("Connected\n")

        self.rx_uuid, self.tx_uuid = await self.get_uart_uuids()
        if not self.rx_uuid or not self.tx_uuid:
            await self.disconnect()
            raise ConnectionError("Could not find UART characteristics")
        return True

    async def disconnect(self):
        """Disconnect from the BLE device if connected."""
        if self.client and self.client.is_connected:
            await self.client.disconnect()

    async def start_notify(self, callback):
        """Subscribe to notifications from the UART TX characteristic."""
        await self.client.start_notify(self.tx_uuid, callback)
        self._notifications_started = True

    async def stop_notify(self):
        """Stop UART notifications if they were enabled."""
        if self.client and self._notifications_started:
            await self.client.stop_notify(self.tx_uuid)
            self._notifications_started = False

    async def write(self, message):
        """Encode and write a text message to the UART RX characteristic."""
        await self.client.write_gatt_char(self.rx_uuid, message.encode())

    async def read(self):
        """Read bytes from the device's readable characteristic.

        Raises:
            ConnectionError: If the device has no readable characteristic.
        """
        if not self.read_uuid:
            raise ConnectionError("BLE device has no readable characteristic")
        return await self.client.read_gatt_char(self.read_uuid)
