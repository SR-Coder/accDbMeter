import wifimgr     # importing the Wi-Fi manager library
from time import sleep     
import machine
import gc
import time
import htmlTemplates
import webServerFunctions
import sys


try:
    import usocket as socket
except:
    import socket
# machine.reset()

led0 = machine.Pin(0,machine.Pin.OUT)
led1 = machine.Pin(1,machine.Pin.OUT)
led = machine.Pin(2, machine.Pin.OUT)
wlan = wifimgr.get_connection()        #initializing wlan
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        led1.on()
        time.sleep(0.5)
        led1.off()
        time.sleep(.2)
        pass  
print(" Raspberry Pi Pico W OK")
if wlan:
    led1.on()
led_state = "OFF"
def web_page():
    html = htmlTemplates.htmlPage1(led_state)
    return html

host_addr = socket.getaddrinfo('0.0.0.0',80)[0][-1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    s.bind(host_addr)
except:
    print("Unable to bind closing all sockets!")

    for i in range(10):
        print(".", end='')
        time.sleep(.1)

s.bind(host_addr)
s.listen(5)

# Main While loop for doing stuff 
while True:
    
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        typeAndRoute = webServerFunctions.getReqTypeAndRoute(request)
        print(request)
        print('GET Request Content = %s' % request)
        led_on = request.find('/?led_2_on')
        led_off = request.find('/?led_2_off')
        if led_on == 6:
            print('LED ON -> GPIO2')
            led_state = "ON"
            led.on()
        if led_off == 6:
            print('LED OFF -> GPIO2')
            led_state = "OFF"
            led.off()
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except OSError as e:
        conn.close()
        print('Connection closed')

    except KeyboardInterrupt:
        print("received ctrl-c")
        print("cleaning up")
        conn.close()
        led0.off()
        led1.off()
        led.off()
        sys.exit()
