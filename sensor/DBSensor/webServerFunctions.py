# Some Helper functions for the web server 
import hashlib
import binascii
SECRETS = 'secret.dat'

# Determine type of request
def getReqTypeAndRoute(request):
    try:
        get = request.find("GET")
        post = request.find("POST")
        reqArr = str(request).split(' ')
        if (len(reqArr) > 0):
            route = reqArr[1]
        else:
            route = -1
        if(get):
            # return the route
            return {"get":route}
        if(post):
            # return the route
            return {"post": route}

    except OSError as e: 
        print("An error occured with the request: ", e)
        return {
            "get":get,
            "post":post
        }

def hashPasswords(password):
    print("What is passed to be Hashed: ", password)
    try:
        hashedPassword = hashlib.sha256()
        hashedPassword.update(bytes(password, 'utf-8'))
        hashedPassword = hashedPassword.digest()
        hashedPassword = binascii.hexlify(hashedPassword)
        hashedPassword = hashedPassword.decode('utf-8')
        print("Password Sucessfully Hashed")
        return hashedPassword
    except OSError as e:
        print("Error Hashing Password", e)
        return False


def writeAuthData(req):
    lines = ""
    for username, password in req.items():
        hash = hashPasswords(password)
        if hash:
            lines = f'{username}:{hash}'
        else:
            print('Error writing hash')
            return False
    with open(SECRETS, "w") as f:
        f.write(lines)
    return True


def removeAuthtData():
    with open(SECRETS, "w") as f:
        f.write("")


def readAuthData():
    username = ""
    passwordH = ""
    with open(SECRETS) as f:
        line = f.read()
    username, passwordH = line.strip("\n").split(":")
    return {
        "username": username,
        "passwordH": passwordH
    }

# Check Auth returns True or False
def checkAuth(data):
    currentUser = readAuthData()
    if not data or not currentUser:
        return False
    else:
        thisUser = data['username']
        thisPass = data['password']
        h = hashPasswords(thisPass)
        currUser = currentUser['username']
        currPass = currentUser['passwordH']

        print("*"*64)
        print(" ")
        print("username F: ", currUser)
        print('passH F: ', currPass)
        print("*"*64)
        print("username P: ", thisUser)
        print('passH P: ', h)
        print(" ")
        print("*"*64)

        if thisUser == currUser and currPass == h:
            return True
        else:
            return False

def configAuth():
    try:
        configuredUser = readAuthData()
        setuser = configuredUser['username']
        print('user configured: ', setuser)
        return True
    except OSError as e:
        print('No user configured: first login or factory reset, setting (root, root).', e)
        writeAuthData({'root':'root'})
        return False
    
def renderHTML(conn, page):
        try:
            conn.send('HTTP/1.1 200 OK\n')
            conn.send('Content-Type: text/html\n')
            conn.send('Connection: close\n\n')
            conn.sendall(page)
            conn.close()
            print('Page rendered')
            return True
        except OSError as e:
            print("Something went wrong with the page render: ",e)
            return False
    

def redirect(conn, route, page, data=""):

    pass