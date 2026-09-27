"""Get BLE UART characteristics using module simplepyble.

Requirements:
    pip install simplepyble
"""
import simplepyble

# The advertised name used by the BLE peripheral we want to find.
TARGET_NAME = "JDY-33-BLE"


def list_ble_characteristics(peripheral):
    """Find the writable and notifiable UART characteristics.

    Different BLE UART modules use different (non-standard) UUIDs for
    their characteristics, so we discover them at runtime instead of
    hardcoding the Nordic UART Service UUIDs.
    """
    for service in peripheral.services():
        for char in service.characteristics():
            uuid = char.uuid()
            capabilities = char.capabilities()
            print(uuid, capabilities)


def ble_connect(ble_device_name):
    """Scan for ble_device_name and connect the matching peripheral."""
    ble_device = None

    adapters = simplepyble.Adapter.get_adapters()
    if not adapters:
        print("Error! No Bluetooth adapters found.")
        return
    adapter = adapters[0]

    print(f"Scanning for {ble_device_name}...")
    adapter.scan_for(5000)

    peripherals = adapter.scan_get_results()
    for peripheral in peripherals:
        if peripheral.identifier() == ble_device_name:
            ble_device = peripheral
            break

    if ble_device:
        print(f"Found {ble_device_name} at {ble_device.address()}")
        ble_device.connect()
        print("Connected\n")
    else:
        print(f"Device '{ble_device_name}' was not found. Make sure it is advertising.")

    return ble_device


def main():
    """Connect, and show BLE UART characteristics."""
    try:
        ble_device = ble_connect(TARGET_NAME)
        if ble_device:
            list_ble_characteristics(ble_device)
    finally:
        if ble_device and ble_device.is_connected:
            ble_device.disconnect()
            print("\nDisconnected")


if __name__ == "__main__":
    main()
