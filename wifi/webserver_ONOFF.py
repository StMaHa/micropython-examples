try:
  import usocket as socket
except:
  import socket
from machine import Pin
from time import sleep


DEBUG =False

def get_webpage(led):
    if led.value() == 1:
        gpio_state="ON"
    else:
        gpio_state="OFF"

    html = """ \
            <html><head><title>Robo Web Server</title> \
                <meta name="viewport" content="width=device-width, initial-scale=1"> \
                <link rel="icon" href="data:,"> \
                <style> \
                    html{font-family: Helvetica;display:inline-block; margin: 0px auto; text-align: center;} \
                    h1{color: #0F3376; padding: 2vh;} \
                    p{font-size: 1.5rem;}.button \
                    {display: inline-block; background-color: #e7bd3b; border: none; \
                    border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;} \
                    .button2{background-color: #4286f4;} \
                </style> \
            </head><body> \
                <h1>ESP Web Server</h1> \
                <p>GPIO state: <strong>""" + gpio_state + """</strong></p> \
                <p><a href="/?led=on"><button class="button">forward</button></a></p> \
                <p><a href="/?led=on"><button class="button">left</button></a></p> \
                <p><a href="/?led=on"><button class="button">right</button></a></p> \
                <p><a href="/?led=off"><button class="button button2">backward</button></a></p> \
            </body></html>"""
    return html


def run_server():
    if DEBUG:
        print("Start web server...")
    led = Pin(15, Pin.OUT)
    led.on()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        if DEBUG:
            print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)
        if DEBUG:
            print('Content = %s' % request)
        led_on = request.find('/?led=on')
        led_off = request.find('/?led=off')
        if led_on == 6:
            if DEBUG:
                print('LED ON')
            led.value(1)
        if led_off == 6:
            if DEBUG:
                print('LED OFF')
            led.value(0)
        response = get_webpage(led)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

if __name__ == "__main__":
    DEBUG = True
    run_server()