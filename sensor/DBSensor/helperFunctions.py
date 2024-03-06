import hashlib
import binascii
import ure

def hashPasswords(password):
    try:
        hashedPassword = hashlib.sha256()
        hashedPassword.update(bytes(password, 'utf-8'))
        hashedPassword = hashedPassword.digest()
        hashedPassword = binascii.hexlify(hashedPassword)
        hashedPassword = hashedPassword.decode('utf-8')
        return hashedPassword
    except OSError as e:
        print("(hashPasswords)Error Hashing Password", e)
        return False
    
def statusLight(pin):
    '''
    Accepts a "machine.pin" object a time in milliseconds, a frequency and a messages.
    Use this function to set flashing status lights.  Make sure to come up with a good plan 
    these lights
    '''
    print('(statusLight) Pin Value: ',pin.value())
    if pin.value() == 0:
        pin.on()
    else:
        pin.off()
    return True

def isFloat(string: str):
    try:
        float(string)
        return True
    except:
        return False
    
def isValidIPv4(address:str):
    if ure.match("([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])\\.([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])", address):
        return True
    else:
        print('(isValidIPv4)Invalid IPv4 Address')
        return False

def isValidURL(url:str):
    if ure.match('^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$', url):
        return True
    else:
        print("(isValidURL)Invalid URL")
        return False