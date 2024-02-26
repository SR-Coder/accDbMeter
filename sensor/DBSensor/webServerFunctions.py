# Some Helper functions for the web server 
import hashlib
import binascii
import select
import fileFunctions as ff
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
            conn.close()
            return False
    
def sendStyleSheet(conn, file='./style.css'):
    try:
        textFile = ""
        conn.send('Content-type: text/css\n')
        conn.send('Connection: close\n\n')
        with open(file, 'r') as dataS:
            textFile = dataS.read()
        conn.sendall(textFile)
        conn.close()
        print('CSS Style Sheet Sent')
        return True
    except OSError as e:
        print('Something went wrong sending the style sheet!', e)
        conn.close()
        return False

def redirect(conn, serverAddress, route, data=""):
    
    newLoc = f"http://{serverAddress[0]}{route}"

    try:
        conn.send('HTTP/1.1 301 Moved Permanently\n')
        conn.send(f'Location: {newLoc}\n')
        conn.send('Content-Length: 0')
        conn.close()
        return True
    except OSError as e:
        print("Something went wring in the redirect: ", e)
        conn.close()
        return False
    
def parseHTTPReq(request):
    print('Parsing http Req')
    headers = {}
    request = request.decode('utf-8')
    lines = request.split('\r\n')
    method, path, httpVersion = lines[0].split(' ')
    for line in lines[1:]:
        if line == '':
            break
        header, value = line.split(': ', 1)
        headers[header] = value
    contentLength = int(headers.get('Content-Length', 0))
    print("REQ PARTS ---> ", method, path, httpVersion, contentLength)
    return contentLength
    

    
def streamRequestBody(conn, request, bufferSize):
    print("attempting to stream req body")
    # method, path, httpVersion, headers, contentLength = parseHTTPReq(request)
    contentLength = 10000
    remaining = contentLength
    myBuffer = b''
    while remaining > 0:
        chunkSize = min(remaining, bufferSize)
        chunk = conn.recv(chunkSize)
        print(chunk)
        myBuffer += chunk
        remaining -= len(chunk)
        if len(chunk) == 0:
            remaining = 0
    print('Inside Stream Request --->',myBuffer)
    return myBuffer

def handleConnections1(sock):
    conn, addr = sock.accept()
    conn.settimeout(3.0)
    print('Received HTTP Request')
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    return request, conn

def handleConnection2(sock):

    readable, _, _ = select.select([sock], [],[], 1.0)

    for s in readable:
        if s is sock:
            conn, addr = sock.accept()
            print(f'connection from {addr}')
            conn.setblocking(False)

            buffer = bytearray(1024)
            totalBytesRead = 0

            while True:
                try:
                    nbytes = conn.readinto(buffer, 1024)
                    if nbytes is None:
                        continue
                    
                    if nbytes == 0:
                        break
                    totalBytesRead += nbytes
                    print(f'received {nbytes} bytes')
                    print(buffer[:nbytes])
                    return buffer, conn
                except OSError as e:
                    if str(e) == '[Errno 11] EAGAIN' or str(e) == '[Errno 119] EAGAIN':
                        continue
                    else: 
                        raise

            print(f'Total bytes recieved: {totalBytesRead}')
    

    


# while b'\r\n\r\n' not in buffer:
#     data1 = conn.recv(1024)
#     print("this is the data:  -->", data)
#     if not data:
#         print('no more data')
#         isDone = True
#         break
#     buffer += data1


# b'POST /update/config HTTP/1.1\r\nHost: 192.168.1.82\r\nConnection: keep-alive\r\nContent-Length: 387\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nOrigin: http://192.168.1.82\r\nContent-Type: application/x-www-form-urlencoded\r\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\nReferer: http://192.168.1.82/dashboard\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: en-US,en;q=0.9\r\n\r\nsensorName=iPZl9V2Z93kPVlVTVbXkOKIkn2f8j0Aq&username=root&password=&confPassword=asdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasdfasd'