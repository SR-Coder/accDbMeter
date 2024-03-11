import flashmsgs


def index():
    if 'login' in flashmsgs.flashMsg:
        loginMessage = flashmsgs.flashMsg['login']
    else:
        loginMessage = ""

    html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="shortcut icon" href="./favicon.ico" type="image/x-icon">
            <link rel="stylesheet" href="./style.css">
            <title>ACC DB Sensor | Login</title>
        </head>
            <body>
                <header>
                    <div class="wide">
                        <h1>ACC DB Meter | Sensor Config Login Page</h1>
                        <div class="config-header">
                            <p>v1.0</p>
                        </div>
                    </div>
                </header>
                <main>
                    <div class="login-form">
                        <form class="login" action="/login" method="post">
                            <p class="warning">{}</p>
                            <div class="form-item">
                                <label class="input-label" for="username">Username:</label>
                                <input type="text" name="username" id="username" placeholder="username">
                            </div>
                            <div class="form-item">
                                <label class="input-label" for="password">Password: </label>
                                <input type="password" name="password" id="password" placeholder="password">
                            </div>
                            <button class="button-submit" type="submit">Submit</button>
                        </form>
                    </div>


                </main>
                <footer>
                    <p>Created by the ACC Software Design Team 2024</p>
                </footer>
            </body>
        </html>
    """ .format(loginMessage)
    flashmsgs.flashMsg['login']=""
    return html

def dashboard(data, args={}):
    """
    returns an html string that can be sent to the server.
    Data must be a dictionary with the following:
    - username
    - sensorAddress
    - sensorName
    - sensorLocation
    - xLoc
    - yLoc
    - mqttClientID
    - mqttAddress
    - mqttPort
    - mqttUsername
    - mqttPassword
    - mqttRate
    """    
    if 'units' in data:
        if data['units'] == 'feet':
            isFeet = 'selected'
            isMeters = ""
        elif data['units'] == 'meters':
            isMeters = 'selected'
            isFeet = ""
    else:
        isFeet = "selected"
        isMeters = ""
    
    locationMessages = ""
    passwordMessages = ""
    mqttMessages = ""
    passwordKeys = ['password','confPassword']
    locMsgKeys = ['sensorLocationMsg','unitsMsg','xLocMsg','yLocMsg']
    mqttMsgKeys = ['mqttClientID', 'mqttAddress', 'mqttPort', 'mqttUsername', 'mqttPassword', 'mqttRate']
    for msg in flashmsgs.flashMsg:
        key = msg
        if key in passwordKeys:
            passwordMessages += flashmsgs.flashMsg[key] + "\r"
        if key in locMsgKeys:
            locationMessages += flashmsgs.flashMsg[key] + "\r"
        if key in mqttMsgKeys:
            mqttMessages += flashmsgs.flashMsg[key] + "\r"

    rateOff=""
    rate1=""
    rate2=""
    rate3=""
    rate4=""
    rate5=""
    rate6=""
    rate7=""
    rate8=""
    rate9=""

    print("the data at mqttRate",data['mqttRate'])
    r = data['mqttRate']
    if r == "0":
        rateOff = "selected"
    elif r == '.016':
        rate1 = "selected"
    elif r == '1':
        rate2 = 'selected'
    elif r == '.6':
        rate3 = 'selected'
    elif r == '.30':
        rate4 = 'selected'
    elif r == '60':
        rate5 = 'selected'
    elif r == '600':
        rate6 = 'selected'
    elif r == '6000':
        rate7 = 'selected'
    elif r == '20000':
        rate8 = 'selected'
    elif r == '40000':
        rate9 = 'selected'


    html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="shortcut icon" href="./favicon.png" type="image/x-icon">
            <link rel="stylesheet" href="./style.css">
            <title>ACC DB Sensor</title>
        </head>
            <body>
                <header>
                    <div class="wide">
                        <h1>ACC DB Meter Sensor</h1>
                        <div class="config-header">
                            <p>v1.0</p>
                            <p>logged in as: {username}</p>
                            <p>Sensor Address: {sensorAddress}</p>
                            <p>MQTT Address: {mqttAddress}</p>
                        </div>
                    </div>
                    <form action="/dashboard/logout" method="post">
                        <button type="submit">Logout</button>
                    </form>
                </header>
                <main>
                    <div class="config-header">
                        <h1>DB Sensor Configuration</h1>
                        <a class="btn" href="/dashboard/restart">Restart Sensor</a>
                        <a class="btn" href="/dashboard/mqttStop">Stop MQTT</a>
                        <a class="btn" href="/dashboard/mqttStart">Start MQTT</a>
                        <a class="btn" href="/dashboard/mqttRestart">Restart MQTT</a>
                    </div>
                    <div class="form-container">
                        
                        <form action="/dashboard/update/sensordata" method="post" >
                            <h2>Device Information</h2>
                            <p class="warning">{passwordMessages}</p>
                            <div class="form-item">
                                <label class="input-label" for="sensorName">Sensor Name</label>
                                <input class="text-input" type="text" name="sensorName" id="sensorName" maxlength="16" value="{sensorName}">
                            </div>
                            <div class="form-item">
                                <label class="input-label" for="username">Username</label>
                                <input class="text-input" type="text" name="username" id="username" maxlength="16" value="{username}">
                            </div>
                            <div class="form-item">
                                <label class="input-label" for="password">Password</label>
                                <input class="text-input" type="password" name="password" maxlength="16" id="password" >
                            </div>
                            <div class="form-item">
                                <label class="input-label" for="confPassword">Confirm Password</label>
                                <input class="text-input" type="password" name="confPassword" maxlength="16" id="confPassword" >
                            </div>
                            <div class="center">
                                <button class="button-submit" type="submit">Submit</button>
                            </div>
                        </form>
                            <div class="center">
                                <hr>
                            </div>
                            <h2>Physical Location</h2>
                            <p class="warning">{locationMessages}</p>
                        <form action="/dashboard/update/sensorlocation" method="post">
                            <div class="form-item">
                                <label class="input-label tooltip" for="sensorLocation">Location Name
                                    <span class="tooltiptext">Provide a descriptive location for this sensor.</span>
                                </label>
                                <input class="text-input" type="text" name="sensorLocation" id="sensorLocation" maxlength="32" value="{sensorLocation}">
                            </div>
                            <!-- <h3>Distance from left to right (X), and front to back (Y)</h3> -->
                            <div class="form-item">
                                <label class="input-label tooltip" for="units">Units
                                    <span class="tooltiptext">Select a measurement unit (english or metric)</span>
                                </label>
                                <select name="units" id="units">
                                    <option value="feet" {isFeet}>Feet</option>
                                    <option value="meters" {isMeters}>Meters</option>
                                </select>
                            </div>
                            <div class="form-item">
                                <label class="input-label tooltip" for="xLoc">X - Location
                                    <span class="tooltiptext">Distance left or right from center stage (Stage Right is Negative)</span>
                                </label>
                                <input class="text-input" type="number" name="xLoc" id="xLoc" maxlength="4" value="{xLoc}">
                            </div>
                            <div class="form-item">
                                <label class="input-label tooltip" for="yLoc">Y - Location
                                    <span class="tooltiptext">Distance from the front of the stage (onstage is negative)</span>
                                </label>
                                <input class="text-input" type="number" name="yLoc" id="yLoc" maxlength="4" value="{yLoc}">
                            </div>
                            <div class="center">
                                <button class="button-submit" type="submit">Submit</button>
                            </div>
                        </form>
                            <div class="center">
                                <hr>
                            </div>
                            <h2>MQTT Server Settings</h2>
                            <p class="warning">{mqttMessages}</p>
                        <form action="/dashboard/update/mqttsettings" method="post">
                            <div class="form-item">
                                <label class="input-label tooltip" for="mqttClientID">MQTT Client ID 
                                    <span class="tooltiptext">MQTT Client ID. Pick a unique name</span>
                                </label>
                                <input class="text-input" type="text" name="mqttClientID" id="mqttClientID" maxlength="16" value="{mqttClientID}">
                            </div>
                            <div class="form-item">
                                <label class="input-label tooltip" for="mqttAddress">MQTT Server 
                                    <span class="tooltiptext">Ip Address or Server Name (ie: 10.1.1.10, or hive.mq.com)</span>
                                </label>
                                
                                <input class="text-input" type="text" name="mqttAddress" id="mqttAddress" value="{mqttAddress}">
                            </div>
                            <div class="form-item">
                                <label class="input-label tooltip" for="mqttPort">MQTT Port 
                                    <span class="tooltiptext">Port Number for MQTT Server</span>
                                </label>
                                
                                <input class="text-input" type="text" name="mqttPort" id="mqttPort" maxlength="4" value="{mqttPort}">
                            </div>
                            <div class="form-item">
                                <label class="input-label tooltip" for="mqttRate">MQTT Msg Rate 
                                    <span class="tooltiptext">Select how many times per second to send messages</span>
                                </label>
                                <select name="mqttRate" id="mqttRate">
                                    <option value="0" {rateOff}>Off</option>
                                    <option value=".016" {rate1}>1 per min</option>
                                    <option value="1" {rate2}>1hz</option>
                                    <option value="6" {rate3}>10hz</option>
                                    <option value="30" {rate4}>30hz</option>
                                    <option value="60" {rate5}>60hz</option>
                                    <option value="600" {rate6}>600hz</option>
                                    <option value="6000" {rate7}>6000hz</option>
                                    <option value="20000" {rate8}>20000hz</option>
                                    <option value="40000" {rate9}>40000hz</option>
                                </select>
                            </div>
                            <div class="center">
                                <button class="button-submit" type="submit">Submit</button>
                            </div>
                        </form>
                        <div class="center">
                            <hr>
                        </div>
                        <form action="/dashboard/update/mqttpass" method="post">
                            <div class="form-item">
                                <label class="input-label tooltip" for="mqttUsername">MQTT Username 
                                    <span class="tooltiptext">Your username for logging into the MQTT Server</span>
                                </label>
                                
                                <input class="text-input" type="text" name="mqttUsername" id="mqttUsername" maxlength="16" value="{mqttUsername}">
                            </div>
                            <div class="form-item">
                                <label class="input-label tooltip" for="mqttPassword">MQTT Password 
                                    <span class="tooltiptext">Password for logging into MQTT Server.  WARNING THIS WILL BE SAVED UNHASHED IN THE CONFIG.JSON FILE</span>
                                </label>
                                <input class="text-input" type="text" name="mqttPassword" id="mqttPassword" maxlength="16" value="{mqttPassword}">
                            </div>
                            <div class="form-item">
                                <label class="input-label tooltip" for="mqttConfPassword">MQTT Password 
                                    <span class="tooltiptext">Password for logging into MQTT Server.  WARNING THIS WILL BE SAVED UNHASHED IN THE CONFIG.JSON FILE</span>
                                </label>
                                <input class="text-input" type="text" name="mqttConfPassword" maxlength="16" id="mqttConfPassword">
                            </div>
                            <div class="center">
                                <button class="button-submit" type="submit">Submit</button>
                            </div>
                        </form>
                        
                    </div>
                </main>
                <footer>
                    <p>Created by the ACC Software Design Team 2024</p>
                </footer>
            </body>
        </html>
    '''.format(
        passwordMessages = passwordMessages,
        username = data['username'],
        sensorAddress = data['sensorAddress'],
        sensorName = data['sensorName'],

        locationMessages = locationMessages,
        sensorLocation = data['sensorLocation'],
        xLoc = data['xLoc'],
        yLoc = data['yLoc'], 

        mqttMessages = mqttMessages,
        mqttClientID = data['mqttClientID'],
        mqttAddress = data['mqttAddress'],
        mqttPort= data['mqttPort'],
        mqttUsername = data['mqttUsername'],
        mqttPassword = data['mqttPassword'],
        mqttRate = data['mqttRate'],

        rateOff = rateOff,
        rate1 = rate1,
        rate2 = rate2,
        rate3 = rate3,
        rate4 = rate4,
        rate5 = rate5,
        rate6 = rate6, 
        rate7 = rate7,
        rate8 = rate8,
        rate9 = rate9,

        isFeet = isFeet,
        isMeters = isMeters
    )

    flashmsgs.flashMsg = {}

    return html