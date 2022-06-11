import wifi_client as wifi
import webserver
from machine import Pin

wifi.setup_wifi()
led = Pin(15, Pin.OUT)
led.off()
webserver.run_server()
