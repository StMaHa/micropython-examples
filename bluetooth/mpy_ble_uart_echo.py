"""
Example usage of BLEUART
"""
from ble_uart import BLEUART
from time import sleep

def main():
    """
    Simple echo server demonstrating BLE UART usage.
    
    - Creates a BLE UART peripheral
    - Waits for a central device to connect (blocks in __init__)
    - Sends a welcome message
    - Echoes back any received data
    """

    try:
        # Initialize BLE UART (blocks until a central connects)
        ble_uart = BLEUART()

        # Verify connection is established
        assert ble_uart.is_connected(), "Connection check failed"
        
        # Send welcome message to connected central
        ble_uart.send("Send me a message...")
        
        # Main event loop
        while True:
            msg = ble_uart.read()  # Non-blocking read of receive buffer
            if msg:                # If data was received
                print("Received:", msg)
                # Echo the message back with a prefix
                ble_uart.send("Echo: " + msg)
            sleep(0.1)  # Yield to other tasks
    except KeyboardInterrupt:
        print("Program terminated by user")


if __name__ == "__main__":
    main()


