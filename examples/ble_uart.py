"""
BLE UART implementation using Nordic UART Service (NUS) for MicroPython.

This module provides a simple bidirectional serial communication over Bluetooth Low Energy
using the standard Nordic UART Service (NUS). Supports sending and receiving data from
connected BLE central devices.
https://docs.micropython.org/en/latest/library/bluetooth.html

Example:
    ble = BLEUART(name="MyDevice")
    ble.send("Hello from BLE")
    while True:
        data = ble.read()
        if data:
            print(f"Received: {data}")
"""
import bluetooth
import struct
import time
from micropython import const

# BLE event codes
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

# BLE Advertising Flags
_BLE_FLAG_LIMITED_DISCOVER = const(0x01)     # Device discoverable for a limited time only
_BLE_FLAG_GENERAL_DISCOVER = const(0x02)     # Device continuously discoverable
_BLE_FLAG_NO_BR_EDR_SUPPORT = const(0x04)    # Pure BLE device (no classic Bluetooth)
_BLE_FLAG_SIMULTAN_CONTROLLER = const(0x08)  # Simultaneous LE + BR/EDR Controller (not tested)
_BLE_FLAG_SIMULTAN_HOST = const(0x10)        # Simultaneous LE + BR/EDR Host (not tested)
_BLE_FLAG_DEFAULT = _BLE_FLAG_GENERAL_DISCOVER | _BLE_FLAG_NO_BR_EDR_SUPPORT
_BLE_APPEARANCE_COMPUTER = const(0x80)       # Appearance code: Generic Computer

# BLE Advertisement data types
_ADV_TYPE_FLAGS = const(0x01)                # Flags
_ADV_TYPE_NAME = const(0x09)                 # Complete Local Name
_ADV_TYPE_APPEARANCE = const(0x19)           # Appearance

_ADV_INTERVAL_US = 500000                    # Advertisement interval in microseconds


