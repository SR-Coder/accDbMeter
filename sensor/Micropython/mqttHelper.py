import simple
import time
import machine
MQTTClient = simple.MQTTClient

# CREATE A CONFIG FILE 
_PORT = 1885
_MQTT_SERVER = "192.168.1.93"
_CLIENT_ID = "DBSensor1"
_TOPIC_PUB = b'ACC DB sensor'
_TOPIC_MSG = b'TEST'

def mqttConnect(clientID:str, mqttServer:str, port:int, keepAlive:int):
    # client = MQTTClient(_CLIENT_ID, _MQTT_SERVER, _PORT, keepalive=3600)
    client = MQTTClient(clientID, mqttServer, port, keepalive=keepAlive)
    client.connect()
    print('\rConnected to %s MQTT Broker' %(mqttServer))
    return client

def mqttReconnect():
    print('Failed to Connect to the MQTT Broker. Reconnecting...')
    for i in range(100):
        print(".", end='')
    print("resetting sensor")
    machine.reset()


def startMqttClient(clientID:str, mqttServer:str, port:int, keepAlive:int=3600):
    try: 
        client = mqttConnect(clientID, mqttServer, port, keepAlive)
        return client
    except OSError as e:
        print("An Error was encountered... reconnecting...", e)
        time.sleep(3)
        mqttReconnect()
