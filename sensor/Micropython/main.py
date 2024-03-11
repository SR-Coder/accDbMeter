import wifimgr     # importing the Wi-Fi manager library
from time import sleep     
import machine
import gc
import time
import _thread
import htmlTemplates
import webServerFunctions as wsf
import sys
from mqttHelper import mqttConnect, mqttReconnect, startMqttClient, _TOPIC_PUB, _TOPIC_MSG
import fileFunctions as ff
import helperFunctions as hf
from myController import controller

global run_core_1
run_core_1 = False


global termSig
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
    serverAddress = wlan.ifconfig()
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
    s.close()
    for i in range(10):
        print(".", end='')
        time.sleep(.1)

s.bind(host_addr)
s.listen(5)


print("Waiting for connections")
for i in range(50):
    print(".", end="")
    
    time.sleep(.1)


print('Checking Auth Configurations...')
data = {
    'sensorAddress':wlan.ifconfig()[0],
}
wsf.configAuth()
ff.clearCookies()
ff.createConfig(data)

configData = ff.readConfig()

print("Connecting to Mqtt Server...")
mqttClientID = configData['mqttClientID']
mqttServer = configData['mqttAddress']
mqttPort = int(configData['mqttPort'])
print(f'The MQTT Client ID is: {mqttClientID}, the Server Address is: {mqttServer}, and the Port is: {mqttPort}!')
client = startMqttClient(configData['mqttClientID'], configData['mqttAddress'], int(configData['mqttPort']))

# print("checking out the Mqtt Client obj: ", client.__dict__)

ledPin = False
# Main While loop for doing stuff 



prevTime = time.time()
cookieTimeout = configData['c-timeout']
run_core_1 = True
# s.setblocking(False)
while True:

    # Check for expired cookies
    now = time.time()
    if now > (prevTime + cookieTimeout):
        ff.expireCookies()
        prevTime = now

    try:
        # FREE FRAGEMENTED MEM
        if gc.mem_free() < 102000:
            gc.collect()
    
        conn, addr = s.accept()
        
        conn.settimeout(3.0)
        request = conn.recv(1024)
        conn.settimeout(None)
        recDict = wsf.parseRequest(request)
        response = controller(recDict, serverAddress, client, conn)
        conn.close()

    except OSError as e:
        # ON ERROR CLOSE CLIENT CONN
        print('Connection closed',e)

    except KeyboardInterrupt:
        # ON QUIT CLEAN UP
        print("received ctrl-c")
        print("cleaning up")
        config = ff.readConfig()
        config['isLoggedIn'] = False
        ff.updateConfig(config)
        ff.clearCookies()
        s.close()
        led0.off()
        led1.off()
        led.off()
        sys.exit()
    