class BLEUART:
    '''
    BLE UART service using Nordic UART Service (NUS) UUIDs.
    
    Implements a serial communication interface over Bluetooth Low Energy using the
    standardized Nordic UART Service specification. Allows bidirectional data exchange
    with connected BLE central devices.
    
    Nordic UART Service (NUS):
    - Service UUID: 6E400001-B5A3-F393-E0A9-E50E24DCCA9E
    - TX Characteristic (NOTIFY): 6E400003-B5A3-F393-E0A9-E50E24DCCA9E
    - RX Characteristic (WRITE): 6E400002-B5A3-F393-E0A9-E50E24DCCA9E
    
    Attributes:
        _name (str): Device name advertised in BLE advertisements
        _flags (int): BLE advertising flags
        _ble: BLE instance from micropython.bluetooth
        _connections (set): Set of active connection handles
        _rx_buffer (bytearray): Buffer for received data
    '''
    def __init__(self, name="PICO_BLE_UART", flags=_BLE_FLAG_DEFAULT):
        """
        Initialize BLE UART service.
        
        Args:
            name (str): Device name to advertise (default: "PICO_BLE_UART")
            flags (int): BLE advertising flags (default: GENERAL_DISCOVER | NO_BR_EDR)
        
        Blocks until a central device connects, then continues execution.
        """
        self._name = name
        self._flags = flags
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)  # Register IRQ handler for BLE events

        # Nordic UART Service (NUS) UUIDs
        UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
        # TX: Device -> Central (Notify capability allows unsolicited messages)
        UART_TX = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY)
        # RX: Central -> Device (Write capability allows central to send data)
        UART_RX = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE)
        
        # Register the UART service with BLE stack
        UART_SERVICE = (UART_UUID, (UART_TX, UART_RX))
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((UART_SERVICE,))
        self._connections = set()      # Active connection handles
        self._rx_buffer = bytearray()  # Receive buffer

        self._advertise()
        print(f"BLE UART '{self._name}' is now advertising.")

        # Block until a central device connects (synchronous initialization)
        while not self.is_connected():
            time.sleep(0.5)
        time.sleep(0.5)  # Wait a bit more to ensure connection is stable
        
    def _irq(self, event, data):
        """
        Bluetooth event handler (Interrupt Request).
        
        Called asynchronously by the BLE stack when events occur.
        
        Args:
            event (int): Event type (_IRQ_CENTRAL_CONNECT, _IRQ_CENTRAL_DISCONNECT, _IRQ_GATTS_WRITE)
            data: Event-specific data
        """
        if event == _IRQ_CENTRAL_CONNECT:  # Central connected
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("Central connected")

        elif event == _IRQ_CENTRAL_DISCONNECT:  # Central disconnected
            conn_handle, _, _ = data
            self._connections.discard(conn_handle)
            print("Central disconnected")
            # Resume advertising to accept new connections
            self._advertise()

        elif event == _IRQ_GATTS_WRITE:  # Write received on RX characteristic
            conn_handle, value_handle = data
            if value_handle == self._rx_handle:
                # Read the data written to the RX characteristic
                msg = self._ble.gatts_read(self._rx_handle)
                self._rx_buffer.extend(msg)
                print("Received:", msg.decode().strip())

    def _advertise(self):
        """
        Build and start BLE advertising payload.
        
        Constructs a BLE advertisement packet containing:
        - Flags (advertising modes)
        - Device name
        - Device appearance (Generic Computer)
        
        Advertisement format is optimized for size (no UUID to save space).
        """
        # Create advertisement payload
        adv_payload = bytearray()

        # 1. Flags - indicates device capabilities and advertising mode
        # Format: length, type, value
        adv_payload += struct.pack("BB", 2, _ADV_TYPE_FLAGS)
        adv_payload += struct.pack("B", self._flags)
        
        # 2. Device Name - human-readable identifier
        name_bytes = bytes(self._name, "utf-8")
        adv_payload += struct.pack("BB", len(self._name) + 1, _ADV_TYPE_NAME) + name_bytes
        
        # 3. Appearance - indicates device type to central
        appearance = struct.pack("<h", _BLE_APPEARANCE_COMPUTER)
        adv_payload += struct.pack("BB", len(appearance) + 1, _ADV_TYPE_APPEARANCE) + appearance

        # Start advertising with the payload
        self._ble.gap_advertise(_ADV_INTERVAL_US, adv_payload)

    def send(self, data):
        """
        Send data to all connected central devices.
        
        Args:
            data (str or bytes): Data to send. Strings are automatically encoded to UTF-8.
        
        Note:
            Data is silently dropped if no devices are connected. No buffering occurs.
        """
        if isinstance(data, str):
            data = data.encode()
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx_handle, data)

    def read(self):
        """
        Read and clear all received data from the buffer.
        
        Returns:
            bytes: Data received from connected central devices. Empty bytes if no data.
        
        Note:
            This method clears the receive buffer after reading.
        """
        data = bytes(self._rx_buffer)
        self._rx_buffer[:] = b""
        return data
    
    def is_connected(self):
        """
        Check if at least one central device is connected.
        
        Returns:
            bool: True if connected, False otherwise.
        """
        return len(self._connections) > 0


# Example usage
if __name__ == "__main__":
    """
    Simple echo server demonstrating BLE UART usage.
    
    - Creates a BLE UART peripheral
    - Waits for a central device to connect (blocks in __init__)
    - Sends a welcome message
    - Echoes back any received data
    """
    # Initialize BLE UART (blocks until a central connects)
    ble_uart = BLEUART()

    # Verify connection is established
    assert ble_uart.is_connected(), "Connection check failed"
    
    # Send welcome message to connected central
    ble_uart.send("Send me a message...")
    
    # Main event loop
    while True:
        msg = ble_uart.read()  # Non-blocking read of receive buffer
        if msg:                # If data was received
            # Echo the message back with a prefix
            ble_uart.send("Echo: " + msg.decode())
        time.sleep(0.1)  # Yield to other tasks

