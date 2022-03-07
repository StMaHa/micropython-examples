import network
import binascii

ssid = 'YourWifiName'
passwd = 'YourPassword'

def setup_wifi():
    print("Setup wireless network...")
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)       # activate the interface
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, passwd)
        while not wlan.isconnected():
            pass
    network_config = wlan.ifconfig()
    print('Network config:')
    print(' - IP Address    :', network_config[0])
    print(' - Subnet Mask   :', network_config[1])
    print(' - Def. Gateway  :', network_config[2])
    print(' - DNS Server    :', network_config[3])
    mac_bytes = wlan.config('mac')
    mac_str = binascii.hexlify(mac_bytes, ':').decode()
    print(" - Phys. Address :", mac_str)


if __name__ == "__main__":
    setup_wifi()