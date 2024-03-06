# Some Helper functions for the web server 
import fileFunctions as ff
import helperFunctions as hf
import socket
SECRETS = 'secret.dat'


# Check Auth returns True or False
def checkAuth(data):
    currentUser = ff.readAuthData()
    if not data or not currentUser:
        return False
    else:
        thisUser = data['username']
        thisPass = data['password']
        h = hf.hashPasswords(thisPass)
        currUser = currentUser['username']
        currPass = currentUser['passwordH']
        if thisUser == currUser and currPass == h:
            return True
        else:
            return False

def configAuth():
    try:
        configuredUser = ff.readAuthData()
        setuser = configuredUser['username']
        return True
    except OSError as e:
        print('(configAuth)No user configured: first login or factory reset, setting (root, root).', e)
        ff.writeAuthData({'root':'root'})
        return False
    
def renderHTML(conn, page):
        try:
            conn.send('HTTP/1.1 200 OK\r\n')
            conn.send('Content-Type: text/html\r\n')
            conn.send('Connection: close\r\n\r\n')
            conn.sendall(page)
            conn.close()
            print('(renderHTML)(PAGE RENDER)')
            return True
        except OSError as e:
            print("(ERROR)(renderHTML) ",e)
            conn.close()
            return False
    
def sendStyleSheet(conn, file='./style.css'):
    try:
        textFile = ""
        with open(file, 'r') as dataS:
            textFile = dataS.read()
        conn.send("HTTP/1.1 200 OK\r\n")
        conn.send('Content-type: text/css\r\n')
        conn.send('Connection: close\r\n\r\n')
        conn.sendall(textFile)
        conn.close()
        print("(STYLESHEET) Sent")
        return True
    except OSError as e:
        print('(ERROR)(sendStyleSheet)', e)
        conn.close()
        return False
    
def sendFavicon(conn: socket.socket, file='./favicon.ico'):
    try:
        with open(file, 'rb') as dataS:
            myFile = dataS.read()
        conn.send("HTTP/1.1 200 OK\r\n".encode())
        conn.send('Content-type: image/png\r\n'.encode())
        conn.send(f'Content-Length: {len(myFile)}\r\n'.encode())
        conn.send('Connection: Close\r\n\r\n'.encode())
        conn.sendall(myFile)
        conn.close()
        print('(FAVICON) Sent')
        return True
    except Exception as e:
        print('(ERROR)(sendFavicon) ', e)
        return False

def redirect(conn, serverAddress, route, cookieData={}):
    '''
        Take a connection object, address, and a route, and optional cookie data
        and sends it along with the redirect to the new location
        the cookieData object must contain
        - max-age
    '''
    newLoc = f"http://{serverAddress[0]}{route}"

    try:
        conn.send('HTTP/1.1 301 Moved Permanently\r\n')
        conn.send(f'Location: {newLoc}\r\n')
        conn.send('Content-Length: 0\r\n')
        if len(cookieData)>0:
            for key in cookieData:
                if key != "max-age" and key !='current-time':
                    conn.send(f'Set-Cookie: {key}={cookieData[key]}; Path=/dashboard; Max-age:{cookieData["max-age"]}\r\n')
        conn.send('Connection: Close\r\n\r\n')
        conn.close()
        print("(REDIRECTING): ",newLoc)
        return True
    except OSError as e:
        print("(ERROR)(redirect): ", e, newLoc)
        conn.close()
        return False
    

# def getCookies(request):
#     cookie = {}
#     catagory = ""
#     try:
#         lines = request.split('\r\n')
#         for line in lines:
#             catagory = line.split(':')
#             if catagory[0] == "Cookie":
#                 data = catagory[1].split(';')
#                 for part in data:
#                     temp = part.split("=")
#                     # Remove leading whitespace
#                     cookie[temp[0][1:]] = temp[1]
#         return cookie
#     except OSError as e:
#         print("(getCookies)Something went wrong getting the cookies from the request! \r", e)
#         return False

def checkCookies(cookie:dict):
    try:
        serverCookie = None
        if len(cookie) == 2:
            cookie = eval(str(cookie))
            serverCookie = ff.getOneCookie(cookie['username'], cookie['id'])
        if serverCookie:
            return True
        else:
            return False
    except OSError as e:
        print("(checkCookies)an error occured checking cookies: ",e)
        return False

def parseRequest(request:bytes):
    # VARIABLES
    headers = {}
    tCookie = {}
    formData = {}
    
    # DECODE AND SPLIT
    request = request.decode('utf-8')
    lines = request.split('\r\n')
    method, path, httpVersion = lines[0].split(' ')
    headers["Method"] = method
    headers['Path'] = path
    headers['HttpVersion'] = httpVersion
    headers['Cookie'] = {}
    for line in lines[1:]:
        if line == '':
            break
        header, value = line.split(': ', 1)
        if header == 'Cookie':
            data = value.split('; ', 1)
            for items in data:
                head, val = items.split('=')
                tCookie[head] = val
            headers[header] = tCookie
        else:
            headers[header] = value
    postData = lines[-1].split('&')
    try:
        if postData[0] != '':
            for item in postData:
                header, value = item.split('=',1)
                formData[header] = value
            headers['Post'] = formData
    except Exception as e:
        print("Something went wrong parsing the data!! ", e)
        print(postData)
    return headers
