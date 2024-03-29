# Raspberry Pi Pico W

This template provides a light weight Wi-Fi Manager using MicroPython. Development starting with esp32 and the teensy4.1 with esp32 wifi over spi.  While the micropython webserver works adquately, the implementation with micropython is slow, the mqtt and webserver sockets have unexpected interactions that lead to negative effects.    





## Initializing the Sensor 
- clone the repo
- open the code in either VSCode using the PyMakr Plugin or Thonny IDE
- Have MicroPython set up on your RPPW
- Transfer the code from the ide of your choice to the RPPW
- Hard Reset the device or turn it off and back on again
- Connect to the `ACCDBMeter-WifiManager` station
- Once connected navigate to `192.168.4.1:8080`
- Select your prefered local network and enter the network password
- KNOWN ISSUES - the Wifi manager will record open networks and will attempt to connect to them before the network that was specified in the previous steps
- Re-connect to your local wifi networks and then search for your device on your router.

## Wi-Fi Manager
A Wi-Fi Manager library has been added to MicroPython, therefore the end user can now connect to the accespoint on inital power up and select an available SSID and enter a password.  This allows end user configuration

### General Flow:
- On initial power up (after code is uploaded) the RPPW performs as an access point allowing users to connect to basic web server
- User configures the RPPW to connect to their prefered wireless network
- Network credentials are then saved to a file in the RPPW long term storage
- The Wifi manager loop will end returning to the main loop prompting the device to connect to the network that was specified
- The device is now on the network and ready to be configured via the web ui. 

This is based directly on this guide:
https://microcontrollerslab.com/raspberry-pi-pico-w-wi-fi-manager-web-server/

## MQTT integration
WIP

### TODO
- [ ] Require SSID's with a Password no open networks
- [x] Build a config file for ease of use
- [x] Write is logged out on startup.
- [x] Build Sensor Config Page
    - [x] Add server address
    - [x] Add server port
    - [x] Add device unique ID
    - [x] Add validations
- [ ] Add ability to change passwords and default ssid
- [x] Ensure auth data is writen to secrets file not user config file
- [x] Require password to enter the Config page
- [ ] Connect config file to mqtt stuff
- [x] Cookie Based Session
- [ ] Interface with sensor
- [ ] Interface with MQTT
- [ ] Send Data to MQTT
- [ ] Multi-Threading

## Version 2
- [x] Address Security Concerns:
    - [x] Add session or token to tie login to individual user
- [ ] Convert structure to a "Class" object