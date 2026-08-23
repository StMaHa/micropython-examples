"""Send a periodic text message to a BLE UART device and print responses."""
import asyncio
from ble_uart_client import BLEUARTClient

# Bluetooth - UART adapter
# - Raspberry Pi Pico W/2W
# - JDY-33:    BT CLassic (JDY-33-SPP) and BLE (JDY-33-BLE)

# The advertised name used by the BLE peripheral we want to find.
TARGET_NAME = "PICO_BLE_UART"  # See configured name on Raspberry Pi Pico W/2W
USE_READ_POLLING = False  # Set to True to read the device's readable characteristic after each write (polling).
                          #  Polling is working with BLE of Raspberry Pi Pico W/2W, other devices might not.
                          # Set to False to only read the device's TX notify characteristic (event-driven).

async def _uart_echo_client():
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
    4. Send messages in a loop

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
            i = 0
            while True:
                # Give each message a distinct sequence number for easy tracing.
                i += 1
                msg = f"Hello World {i}"
                print(f"TX: {msg}")
                try:
                    # The client encodes the text and writes it to the peripheral's
                    # RX characteristic.
                    response = await ble_uart.write(msg)
                    if response:  # Only print if a response was received (polling enabled)
                        print(f"RX: {response}")
                except Exception as error:
                    # Present BLE read/write failures as an application error.
                    raise ConnectionError(
                        f"BLE device communication failed: {error}"
                    ) from None
                # Delay the event loop and limit the message rate to one/sec.
                await asyncio.sleep(1)
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

        # Run the coroutine until it exits or the user interrupts the program.
        asyncio.run(_uart_echo_client())
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