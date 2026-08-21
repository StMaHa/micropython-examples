"""Send a periodic text message to a BLE UART device and print responses."""
import asyncio
from ble_uart_client import BLEUARTClient


# The advertised name used by the BLE peripheral we want to find.
TARGET_NAME = "PICO_BLE_UART"


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
    # Store the target name in a client object; connection work is asynchronous.
    ble_uart_client = BLEUARTClient(TARGET_NAME)
    try:
        # Entering the context scans for the device, connects to it, and finds
        # the RX/TX characteristics. Exiting it disconnects automatically.
        async with ble_uart_client as ble_uart:
            def handle_rx(_, data):
                """Print a notification received from the BLE UART device."""
                # Bleak supplies the characteristic and the received bytes.
                print(f"RX: {data.decode()}")

            # Listen for responses before sending the first message so that
            # early notifications are not missed.
            await ble_uart.start_notify(handle_rx)

            print("Sending messages every second...\n")
            i = 0
            while True:
                # Give each message a distinct sequence number for easy tracing.
                i += 1
                msg = f"Hello World {i}"
                print(f"TX: {msg}")
                # The client encodes the text and writes it to the peripheral's
                # RX characteristic.
                await ble_uart.write(msg)
                # Yield to the event loop and limit the message rate to one/sec.
                await asyncio.sleep(1)
    except KeyboardInterrupt:
        raise KeyboardInterrupt


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
        # Stop cleanly instead of showing an interruption traceback.
        print("\n\nProgram terminated by user")
        print("Disconnected")


if __name__ == "__main__":
    main()