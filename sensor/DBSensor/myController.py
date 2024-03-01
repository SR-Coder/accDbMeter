import ure
import machine
import time
from htmlTemplates import index, dashboard
import webServerFunctions as wsf
import fileFunctions as ff
import helperFunctions as hf
import flashmsgs



def controller( route, request, serverAddress, client, conn=None):
    isLoggedIn = ff.getIsLoggedIn()
    config = ff.readConfig()
    route = list(route.values())[0]
    page = ""
    # define all the routes here in this function
    # BASE ROUTE '/'
    if route == '/' and not isLoggedIn:
        # page = index()
        return wsf.renderHTML(conn, index())
        
    # LOGIN ROUTE
    elif route == '/login' and not isLoggedIn:
        match = ure.search("username=([^&]*)&password=(.*)", request)
        if match is None:
            flashmsgs.flashMsg['login'] = "Invalid Username or Password"
            return wsf.redirect(conn, serverAddress, '/')
        # version 1.9 compatibility
        try:
            username = match.group(1).decode("utf-8").replace("%3F", "?").replace("%21", "!")
            password = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
        except Exception as e:
            username = match.group(1).replace("%3F", "?").replace("%21", "!")
            password = match.group(2).replace("%3F", "?").replace("%21", "!")
            print('an exception occured in breaking out the password', e)
        password=str(password).strip("'")
        data = {
            "username":username,
            "password":password
        }
        print(data)
        isAuthenticated = wsf.checkAuth(data)
        if isAuthenticated:
            config['isLoggedIn'] = True
            config['thisUser']=username
            config['thisServer'] = serverAddress
            cookieID = ff.generateUUID(32)
            cookieObj = {
                'username': username,
                'id': cookieID,
                'max-age':3600,
                'current-time':time.time()
            }
            ff.saveCookieData()
            ff.updateConfig(config)
            return wsf.redirect(conn, serverAddress, '/dashboard', cookieObj)
        else:
            flashmsgs.flashMsg["login"] = "Invalid Username or Password"
            return wsf.redirect(conn, serverAddress, '/')
    elif route =='/logout':
        ff.setIsloggedIn(False)
        return wsf.redirect(conn, serverAddress, '/')
        pass

    elif route == '/style.css':
        wsf.sendStyleSheet(conn)
        return True
        
    elif route == '/favicon.ico':
        wsf.sendFavicon(conn)
        return True
    elif route == '/favicon.png':
        wsf.sendFavicon(conn)
        return True
    
    # PROTECTED ROUTES
    if not isLoggedIn:
        return wsf.redirect(conn, serverAddress,'/')
    else:
        # RENDER METHODS
        if route == '/dashboard':
            return wsf.renderHTML(conn, dashboard(config))
        
        # ACTION METHODS
        elif route == '/logout':
            ff.setIsloggedIn(False)
            return wsf.redirect(conn, serverAddress, '/')
        
        elif route == '/mqttStop':
            client.disconnect()
            return wsf.redirect(conn, serverAddress, '/dashboard')
        
        elif route == '/mqttStart':
            client.connect()
            return wsf.redirect(conn, serverAddress, '/dashboard')
        
        elif route == '/mqttRestart':
            client.disconnect()
            time.sleep(3)
            client.connect()
            return wsf.redirect(conn, serverAddress, '/dashboard')

        elif route == '/reset':
            ff.setIsloggedIn(False)
            machine.reset()
            return wsf.redirect(conn, serverAddress, '/')
        
        # UPDATE ROUTES (NEED HANDLERS, AND VALIDATIONS)
        elif route == '/update/sensordata':
            currentAuth = ff.readAuthData()
            hPass = None
            data = config
            newPass = ""
            match = ure.search("sensorName=([^&]*)&username=([^&]*)&password=(.*)&confPassword=([^']*)", request)
            # version 1.9 compatibility
            try:
                sensorName = match.group(1).decode("utf-8").replace("%3F", "?").replace("%21", "!")
                username = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
                password = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
                confirmPassword = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
            except Exception as e:
                sensorName = match.group(1).replace("%3F", "?").replace("%21", "!")
                username = match.group(2).replace("%3F", "?").replace("%21", "!")
                password = match.group(3).replace("%3F", "?").replace("%21", "!")
                confirmPassword = match.group(4).replace("%3F", "?").replace("%21", "!")
            
            if password and password != "":
                if confirmPassword:
                    if password == confirmPassword:
                        newPass = hf.hashPasswords(password)
                    else:
                        newPass = currentAuth['passwordH']
                        flashmsgs.flashMsg['password'] = 'Passwords dont match!'
                else: 
                    newPass = currentAuth['passwordH']
                    flashmsgs.flashMsg['confpassword'] = "Please confirm your password."
            else:
                newPass = currentAuth['passwordH']
            if username and username != currentAuth['username']:
                newUsername = username
            else:
                newUsername = currentAuth['username']
            
            # Update auth data
            ff.updateAuthData({newUsername:newPass})

            # Update Config Data
            data["sensorName"] = sensorName
            data["username"] = username
            data['thisUser'] = username

            ff.updateConfig(data)

            return wsf.redirect(conn, serverAddress, '/dashboard')

        elif route == '/update/sensorlocation':
            isValid = True
            match = ure.search("sensorLocation=([^&]*)&units=([^&]*)&xLoc=([+-]?\d+\.?\d*)&yLoc=([+-]?\d+\.?\d*)", request)
            try:
                sensorLocation = match.group(1).decode("utf-8").replace("%3F", "?").replace("%21", "!")
                units = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
                xLoc = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
                yLoc = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
            except Exception as e:
                sensorLocation = match.group(1).replace("%3F", "?").replace("%21", "!").replace("%25", " ").replace('+', " ")
                units = match.group(2).replace("%3F", "?").replace("%21", "!")
                xLoc = match.group(3).replace("%3F", "?").replace("%21", "!")
                yLoc = match.group(4).replace("%3F", "?").replace("%21", "!")
            print("this is the request data for update sensor location: ", request)

            # VALIDATIONS
            if len(sensorLocation) < 4:
                isValid = False
                flashmsgs.flashMsg['sensorLocationMsg'] = "Please enter a valid location name! (> 4 char)"
            if len(units)<1:
                isValid = False
                flashmsgs.flashMsg['unitsMsg'] = "Please enter a valid unit of measure!"
            if not hf.isFloat(xLoc):
                isValid = False
                flashmsgs.flashMsg['xLocMsg'] = "Please enter a valid 'x-location' number (0-999.99)!"
            if not hf.isFloat(yLoc):
                isValid = False
                flashmsgs.flashMsg['yLocMsg'] = "Please enter a valid 'y-location' number (0-999.99)!"

            if isValid:
                data = config
                data['sensorLocation'] = sensorLocation
                data['units'] = units
                data['xLoc'] = xLoc
                data['yLoc'] = yLoc

                ff.updateConfig(data)

            return wsf.redirect(conn, serverAddress, '/dashboard')

        elif route == '/update/mqttsettings':
            isValid = True
            # fix the last regex
            match = ure.search("mqttClientID=([^&]*)&mqttAddress=([^&]*)&mqttPort=([[+-]?\d+\.?\d*)&mqttUsername=([^&]*)&mqttPassword=(.*)&mqttRate=(\d+\.?\d*)", request)
            try:
                mqttClientID = match.group(1).decode("utf-8").replace("%3F", "?").replace("%21", "!").replace("%25", " ").replace('+', " ")
                mqttAddress = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!").replace("%3A", ":").replace('%2F', '/')
                mqttPort = match.group(3).decode("utf-8").replace("%3F", "?").replace("%21", "!")
                mqttUsername = match.group(4).decode("utf-8").replace("%3F", "?").replace("%21", "!")
                mqttPassword = match.group(5).decode("utf-8").replace("%3F", "?").replace("%21", "!")
                mqttRate = match.group(6).decode("utf-8").replace("%3F", "?").replace("%21", "!")
            except Exception as e:
                mqttClientID = match.group(1).replace("%3F", "?").replace("%21", "!").replace("%25", " ").replace('+', " ")
                mqttAddress = match.group(2).replace("%3F", "?").replace("%21", "!").replace("%3A", ":").replace('%2F', '/')
                mqttPort = match.group(3).replace("%3F", "?").replace("%21", "!")
                mqttUsername = match.group(4).replace("%3F", "?").replace("%21", "!")
                mqttPassword = match.group(5).replace("%3F", "?").replace("%21", "!")
                mqttRate = match.group(6).replace("%3F", "?").replace("%21", "!")

            # VALIDATIONS
            print("PRE VALIDATION:", mqttRate)
            if len(mqttClientID) < 4:
                flashmsgs.flashMsg['mqttClientID'] = "MQTT Client ID must be longer than 4 characters!"
                isValid = False
            try:
                int(mqttAddress[0])
                print(mqttAddress[0])
                if not hf.isValidIPv4(mqttAddress):
                    flashmsgs.flashMsg['mqttAddress'] = 'Not a valid IPv4 address'
                    isValid = False
            except:
                if not hf.isValidURL(mqttAddress):
                    flashmsgs.flashMsg['mqttAddress'] = "Not a valid url, must start with 'http', or 'https'"
                    isValid = False
            if not ure.match('[1-10000]', mqttPort):
                flashmsgs.flashMsg['mqttPort'] = "Not a valid port number, must be an integer!"
                isValid = False
            if len(mqttUsername) < 4 and len(mqttUsername)>0:
                flashmsgs.flashMsg['mqttUsername'] = "Username must be longer than 4 characters!"
                isValid = False
            if len(mqttPassword)<8 and len(mqttPassword)>0:
                flashmsgs.flashMsg['mqttPassword'] = "Password must be greater that 8 characters!"
                isValid = False
            if not ure.match('[1-60000]', mqttRate):
                flashmsgs.flashMsg['mqttRate'] = "MQTT message rate must be between 1 and 60000!"
                isValid = False
            
            if isValid:
                print(mqttPassword ,mqttRate)
                data = config
                config['mqttClientID'] = mqttClientID 
                config['mqttAddress'] = mqttAddress 
                config['mqttPort'] = mqttPort 
                config['mqttUsername'] = mqttUsername 
                config['mqttPassword'] = mqttPassword 
                config['mqttRate'] = mqttRate 

                ff.updateConfig(data)
            
            
            print("this is the request data for update mqtt settings: ", request)
            return wsf.redirect(conn, serverAddress, '/dashboard')
        
        
        elif route == '/favicon.ico':
            wsf.sendFavicon(conn)
            return True
        elif route == '/favicon.png':
            wsf.sendFavicon(conn)
            return True
        elif route == '/style.css':
            wsf.sendStyleSheet(conn)
            return True

        else:
            print('route not found')
            return wsf.redirect(conn, serverAddress, '/dashboard')
