"""Simple BLE UART client: toggle a device's LED on/off using simplepyble.

This is a minimal, self-contained example (no helper classes, no asyncio)
that:
1. Scans for a BLE peripheral by its advertised name
2. Connects to it
3. Auto-discovers the UART write/notify characteristics (UUIDs vary by
   module/vendor - e.g. the JDY-33-BLE does NOT use the standard Nordic
   UART Service UUIDs used by the MicroPython ble_uart.py example)
4. Controls Robo by sending commands

simplepyble is a synchronous, C++-backed library, so unlike bleak no
asyncio/await loop is needed.

Note: simplepyble is licensed under the Business Source License 1.1
(free for non-commercial use; a commercial license is required for
commercial use). See https://www.simpleble.org for details.

Requirements:
    pip install simplepyble keyboard
"""
import simplepyble
import keyboard

# The advertised name used by the BLE peripheral we want to find.
TARGET_NAME = "JDY-33-BLE-00"

KEY_DICT = {
    # up / forward
    "up": "up",
    "nach-oben": "up",
    # down / backward
    "down": "dn",
    "nach-unten": "dn",
    # left / turn left
    "left": "lt",
    "nach-links": "lt",
    # right / turn right
    "right": "rt",
    "nach-rechts": "rt",
    # stop
    "end": "sp",
    "ende": "sp",
    "clear": "sp",
    "enter": "run",
    # escape / exit / cancel
    "esc": "esc"
}

# Global variables
write_ble_char = None
notify_ble_char = None
ble_device = None


def find_uart_characteristics():
    """Find the writable and notifiable UART characteristics.

    Different BLE UART modules use different (non-standard) UUIDs for
    their characteristics, so we discover them at runtime instead of
    hardcoding the Nordic UART Service UUIDs.

    Returns (write, notify):
        write  = (service_uuid, write_uuid, needs_response) or None
        notify = (service_uuid, notify_uuid) or None
    """
    global write_ble_char, notify_ble_char, ble_device

    for service in ble_device.services():
        for char in service.characteristics():
            uuid = char.uuid()
            if uuid.startswith("0000a2"):  # meta-information / configuration, not a UART characteristic
                continue

            capabilities = char.capabilities()
            if write_ble_char is None and "write_request" in capabilities:
                write_ble_char = (service.uuid(), uuid, True)
            if write_ble_char is None and "write_command" in capabilities:
                write_ble_char = (service.uuid(), uuid, False)
            if notify_ble_char is None and "notify" in capabilities:
                notify_ble_char = (service.uuid(), uuid)

    if write_ble_char:
        print(f"Write characteristic: {write_ble_char}")
    else:
        print("Write characteristic not found.")

    if notify_ble_char:
        print(f"Notify characteristic: {notify_ble_char}")
    else:
        print("Notify characteristic not found.")


def ble_connect(ble_device_name):
    """Scan for ble_device_name and connect the matching peripheral."""
    global ble_device

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
        print(f"Device '{target_name}' was not found. Make sure it is advertising.")


def send_command(cmd):
    """Write a text command using the discovered write characteristic."""
    global write_ble_char, ble_device
    service_uuid, char_uuid, needs_response = write_ble_char
    data = cmd.encode()
    if needs_response:
        ble_device.write_request(service_uuid, char_uuid, data)
    else:
        ble_device.write_command(service_uuid, char_uuid, data)

# Key press event handler function (callback function)
def on_key_press(event):
    if event.name in KEY_DICT:
        send_command(KEY_DICT[event.name])

# Key release event handler function (callback function)
def on_key_release(event):
    send_command("dn")

# Key action event handler function (callback function)
def on_key_action(event):
    if event.event_type == keyboard.KEY_DOWN:
        on_key_press(event)
    elif event.event_type == keyboard.KEY_UP:
        on_key_release(event)


def handle_rx(data):
    """Print a notification received from the BLE UART device."""
    print(f"RX: {data.decode(errors='replace')}")


def main():
    """Scan, connect, and forward key presses to the BLE UART peripheral."""
    global write_ble_char, notify_ble_char, ble_device

    try:
        ble_connect(TARGET_NAME)
        find_uart_characteristics()
        if write_ble_char is None:
            print("Error! No writable UART characteristic found.")
            return

        if notify_ble_char:
            # Listen for responses before sending the first message so that
            # early notifications are not missed.
            notify_service, notify_char = notify_ble_char
            ble_device.notify(notify_service, notify_char, handle_rx)

        print("\nPress arrow keys to move, ESC to exit.")
        # on_press and on_release cannot work together, only one callback is possible
        #keyboard.on_press(on_key_press)
        #keyboard.on_release(on_key_release)
        keyboard.hook(on_key_action)
        keyboard.wait('esc')

        print("Program terminated.")
    finally:
        ble_device.disconnect()
        print("\nDisconnected")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
