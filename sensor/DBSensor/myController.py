import ure
import machine
import time
from htmlTemplates import index, dashboard
import webServerFunctions as wsf
import fileFunctions as ff

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
            # page = index("Invalid Username or Password (POST)")
            return wsf.redirect(conn, serverAddress, '/', "invalid username or password")
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
            ff.updateConfig(config)
            return wsf.redirect(conn, serverAddress, '/dashboard')
        else:
            return wsf.redirect(conn, serverAddress, '/')
    elif route =='/logout':
        ff.setIsloggedIn(False)
        return wsf.redirect(conn, serverAddress, '/')
        pass

    elif route == '/style.css':
        wsf.sendStyleSheet(conn)
        return True
        
    elif route == '/favicon.ico':
        print('no favicon')
        return False
    
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
            hPass = None
            data = config
            match = ure.search("sensorName=([^&]*)&username=([^&]*)&password=(.*)&confPassword=([^']*)", request)
            # version 1.9 compatibility
            try:
                sensorName = match.group(1).decode("utf-8").replace("%3F", "?").replace("%21", "!")
                username = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
                password = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
                confirmPassword = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
            except Exception as e:
                sensorName = match.group(1)  #.replace("%3F", "?").replace("%21", "!")
                username = match.group(2)  #.replace("%3F", "?").replace("%21", "!")
                password = match.group(3)  #.replace("%3F", "?").replace("%21", "!")
                confirmPassword = match.group(4)  #.replace("%3F", "?").replace("%21", "!")

            # NEED TO WRITE THIS TO THE SECRETS FILE NOT THE USER DATA SET
            if password:
                if confirmPassword:
                    if password == confirmPassword:
                        hPass = wsf.hashPasswords(password)

            data["sensorName"] = sensorName
            data["username"] = username
            data['thisUser'] = username


            print("New Data set: ", data)

            ff.updateConfig(data)

            return wsf.redirect(conn, serverAddress, '/dashboard')

        elif route == '/update/sensorlocation':
            print("this is the request data for update sensor location: ", request)
            return wsf.redirect(conn, serverAddress, '/dashboard')

        elif route == '/update/mqttsettings':
            print("this is the request data for update mqtt settings: ", request)
            return wsf.redirect(conn, serverAddress, '/dashboard')
        
        elif route == '/favicon.ico':
            print('no favicon')
            return False
        
        elif route == '/style.css':
            wsf.sendStyleSheet(conn)
            return True

        else:
            print('route not found')
            return wsf.redirect(conn, serverAddress, '/dashboard')
