import network
import binascii
from machine import Pin
from time import sleep

DEBUG = False
led_onboard = 15
ssid = 'mySSID'
passwd = 'myPassword'

def setup_wifi():
    led = Pin(led_onboard, Pin.OUT)
    if DEBUG:
        print("Setup wireless network...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)       # activate the interface
    mac_bytes = wlan.config('mac')
    mac_str = binascii.hexlify(mac_bytes, ':').decode()
    if DEBUG:
        print('Network config:')
        print(" - Phys. Address :", mac_str)
    if not wlan.isconnected():
        if DEBUG:
            print('Connecting to network...')
        wlan.connect(ssid, passwd)
        while not wlan.isconnected():
            led.value(not led.value())
            sleep(0.1)
            pass
    network_config = wlan.ifconfig()
    if DEBUG:
        print(' - IP Address    :', network_config[0])
        print(' - Subnet Mask   :', network_config[1])
        print(' - Def. Gateway  :', network_config[2])
        print(' - DNS Server    :', network_config[3])


if __name__ == "__main__":
    DEBUG = True
    setup_wifi()