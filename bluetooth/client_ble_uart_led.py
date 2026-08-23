"""Toggle a BLE UART device's LED by sending alternating state commands."""
import asyncio
from ble_uart_client import BLEUARTClient

# Bluetooth - UART adapter
# Raspberry Pi Pico W/2W
# - JDY-33:    BT CLassic (JDY-33-SPP) and BLE (JDY-33-BLE)

# The advertised name used by the BLE peripheral we want to find.
TARGET_NAME = "JDY-33-BLE"
USE_READ_POLLING = False  # Set to True to read the device's readable characteristic after each write (polling).
                          #  Polling cannot be used easily on some devices. Notification is working fast and reliable.
                          # Set to False to only read the device's TX notify characteristic (event-driven).

async def _uart_led_client():
    """
    Main BLE UART client function.

    Uses ``BLEUARTClient`` as an async context manager for bidirectional
    communication. Device scanning, connection, and UART characteristic
    discovery happen when entering the context; disconnection happens when it
    exits.

    Flow:
    1. Create the BLE UART client
    2. Connect and discover UART characteristics through ``async with``
    3. Set up a notification handler for incoming data
    4. Read and display the device response after each command

    Raises:
        KeyboardInterrupt: When user presses Ctrl+C
    """
    try:
        # Entering the context scans, connects, and discovers the UART UUIDs.
        # Keep the polling policy inside the client instead of handling reads
        # separately in this application loop.
        async with BLEUARTClient(TARGET_NAME, use_read_polling=USE_READ_POLLING) as ble_uart:
            if not USE_READ_POLLING:
                print("\nListening for notifications from the BLE UART device...")
                # Define a callback to handle incoming notifications from the BLE UART device.
                def handle_rx(_, data):
                    """Print a notification received from the BLE UART device."""
                    # Bleak supplies the characteristic and the received bytes.
                    print(f"RX: {data.decode(errors='replace')}")

                # Listen for responses before sending the first message so that
                # early notifications are not missed.
                await ble_uart.start_notify(handle_rx)
            else:
                print("\nUsing polling mode to read responses from the BLE UART device...")

            print("Sending messages every second...\n")
            while True:
                # The peripheral expects newline-terminated text commands.
                for state in ("on\n", "off\n"):
                    print(f"Turn LED {state.strip()}")
                    try:
                        # The client writes the command and reads the response.
                        response = await ble_uart.write(state)
                        await asyncio.sleep(0.1)
                        if response:  # Only print if a response was received (polling enabled)
                            print(f"RX: {response}")
                    except Exception as error:
                        # Present BLE read/write failures as an application error.
                        raise ConnectionError(f"BLE device communication failed: {error}")
                    # Keep each LED state active to see LED blinking.
                    await asyncio.sleep(0.9)
    except KeyboardInterrupt:
        raise KeyboardInterrupt
    except ConnectionError as error:
        print(f"{error}\nMake sure the device is advertising and try again.")

def main():
    """Entry point - run the BLE UART client."""
    try:
        print("=" * 20)
        print("BLE UART Client")
        print("=" * 20)
        print()

        # Start the event loop that drives scanning, notifications, and writes.
        asyncio.run(_uart_led_client())
    except KeyboardInterrupt:
        # Allow a manual stop without displaying a traceback.
        print("\nProgram terminated by user")
        print("Disconnected")
    except ConnectionError as e:
        # Report connection failures raised by the async client.
        print(f"\n{e}")
        print("Disconnected")


if __name__ == "__main__":
    main()
