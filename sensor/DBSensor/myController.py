import ure
from htmlTemplates import index, dashboard
import webServerFunctions as wsf
import fileFunctions as ff

def controller( route, request, serverAddress, conn=None):
    route = list(route.values())[0]
    page = ""
    # define all the routes here in this function
    # BASE ROUTE '/'
    if route == '/':
        # page = index()
        return wsf.renderHTML(conn, index())
        
    # LOGIN ROUTE
    elif route == '/login':
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
            config = ff.readConfig()
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
        
    elif route == '/favicon.ico':
        print('no favicon')
        return False
    
    # PROTECTED ROUTES
    if not ff.getIsLoggedIn():
        return wsf.redirect(conn, serverAddress,'/')
    else:
        if route == '/dashboard':
            return wsf.renderHTML(conn, dashboard())
        
        elif route == '/logout':
            ff.setIsloggedIn(False)
            return wsf.redirect(conn, serverAddress, '/')
        
        else:
            print('route not found')
            return wsf.redirect(conn, serverAddress, '/')
