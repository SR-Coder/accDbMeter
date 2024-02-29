# Some Helper functions for the web server 
import hashlib
import binascii
import select
import fileFunctions as ff
import helperFunctions as hf
SECRETS = 'secret.dat'
import socket

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
        print('user configured: ', setuser)
        return True
    except OSError as e:
        print('No user configured: first login or factory reset, setting (root, root).', e)
        ff.writeAuthData({'root':'root'})
        return False
    
def renderHTML(conn, page):
        try:
            conn.send('HTTP/1.1 200 OK\r\n')
            conn.send('Content-Type: text/html\r\n')
            conn.send('Connection: close\r\n\r\n')
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
        with open(file, 'r') as dataS:
            textFile = dataS.read()
        conn.send("HTTP/1.1 200 OK\r\n")
        conn.send('Content-type: text/css\r\n')
        conn.send('Connection: close\r\n\r\n')
        conn.sendall(textFile)
        conn.close()
        print('CSS Style Sheet Sent')
        return True
    except OSError as e:
        print('Something went wrong sending the style sheet!', e)
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
        return True
    except Exception as e:
        print('Something went wrong sending the favicon: ', e)
        return False

def redirect(conn, serverAddress, route, data=""):
    
    newLoc = f"http://{serverAddress[0]}{route}"

    try:
        conn.send('HTTP/1.1 301 Moved Permanently\r\n')
        conn.send(f'Location: {newLoc}\r\n')
        conn.send('Content-Length: 0\r\n')
        conn.send('Connection: Close\r\n\r\n')
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

# def handleConnections1(sock):
#     conn, addr = sock.accept()
#     conn.settimeout(3.0)
#     print('Received HTTP Request')
#     request = conn.recv(1024)
#     conn.settimeout(None)
#     request = str(request)
#     return request, conn

# def handleConnection2(sock):

#     readable, _, _ = select.select([sock], [],[], 1.0)

#     for s in readable:
#         if s is sock:
#             conn, addr = sock.accept()
#             print(f'connection from {addr}')
#             conn.setblocking(False)

#             buffer = bytearray(1024)
#             totalBytesRead = 0

#             while True:
#                 try:
#                     nbytes = conn.readinto(buffer, 1024)
#                     if nbytes is None:
#                         continue
                    
#                     if nbytes == 0:
#                         break
#                     totalBytesRead += nbytes
#                     print(f'received {nbytes} bytes')
#                     print(buffer[:nbytes])
#                     return buffer, conn
#                 except OSError as e:
#                     if str(e) == '[Errno 11] EAGAIN' or str(e) == '[Errno 119] EAGAIN':
#                         continue
#                     else: 
#                         raise

#             print(f'Total bytes recieved: {totalBytesRead}')
    

