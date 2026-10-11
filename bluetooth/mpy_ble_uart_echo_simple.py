"""
Bluetooth chat example for MicroPython.

The board shows up on your phone as "MPY_UART".
Connect with a Bluetooth UART app (for example "nRF Toolbox"),
send a message, and the board sends it back with "Echo: " in front.
"""
import bluetooth
from time import sleep

# Constants and configuration for the Bluetooth chat example
# --- Settings you can change ---
DEVICE_NAME = "MPY_UART"      # the name your phone will see
ADVERTISE_EVERY_US = 500000   # shout "I'm here!" every half second (in microseconds)

# --- Event numbers: Bluetooth tells us what happened using these numbers ---
EVENT_BLE_CONNECTED = 1
EVENT_BLE_DISCONNECTED = 2
EVENT_BLE_SENT_DATA = 3

# --- Nordic UART Service: a standard "text chat" over Bluetooth ---
# Every Bluetooth service and channel has its own long ID number (UUID).
SERVICE_ID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
# Channel for sending text FROM the board TO the phone
SEND_CHANNEL = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY)
# Channel for receiving text FROM the phone TO the board
RECEIVE_CHANNEL = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE)

# --- Advertising message: how the board introduces itself ---
# Each part is written as: length, type, data.
TYPE_FLAGS = 0x01                   # this part says "how I can be found"
TYPE_NAME = 0x09                    # this part says "this is my name"
FLAGS_VISIBLE_BLE_ONLY = 0x06       # "anyone can find me, I only use Bluetooth Low Energy"

# --- Global variables for advertising ---
advertising_data = bytes([2, TYPE_FLAGS, FLAGS_VISIBLE_BLE_ONLY])
advertising_data += bytes([len(DEVICE_NAME.encode()) + 1, TYPE_NAME]) + DEVICE_NAME.encode()

# --- Global variables that remember what is going on ---
connection = None         # who is connected (None means nobody)
received_bytes = b"" # text that arrived but is not handled yet
ble = None           # the Bluetooth object, created in main()
send_handle = None   # number of the channel used to send to the phone
receive_handle = None  # number of the channel used to receive from the phone


def on_bluetooth_event(event, data):
    """Bluetooth calls this function by itself whenever something happens."""
    global connection, received_bytes

    if event == EVENT_BLE_CONNECTED:
        connection = data[0]          # remember who connected
        print("Connected")

    elif event == EVENT_BLE_DISCONNECTED:
        connection = None             # nobody is connected anymore
        print("Disconnected")
        ble.gap_advertise(ADVERTISE_EVERY_US, advertising_data)  # let someone connect again

    elif event == EVENT_BLE_SENT_DATA and data[1] == receive_handle:
        received_bytes += ble.gatts_read(receive_handle)  # save the text that arrived


def read():
    """Return the text that arrived from the connected device ("" if nothing arrived)."""
    global received_bytes
    message = received_bytes.decode().strip()  # bytes -> text
    received_bytes = b""                       # empty the box, we have it now
    return message


def write(message):
    """Send text to the connected device (does nothing if nobody is connected)."""
    if connection is not None:
        ble.gatts_notify(connection, send_handle, message)


def main():
    global ble, send_handle, receive_handle  # shared with the functions above

    # --- Set up Bluetooth ---
    ble = bluetooth.BLE()
    ble.active(True)                  # switch Bluetooth on
    ble.irq(on_bluetooth_event)       # tell Bluetooth which function to call for events

    # Create the chat service. We get back a "handle" (a number) for each channel.
    ((send_handle, receive_handle),) = ble.gatts_register_services(
        ((SERVICE_ID, (SEND_CHANNEL, RECEIVE_CHANNEL)),)
    )

    # Start telling the world that we exist
    ble.gap_advertise(ADVERTISE_EVERY_US, advertising_data)
    print("Advertising... Look for:", DEVICE_NAME)

    # --- Main loop: runs until you press Ctrl+C ---
    try:
        while True:
            message = read()                # did something arrive?
            if message:
                print("Received:", message)
                write("Echo: " + message)   # send it back to the sender

            sleep(0.1)                      # short pause, then check again
    except KeyboardInterrupt:
        print("Stopped")


if __name__ == "__main__":
    main()