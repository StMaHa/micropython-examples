from jdy33_uart import BtUartAdapter

UART_ID = 0            # Use UART0 (pins GP0=TX, GP1=RX by default)
TX_PIN = 12            # GP0 -> RX JDY-31/33
RX_PIN = 13            # GP1 -> TX JDY-31/33

#bt_uart_adapter = BtUartAdapter(tx_pin=TX_PIN, rx_pin=RX_PIN)

#bt_uart_adapter.send_cmd("AT+NAMEJDY-33-SPP-00")
#bt_uart_adapter.send_cmd("AT+NAMBJDY-33-BLE-00")

#bt_uart_adapter.info()
