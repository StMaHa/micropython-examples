from machine import Pin, UART
from time import sleep

# Bluetooth - UART adapter
# - JDY-31:    BT CLassic only
# - JDY-33:    BT CLassic and BLE

UART_ID = 0            # Use UART0 (pins GP0=TX, GP1=RX by default)
TX_PIN = 0             # GP0 -> RX JDY-31/33
RX_PIN = 1             # GP1 -> TX JDY-31/33
BAUD_RATE = 9600       # 9600 is default

BAUD_DICT = {
    "4" : 9600
}

class BtUartAdapter:
    def __init__(self, uart_id=UART_ID, baudrate=BAUD_RATE, tx_pin=TX_PIN, rx_pin=RX_PIN):
        self.uart = UART(uart_id, baudrate=baudrate, tx=Pin(tx_pin), rx=Pin(rx_pin))

    def send_cmd(self, cmd):
        response = None
        key = None
        value = None
        self.uart.write(cmd + "\r\n")
        sleep(0.5)
        if self.uart.any():
            response = self.uart.read().decode().strip()

        if response:
            if "=" in response:
                key, value = response.split("=")
            elif response.lower() == "ok":
                key = cmd
                value = response

        return key, value

    def info(self):
        at_cmd, value = self.send_cmd("AT+VERSION")
        if at_cmd and value:
            print(f"{at_cmd}={value}")

        at_cmd, value = self.send_cmd("AT+LADDR")
        if at_cmd and value:
            print(f"{at_cmd}={value}")

        at_cmd, value = self.send_cmd("AT+BAUD")
        if at_cmd and value:
            print(f"{at_cmd}={BAUD_DICT[value]}")

        at_cmd, name1 = self.send_cmd("AT+NAME")
        at_cmd, name2 = self.send_cmd("AT+NAMB")

        if name1 and name2:
            print(f"\nConnect to BT-UART adapter '{name1}' or '{name2}'.")
        elif name1:
            print(f"\nConnect to BT-UART adapter '{name1}'.")
        else:
            self.uart.deinit()
            print("WARNING! BT-UART adapter is not connected.")


if __name__ == "__main__":
    UART_ID = 0            # Use UART0 (pins GP0=TX, GP1=RX by default)
    TX_PIN = 12            # GP0 -> RX JDY-31/33
    RX_PIN = 13            # GP1 -> TX JDY-31/33

    bt_uart_adapter = BtUartAdapter(tx_pin=TX_PIN, rx_pin=RX_PIN)

    #bt_uart_adapter.send_cmd("AT+NAMEJDY-33-SPP-00")
    #bt_uart_adapter.send_cmd("AT+NAMBJDY-33-BLE-00")

    bt_uart_adapter.info()
