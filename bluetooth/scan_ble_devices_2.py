import asyncio
from bleak import BleakScanner  # python3-bleak
import platform


async def discover_ble_devices():
    print("\nDiscover Bluetooth Low Energy (BLE) devices")
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"  {device}")


if __name__ == "__main__":
    asyncio.run(discover_ble_devices())
