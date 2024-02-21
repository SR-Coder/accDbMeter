import ure
from htmlTemplates import index, dashboard
import webServerFunctions as wsf

def controller(req, data):
    route = list(req.values())[0]
    req = route
    page = ""
    # define all the routes here in this function
    # BASE ROUTE '/'
    if req == '/':
        page = index()

    # LOGIN ROUTE
    elif req == '/login':
        match = ure.search("username=([^&]*)&password=(.*)", data)
        if match is None:
            page = index("Invalid Username or Password (POST)")
        # version 1.9 compatibility
        try:
            username = match.group(1).decode("utf-8").replace("%3F", "?").replace("%21", "!")
            password = match.group(2).decode("utf-8").replace("%3F", "?").replace("%21", "!")
        except Exception:
            username = match.group(1).replace("%3F", "?").replace("%21", "!")
            password = match.group(2).replace("%3F", "?").replace("%21", "!")
        data = {
            "username":username,
            "password":password
        }
        isAuthenticated = wsf.checkAuth(data)
        if isAuthenticated:
            page = dashboard()
        else:
            page = index("Invalid Username or Password (AUTH)")
        
    return page