import json
import random

def generateUUID(length):
    letters = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def readConfig():
    try:
        with open("config.json",'r') as file:
            data = json.load(file)  
        return data
    except OSError as e:
        print("error in reading config: ", e)
        return False

def createConfig():
        config = readConfig()
        print("Configuration loaded!: ",config)
        if not config:
            print('No Config File Found Loading Default!')
            defaultConfig = {
                # state information
                'isLoggedIn':False,
                'thisUser':"",
                'sensorName':generateUUID(32),
                # Other information
                'mqttServer':'192.168.1.93'
            }
            with open("config.json", "w") as file:
                json.dump(defaultConfig, file)
            return False
        return True

def updateConfig(data: dict):
    try:
        with open('config.json', 'w') as file:
            json.dump(data, file)
        return True
    except OSError as e:
        print('Error occured writing Data')
        return False

def clearConfig():
    pass

def setIsloggedIn(state):
    try:
        config = readConfig()
        config['isLoggedIn'] = state
        print(config)
        updateConfig(config)
        return True
    except OSError as e:
        print("Something went wrong setting state: ",e)
        return False

def getIsLoggedIn():
    try:
        config = readConfig()
        return config['isLoggedIn']
    except OSError as e:
        print("Something went wrong getting state: ",e)
        return False