import json
import time
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
        print("(readConfig)error in reading config: ", e)
        return False

def createConfig(data: dict=None):
        config = readConfig()
        defaultConfig = config
        # print("(createConfig)Configuration loaded!: ",config)
        if not config:
            print('(createConfig)No Config File Found Loading Default!')
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
                    'c-timeout':30,
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
                    'c-timeout':30,
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
        print('(updateConfig)Error occured writing Data')
        return False

def clearConfig():
    pass

def setIsloggedIn(state):
    try:
        config = readConfig()
        config['isLoggedIn'] = state
        # print(config)
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
        print("(getIsLoggedIn)Something went wrong getting state: ",e)
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
            print('(writeAuthData)Error writing hash')
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

        # print(lines)
        with open(SECRETS, "w") as f:
            f.write(lines)
        return True
    except OSError as e:
        print("(updateAuthData)Something Went wrong updating Auth: ", e)
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

def saveCookieData(cookie:dict):
    '''
        Accepts a cookie object at login and writes it to the 
        cookie file, only write auth cookies here. Its a good idea
        to make the max age relatively short as this is a hack.
        - username
        - id
        - max-age
        - current-time
    '''
    try:
        with open('cookies.dat','a', encoding='utf-8') as f:
            f.write(f'{str(cookie)}\r')
        return True
    except OSError as e:
        print("(saveCookieData)unable to write cookie data: ", e)
        return False


# COOKIE HANDLING
def getOneCookie(username:str, id:str=None):
    try:
        cookieString = ""
        with open('cookies.dat', 'r') as f:
            cookieString = f.read()
        cookieList = cookieString.split('\r')
        for cookie in cookieList:
            try:
                cookie = eval(str(cookie))
                if id is not None:
                    if cookie['id'] == id and cookie['username'] == username:
                        return cookie
                else:
                    return False
            except Exception as e:
                print("(getOneCookie)something went wrong converting string to dict --> ", e)
                return False
                pass
    except OSError as e:
        print('(getOneCookie)something went wrong retriving your cookie: ', e)
        return False

def expireCookies():
    try:
        now = time.time()
        cookieString = ""
        newCookieList = []
        with open('cookies.dat', 'r') as f:
            cookieString = f.read()
        cookieList = cookieString.split('\r')
        if len(cookieList)>0:
            for cookie in cookieList:
                if cookie != "":
                    try:
                        temp = eval(str(cookie))
                        # print(f'The current time is: {now}, the age is {temp['current-time'] + temp['max-age']}, the difference is:', now - (temp['current-time'] + temp['max-age']))
                        if temp['current-time'] + temp['max-age'] > now:
                            newCookieList.append(temp)
                    except Exception as e:
                        print("(expireCookies)Something went wrong converting string to dict --> ", e)
                        return False
            with open('cookies.dat','w', encoding='utf-8') as f:
                for newCookie in newCookieList:
                    f.write(f'{newCookie}\r')
            return True
        else:
            return False    
    except OSError as e:
        print("(expireCookies)something went wrong expiring the cookie: ", e)
        return False

def clearCookies():
    with open('cookies.dat', 'w') as f:
        f.write("")
    return True