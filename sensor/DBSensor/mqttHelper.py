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

def mqttConnect():
    client = MQTTClient(_CLIENT_ID, _MQTT_SERVER, _PORT, keepalive=3600)
    client.connect()
    print('Connected to %s MQTT Broker' %(_MQTT_SERVER))
    return client

def mqttReconnect():
    print('Failed to Connect to the MQTT Broker. Reconnecting...')
    for i in range(100):
        print(".", end='')
    print("resetting sensor")
    machine.reset()


def startMqttClient():
    try: 
        client = mqttConnect()
        return client
    except OSError as e:
        print("An Error was encountered... reconnecting...", e)
        time.sleep(3)
        mqttReconnect()
