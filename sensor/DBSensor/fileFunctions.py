import json
import random
import helperFunctions as hf
SECRETS = 'secrets.dat'

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

def createConfig(data: dict=None):
        config = readConfig()
        defaultConfig = config
        print("Configuration loaded!: ",config)
        if not config:
            print('No Config File Found Loading Default!')
            if data == None:
                defaultConfig = {
                    # sensor information
                    'isLoggedIn':False,
                    'thisUser':"root",
                    'username':'root',
                    'sensorName':generateUUID(32),
                    'sensorAddress':"",
                    'sensorLocation':"Default Location",
                    'xLoc': 0,
                    'yLoc': 0,
                    # Other information
                    'mqttAddress':'192.168.1.93',
                    'mqttPort':'1885',
                    'mqttClientID':"DefaultName",
                    'mqttUsername': "",
                    'mqttPassword': "",
                    'mqttRate':"60"
                }
            else:
                defaultConfig = {
                    # sensor information
                    'isLoggedIn':False,
                    'thisUser':"root",
                    'username':'root',
                    'sensorName':generateUUID(32),
                    'sensorAddress':data['sensorAddress'],
                    'sensorLocation':"Default Location",
                    'xLoc': 0,
                    'yLoc': 0,
                    # Other information
                    'mqttAddress':'192.168.1.93',
                    'mqttPort':'1885',
                    'mqttClientID':"DefaultName",
                    'mqttUsername': "",
                    'mqttPassword': "",
                    'mqttRate':"60"
                }
            with open("config.json", "w") as file:
                json.dump(defaultConfig, file)
            return False
        defaultConfig['isLoggedIn'] = False
        with open("config.json", "w") as file:
            json.dump(defaultConfig, file)
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
    
def writeAuthData(data: dict):
    '''This method accepts a single line dictionary 
    where the key is the username and the valuse is 
    the password'''
    lines = ""
    for username, password in data.items():
        hash = hf.hashPasswords(password)
        if hash:
            lines = f'{username}:{hash}'
        else:
            print('Error writing hash')
            return False
    with open(SECRETS, "w") as f:
        f.write(lines)
    return True

def updateAuthData(data:dict):
    '''This method accepts a dict but unlike write auth 
    data does not hash the password it just writes it.  
    This is helpful when updating the username but not 
    the password.  USE CAUTION TO NOT WRIT PLAIN PASSWORDS 
    TO THE SECRETS DAT'''
    lines = ""
    try:
        for username, password in data.items():
            lines = f'{username}:{password}'

        print(lines)
        with open(SECRETS, "w") as f:
            f.write(lines)
        return True
    except OSError as e:
        print("Something Went wrong updating Auth: ", e)
        return False

def readAuthData():
    '''
    This method takes 0 positional arguments. It reades the 
    "SECRETS" file and returns a dictionary with two keys:
    - username
    - passwordH
    
    this is the authentication data for the registered user
    the password returned should always be hashed, take care
    to implement the updateauthdata to not write plain passwords!
    '''
    username = ""
    passwordH = ""
    with open(SECRETS) as f:
        line = f.read()
    username, passwordH = line.strip("\n").split(":")
    return {
        "username": username,
        "passwordH": passwordH
    }

def removeAuthtData():
    with open(SECRETS, "w") as f:
        f.write("")

