from machine import Pin, UART
from time import sleep

# Bluetooth - UART adapter
# - JDY-31:    BT CLassic only
# - JDY-33:    BT CLassic and BLE

BAUD_RATE_4 = 9600
BAUD_RATE_8 = 115200

UART_ID = 0                   # Use UART0 (pins GP0=TX, GP1=RX by default)
TX_PIN = 0                    # GP0 -> RX JDY-31
RX_PIN = 1                    # GP1 -> TX JDY-31
BAUD_RATE_INIT = BAUD_RATE_4  # 9600 is default

READ_ONLY = True

BAUD_RATE_NEW = BAUD_RATE_4
BT_NAME_NEW = "JDY-33-SPP"
BLE_NAME_NEW = "JDY-33-BLE"

uart = UART(UART_ID, baudrate=BAUD_RATE_INIT, tx=Pin(TX_PIN), rx=Pin(RX_PIN))
led = Pin("LED", Pin.OUT)


def send_cmd(cmd):
    response = None
    uart.write(cmd + "\r\n")
    sleep(0.5)
    if uart.any():
        response = uart.read().decode().strip()
        print("TX:", response)
    return response

print("Be sure, nothing is connected to this BT-UART adapter.\n")

if not READ_ONLY:
    # Utilize AT mode of JDY-31 BT-UART adapter
    print("Change baudrate and name.")
    if send_cmd("AT+VERSION"):
        send_cmd("AT+LADDR")
        send_cmd("AT+NAME" + BT_NAME_NEW)
        send_cmd("AT+NAMB" + BLE_NAME_NEW)
        send_cmd("AT+BAUD")
        if BAUD_RATE_NEW != BAUD_RATE_INIT:
            if BAUD_RATE_NEW == BAUD_RATE_8:
                send_cmd("AT+BAUD8")  # change baudrate to 115200
            if BAUD_RATE_NEW == BAUD_RATE_4:
                send_cmd("AT+BAUD4")  # change baudrate to 115200
        send_cmd("AT+RESET")
        send_cmd("AT+DISC")
    else:
        print("ERROR! Cannot connect to inital UART.")
    # Switch to new baudrate
    uart.deinit()
    uart = UART(UART_ID, baudrate=BAUD_RATE_NEW, tx=Pin(TX_PIN), rx=Pin(RX_PIN))
    print(uart)

if send_cmd("AT+VERSION"):
    send_cmd("AT+LADDR")    # MAC
    send_cmd("AT+BAUD")     # Baudrate
    send_cmd("AT+UUIDLEN")
    send_cmd("AT+SVRUUID")
    send_cmd("AT+CHRUUID")  # READ, WRITE, NOTIFY
    send_cmd("AT+CRXUUID")  # WRITE, WRITE_WITHOUT_RESPONSE
    send_cmd("AT+NAME")     # BT CLassic name
    send_cmd("AT+NAMB")     # BLE name
else:
    print("ERROR! Cannot connect to UART.")
uart.deinit()
