"""
Example usage of ble_uart_client module
"""
import asyncio
from bleak import BleakClient
from ble_uart_client import find_device_by_name, get_uart_uuids

# Target device name to connect to
TARGET_NAME = "JDY-33-BLE"


async def _uart_led_client():
    """
    Main BLE UART client function.

    Establishes a BLE connection to a UART peripheral and implements
    bidirectional communication:
    - Sends messages to the device
    - Receives and displays responses

    Flow:
    1. Scan and find target device
    2. Connect to device
    3. Discover UART characteristics
    4. Set up notification handler for incoming data
    5. Send on/off messages in a loop to utilize the onboard LED

    Raises:
        KeyboardInterrupt: When user presses Ctrl+C
    """
    # Step 1: Find target device by name
    mac = await find_device_by_name(TARGET_NAME)
    if not mac:
        print("Device not found.\nMake sure the device is advertising and try again.")
        return

    # Step 2: Connect to the device
    print(f"Connecting to {TARGET_NAME}...")

    try:
        async with BleakClient(mac) as client:
            print("Connected\n")

            # Step 3: Auto-detect UART characteristic UUIDs
            rx_uuid, tx_uuid = await get_uart_uuids(client)

            # Verify both characteristics were found
            if not rx_uuid or not tx_uuid:
                print("Could not find UART characteristics")
                return

            # Step 4: Set up notification callback for incoming data
            # This function is called whenever the TX characteristic sends data
            def handle_rx(_, data):
                """Callback for received data from device."""
                print(f"RX: {data.decode()}")

            # Subscribe to TX notifications (incoming data from device)
            await client.start_notify(tx_uuid, handle_rx)

            # Step 5: Send messages in a loop
            print("Sending messages every second...\n")
            while True:
                for state in ("on\n", "off\n"):
                    print(f"LED {state.strip()}")
                    # Send new LED state
                    try:
                        await client.write_gatt_char(rx_uuid, state.encode())
                    except Exception as error:
                        raise ConnectionError(
                            f"BLE device disconnected while writing: {error}"
                        ) from None
                    # Keep LED state for one second
                    await asyncio.sleep(1)

    except:
        raise


def main():
    """Entry point - run the BLE UART client."""
    try:
        print("=" * 20)
        print("BLE UART Client")
        print("=" * 20)
        print()

        # Run the async client
        asyncio.run(_uart_led_client())
    except KeyboardInterrupt:
        # User pressed Ctrl+C
        print("\nProgram terminated by user")
        print("Disconnected")
    except ConnectionError as e:
        # Handle unexpected disconnection
        print(f"\n{e}")
        print("Disconnected")

if __name__ == "__main__":
    main()
