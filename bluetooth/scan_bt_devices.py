import asyncio
import os
import platform
if platform.system().lower() != "linux":
    print(f"Script '{os.path.basename(__file__)}' is only supported on Linux systems.")
    exit(1)
import bluetooth  # python3-bluez


def discover_bt_devices():
    print("\nDiscover Bluetooth Classic devices")
    devices = bluetooth.discover_devices(lookup_names = True)
    for addr, name in devices:
        print(f"  {addr.strip()}: {name.strip()}")


if __name__ == "__main__":
    discover_bt_devices()