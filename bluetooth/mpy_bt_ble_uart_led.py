from machine import Pin, UART
from time import sleep

# Bluetooth - UART adapter
# - JDY-31:    BT CLassic only
# - JDY-33:    BT CLassic and BLE

UART_ID = 0            # Use UART0 (pins GP0=TX, GP1=RX by default)
TX_PIN = 0             # GP0 -> RX JDY-31
RX_PIN = 1             # GP1 -> TX JDY-31
BAUD_RATE = 9600       # 9600 is default


def send_cmd(cmd):
    response = None
    uart.write(cmd + "\r\n")
    sleep(0.5)
    if uart.any():
        response = uart.read().decode().strip()
        print("TX:", response)
    return response


uart = UART(UART_ID, baudrate=BAUD_RATE, tx=Pin(TX_PIN), rx=Pin(RX_PIN))
led = Pin("LED", Pin.OUT)

enable_loop = True
send_cmd("AT+VERSION")
send_cmd("AT+LADDR")
send_cmd("AT+BAUD")
name1 = send_cmd("AT+NAME")
name2 = send_cmd("AT+NAMB")

if name1 and name2:
    name1 = name1.split('=')[1]
    name2 = name2.split('=')[1]
    print(f"\nNow connect to BT-UART adapter '{name1}' or '{name2}'.")
elif name1:
    name1 = name1.split('=')[1]
    print(f"\nNow connect to BT-UART adapter '{name1}'.")
else:
    uart.deinit()
    enable_loop = False
    print("ERROR! UART is not working as expected.")

try:
    while enable_loop:
      if uart.any() > 0:             # check if received anything
        data = uart.read()           # read from UART
        data = data.strip()          # remove white spaces and line breaks
        data = data.decode('utf-8')  # convert bytes to string as UTF-8
        data = data.lower()          # convert to lower case

        print("RX:", data)

        if ("on" in data) or ("1" == data):
          led.on()
          print('LED on')
          uart.write('LED is on\n')
        elif ("off" in data) or ("0" == data):
          led.off()
          print('LED off')
          uart.write('LED is off\n')
except KeyboardInterrupt:
    print("Program terminated by user")
finally:
    uart.deinit()