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


class BLEUARTClient:
    """Manage a BLE UART connection and its UART characteristics."""

    def __init__(self, target_name, use_read_polling=False):
        self.target_name = target_name
        self.use_read_polling = use_read_polling
        self.device_address = None
        self.client = None
        self.rx_uuid = None
        self.tx_uuid = None
        self.read_uuid = None
        self._notifications_started = False

    async def __aenter__(self):
        """Called automatically when entering ``async with BLEUARTClient(...) as x:``.

        Connects to the device. The value returned here becomes ``x``.
        """
        if not await self.connect():
            raise ConnectionError(
                f"Device {self.target_name} was not found"
            )
        return self

    async def __aexit__(self, _, __, ___):
        """Called automatically when leaving the ``async with`` block.

        Runs even if an error happened inside the block, so the connection
        is always cleaned up (like a ``finally``). The 3 unused args carry
        exception info, if any.
        """
        await self.stop_notify()
        await self.disconnect()

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
        """Find the NUS RX/write and TX/notify characteristics.

        RX and TX are named from the peripheral's point of view: RX receives
        data from this central, while TX transmits data to this central.
        """
        rx_uuid = None
        tx_uuid = None
        read_uuid = None
        print("Get UART UUIDs:")
        for service in self.client.services:
            for char in service.characteristics:
                print(char.properties, char.uuid)
                if char.uuid.startswith("0000a2"):
                    continue
                if not rx_uuid and ("write" in char.properties):
                    # NUS RX means peripheral receive. The central writes
                    # commands here, so write() uses this UUID.
                    #
                    # A writable characteristic is where the central sends data to the
                    # peripheral. In UART‑style services this is the RX characteristic:
                    # the peripheral "receives" commands or payloads written by the central.
                    #
                    # Some modules only support Write Without Response (fast, no ACK),
                    # others support Write With Response (slower, but confirmed). Bleak
                    # abstracts this, but the underlying behavior affects timing and
                    # throughput. This UUID is used for all outbound messages.
                    rx_uuid = char.uuid

                if not tx_uuid and "notify" in char.properties:
                    # NUS TX means peripheral transmit. The central receives
                    # asynchronous responses through notifications here.
                    #
                    # A notifiable characteristic pushes data from the peripheral to the
                    # central asynchronously. In UART‑style services this is the TX
                    # characteristic: the peripheral "transmits" data whenever new bytes
                    # are available.
                    #
                    # Notifications are event‑driven: the central does not poll. This is
                    # the preferred mechanism for receiving UART data because it avoids
                    # latency and reduces traffic. Some modules also expose TX as readable,
                    # but notify remains the real-time channel.
                    tx_uuid = char.uuid

                if not read_uuid and "notify" in char.properties:
                    # A readable characteristic allows the central to perform
                    # an explicit GATT Read Request. This is different from
                    # notifications: notifications push data automatically,
                    # while read requires the central to poll the value.
                    #
                    # Some UART‑like services expose a readable TX characteristic
                    # so the central can fetch the current buffer state without
                    # waiting for a notification. Not all UART implementations
                    # include this, but if present, it can be used for polling.
                    read_uuid = char.uuid

        print(f"Using write characteristic:  {rx_uuid}")
        print(f"Using read characteristic:   {read_uuid}")
        print(f"Using notify characteristic: {tx_uuid}")

        return rx_uuid, tx_uuid, read_uuid

    async def connect(self):
        """Find the target, connect to it, and discover its UART UUIDs."""
        self.device_address = await self.find_device_by_name()
        if not self.device_address:
            return False

        print(f"Connecting to {self.target_name}...")
        self.client = BleakClient(self.device_address)
        await self.client.connect()
        print("Connected\n")

        self.rx_uuid, self.tx_uuid, self.read_uuid = await self.get_uart_uuids()
        if not self.rx_uuid or not self.tx_uuid or not self.read_uuid:
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
        """Send text to the peripheral's NUS RX/write endpoint.

        ``rx_uuid`` is not the central's receive UUID. It is the standard NUS
        name for the peripheral characteristic that receives central writes.
        """
        response = None
        # The central writes to the peripheral's RX characteristic.
        await self.client.write_gatt_char(self.rx_uuid, message.encode(), response = True)
        if self.use_read_polling:
            await asyncio.sleep(0.1)  # Allow time for the device to process and respond
            # Polling uses a separate readable characteristic when available;
            # TX is notification-only on many UART peripherals.
            response = await self.read()
        return response

    async def read(self):
        """Poll the characteristic that exposes the GATT read property.

        Raises:
            ConnectionError: If the device has no readable characteristic.
        """
        response = None
        if not self.read_uuid:
            raise ConnectionError("BLE device has no readable characteristic")
        try:
            response = await self.client.read_gatt_char(self.read_uuid, use_cached = False)
            response = response.decode(errors="replace")
        except:
            print("BLE read failed. Device may not support read characteristic.")
        return response

