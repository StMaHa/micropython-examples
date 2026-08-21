"""Toggle a BLE UART device's LED by sending alternating state commands."""
import asyncio
from ble_uart_client import BLEUARTClient

# Target device name to connect to
TARGET_NAME = "JDY-33-BLE"


async def _uart_led_client():
    """
    Main BLE UART client function.

    Uses ``BLEUARTClient`` as an async context manager. The class handles
    scanning, connection, UART characteristic discovery, and disconnection.

    Flow:
    1. Create and connect the BLE UART client
    2. Set up a notification handler for incoming data
    3. Send alternating ``on`` and ``off`` commands

    Raises:
        KeyboardInterrupt: When user presses Ctrl+C
    """
    try:
        # Entering the context scans, connects, and discovers the UART UUIDs.
        async with BLEUARTClient(TARGET_NAME) as ble_uart:
            def handle_rx(_, data):
                """Print a notification received from the BLE UART device."""
                # Bleak passes the characteristic and its payload to callbacks.
                print(f"RX: {data.decode()}")

            # Notifications carry responses from the device to this computer.
            await ble_uart.start_notify(handle_rx)

            print("Sending messages every second...\n")
            while True:
                # The peripheral expects newline-terminated text commands.
                for state in ("on\n", "off\n"):
                    print(f"LED {state.strip()}")
                    try:
                        # The client encodes the command and writes it to RX.
                        await ble_uart.write(state)
                    except Exception as error:
                        # Present a device disconnect as an actionable application error.
                        raise ConnectionError(
                            f"BLE device disconnected while writing: {error}"
                        ) from None
                    # Keep each LED state active to see LED blinking.
                    await asyncio.sleep(1)
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
