import time
import simplepyble


def discover_ble_devices():
    # Check for bluetooth devices
    adapters = simplepyble.Adapter.get_adapters()

    if not adapters:
        print("No bluetooth adapter found.")
        return

    # Choose first bluetooth adapter for scanning
    adapter = adapters[0]
    print(f"Use bluetooth adapter: {adapter.identifier()} [{adapter.address()}]\n")

    print("Discover Bluetooth Low Energy (BLE) devices. Scan for 5 seconds...")
    adapter.scan_for(5000)

    # Get found BLE devices
    ble_devices = adapter.scan_get_results()

    # Ergebnisse übersichtlich ausgeben
    for ble_device in ble_devices:
        if ble_device.identifier():
            name = ble_device.identifier()
        else: 
            name = "Unknown device."
        address = ble_device.address().upper()
        print(f"  {address}: {name}")


if __name__ == "__main__":
    discover_ble_devices()
