import ure
import machine
import time
from htmlTemplates import index, dashboard
import webServerFunctions as wsf
import fileFunctions as ff
import helperFunctions as hf
import flashmsgs



def controller(recDict, serverAddress, client, conn=None):
    # serverAddress, we can still pass that 
    # client = mqttClient
    # conn = connection

    cookies = recDict['Cookie']
    route = recDict['Path']

    # Only check cookies for valid routes
    if route != "/favicon.ico" or route != "/style.css":
        isValidCookie = wsf.checkCookies(cookies)

    # Get the configuration from file
    config = ff.readConfig()

    # define all the routes here in this function
    # BASE ROUTE '/'
    if route == '/' and not isValidCookie:
        # page = index()
        return wsf.renderHTML(conn, index())
        
    # LOGIN ROUTE
    elif route == '/login' and not isValidCookie:
        try:
            up = recDict['Post']
            username = up['username']
            password = up['password']
        except:
            flashmsgs.flashMsg['login'] = "Invalid Username or Password"
            return wsf.redirect(conn, serverAddress, '/')
        data = {
            "username":username,
            "password":password
        }
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
            ff.saveCookieData(cookieObj)
            ff.updateConfig(config)
            return wsf.redirect(conn, serverAddress, '/dashboard', cookieObj)
        else:
            flashmsgs.flashMsg["login"] = "Invalid Username or Password"
            return wsf.redirect(conn, serverAddress, '/')
    
    # LOGOUT ROUTE
    elif route =='/dashboard/logout':
        ff.setIsloggedIn(False)
        ff.clearCookies()
        return wsf.redirect(conn, serverAddress, '/')
        pass

    # RETURNS STYLE SHEETS AND IMAGES
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
    if not isValidCookie:
        return wsf.redirect(conn, serverAddress,'/')
    else:
        # RENDER METHODS
        if route == '/dashboard':
            return wsf.renderHTML(conn, dashboard(config))
        
        # ACTION METHODS
        elif route == '/dashboard/logout':
            ff.setIsloggedIn(False)
            ff.clearCookies()
            return wsf.redirect(conn, serverAddress, '/')
        
        elif route == '/dashboard/mqttStop':
            client.disconnect()
            return wsf.redirect(conn, serverAddress, '/dashboard')
        
        elif route == '/dashboard/mqttStart':
            client.connect()
            return wsf.redirect(conn, serverAddress, '/dashboard')
        
        elif route == '/dashboard/mqttRestart':
            client.disconnect()
            time.sleep(3)
            client.connect()
            return wsf.redirect(conn, serverAddress, '/dashboard')

        elif route == '/dashboard/reset':
            ff.setIsloggedIn(False)
            machine.reset()
            return wsf.redirect(conn, serverAddress, '/')
        
        # UPDATE ROUTES 
        elif route == '/dashboard/update/sensordata':
            currentAuth = ff.readAuthData()
            data = config
            newPass = ""
            try:
                postData = recDict['Post']
                sensorName = postData['sensorName'].replace('+', " ")
                username = postData['username']
                password = postData['password']
                confirmPassword = postData['confPassword']
            except Exception as e:
                print('Something went wrong! ', e)
            
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
            
            ff.updateAuthData({newUsername:newPass})

            data["sensorName"] = sensorName
            data["username"] = username
            data['thisUser'] = username

            ff.updateConfig(data)

            return wsf.redirect(conn, serverAddress, '/dashboard')

        elif route == '/dashboard/update/sensorlocation':
            isValid = True
            try:
                postData = recDict['Post']
                sensorLocation = postData['sensorLocation'].replace('+', " ")
                units = postData['units']
                xLoc = postData['xLoc']
                yLoc = postData['yLoc']
            except Exception as e:
                print('Something went wrong! ',e)
                flashmsgs.flashMsg['sensorLocationMsg'] = "Something went wrong submitting this request"
                return wsf.redirect(conn, serverAddress, '/dashboard')

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

        elif route == '/dashboard/update/mqttsettings':
            isValid = True
            try:
                postData = recDict['Post']
                mqttClientID = postData['mqttClientID'].replace('+', " ")
                mqttAddress = postData['mqttAddress']
                mqttPort = postData['mqttPort']
                mqttRate = postData['mqttRate']
            except Exception as e:
                print('something went wrong! ', e)

            # VALIDATIONS
            if len(mqttClientID) < 4:
                flashmsgs.flashMsg['mqttClientID'] = "MQTT Client ID must be longer than 4 characters!"
                isValid = False
            try:
                int(mqttAddress[0])
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
            if not ure.match('[1-60000]', mqttRate):
                flashmsgs.flashMsg['mqttRate'] = "MQTT message rate must be between 1 and 60000!"
                isValid = False
            
            if isValid:
                data = config
                data['mqttClientID'] = mqttClientID 
                data['mqttAddress'] = mqttAddress 
                data['mqttPort'] = mqttPort 
                data['mqttRate'] = mqttRate 
                ff.updateConfig(data)
            return wsf.redirect(conn, serverAddress, '/dashboard')
        
        elif route == '/dashboard/update/mqttpass':
            isValid = True
            try:
                postData = recDict['Post']
                mqttUsername = postData['mqttUsername']
                mqttPassword = postData['mqttPassword']
                mqttConfPassword = postData['mqttConfPassword']
            except Exception as e:
                print('something went wrong! ', e)
                return wsf.redirect(conn, serverAddress, '/dashboard')

            if len(mqttUsername) < 4 and len(mqttUsername)>0:
                flashmsgs.flashMsg['mqttUsername'] = "Username must be longer than 4 characters!"
                isValid = False
            if len(mqttPassword)<8 and len(mqttPassword)>0:
                flashmsgs.flashMsg['mqttPassword'] = "Password must be greater that 8 characters!"
                isValid = False
            if mqttPassword != mqttConfPassword:
                flashmsgs.flashMsg['mqttPassword'] = "Passwords must match!"
                isValid = False

            if isValid:
                data = config
                data['mqttUsername'] = mqttUsername
                data['mqttPassword'] = mqttPassword
                ff.updateConfig(data)
            return wsf.redirect(conn, serverAddress, '/dashboard')

        else:
            print('(WARNING)(controller) Route Not Found!')
            return wsf.redirect(conn, serverAddress, '/dashboard')
