#ifndef SPIFFS
#define SPIFFS LittleFS
#endif

#define SHOW_TIME_PERIOD 1000
#define LED 38
#define rLED 

#define isI2c false

#include <Adafruit_NeoPixel.h>
#include <Arduino.h>
#include <ArduinoJson.h>
#include <LittleFS.h>
#include "wifimanager.h"
#include "HWCDC.h"
#include <HardwareSerial.h>
#include <WiFi.h> 
#include <PubSubClient.h>
#include <ESPNtpClient.h>
#include "dbMeter.h"

#if isI2c
#include <Wire.h>
#endif

#define NUMPIXELS 1
#define PIN_NEOPIXEL 48

Adafruit_NeoPixel pixels(NUMPIXELS, PIN_NEOPIXEL, NEO_GRB + NEO_KHZ800);

// FILESYSTEM STUFF
void listDir(fs::FS &fs, const char * dirname, uint8_t levels){
    Serial.printf("Listing directory: %s\r\n", dirname);

    File root = fs.open(dirname);
    if(!root){
        Serial.println("- failed to open directory");
        return;
    }
    if(!root.isDirectory()){
        Serial.println(" - not a directory");
        return;
    }

    File file = root.openNextFile();
    while(file){
        if(file.isDirectory()){
            Serial.print("  DIR : ");
            Serial.println(file.name());
            if(levels){
                listDir(fs, file.name(), levels -1);
            }
        } else {
            Serial.print("  FILE: ");
            Serial.print(file.name());
            Serial.print("\tSIZE: ");
            Serial.println(file.size());
        }
        file = root.openNextFile();
    }
}

// MQTT Stuff
WiFiClient espClient;
PubSubClient client(espClient);
// char mqtt_name[128];
char mqtt_server[128];
int mqtt_rate;
bool run_mqtt = true;

// Create a instance of the WifiManager
WIFIMANAGER WifiManager;
AsyncWebServer webServer(80);

// create structure to hold config file data
struct config_t {
    String sensor_UUID;
    String sensor_name;
    String sensor_username;
    String sensor_password;
    String sensor_location;
    String units;
    int x_loc;
    int y_loc;
    String mqtt_server;
    int mqtt_port;
    String mqtt_username;
    String mqtt_password;
    int mqtt_rate;
}; 

config_t my_config;

// a function to write to the config file
void writeConfig(const config_t& config, const char* filename){
  File configFile = SPIFFS.open(filename, "w");
  if (!configFile){
    Serial.println("Failed to open config file for writing");
    return;
  }

  JsonDocument doc;
  doc["sensor_UUID"] = config.sensor_UUID;
  doc["sensor_name"] = config.sensor_name;
  doc["sensor_username"] = config.sensor_username;
  doc["sensor_password"] = config.sensor_password;
  doc["sensor_location"] = config.sensor_location;
  doc["units"] = config.units;
  doc["x_loc"] = config.x_loc;
  doc["y_loc"] = config.y_loc;
  doc["mqtt_server"] = config.mqtt_server;
  doc["mqtt_port"] = config.mqtt_port;
  doc["mqtt_username"] = config.mqtt_username;
  doc["mqtt_password"] = config.mqtt_password;
  doc["mqtt_rate"] = config.mqtt_rate;

  char* buffer[measureJson(doc) + 1];
  serializeJson(doc, buffer, measureJson(doc));
  
  
  Serial.println("***************************************");
  Serial.println("Config File Size: ");
  Serial.println(measureJson(doc));
  configFile.write((uint8_t*)buffer, measureJson(doc));
  Serial.println("\nEND OF FILE!");
  Serial.println("***************************************");
  doc.clear();
  return;
}

// Serial I2C Setup for DB Sensor
#if isI2c
TwoWire dbmeter = TwoWire(0);

// Read from the register of the DB Sensor
uint8_t dbmeter_readreg(TwoWire *dev, uint8_t regAddr){
  dev->beginTransmission(DBM_ADDR);
  dev->write(regAddr);
  dev->endTransmission();
  dev->requestFrom(DBM_ADDR, 1);
  return dev->read();
}
#endif


void setup()
{
  // Start the serial connection
  Serial.begin(115200);
  Serial.println("Connected");

  #if defined(NEOPIXEL_POWER)
  pinMode(NEOPIXEL_POWER, OUTPUT);
  digitalWrite(NEOPIXEL_POWER, HIGH);
  #endif

  pixels.begin();
  pixels.setBrightness(20);

  pixels.fill(pixels.Color(255, 255, 0), 0, NUMPIXELS);
  pixels.show();

  // Start the NTP Client
  NTP.setTimeZone(TZ_America_Los_Angeles);
  NTP.begin();

  // Setup the LED
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);

  // Check the file system
  if (!LittleFS.begin(true)){
    Serial.println("[ERROR] Unable to open spiffs partition or run little FS");
    ESP.deepSleep(15 * 1000 * 1000);
  }

  // GET VALUES FROM CONFIG FILE
  File configFile = SPIFFS.open("/secrets/config.json", "r");
  if (!configFile){
    Serial.println("[ERROR] Unable to open config file");
    return;
  }

  size_t size = configFile.size();
  std::unique_ptr<char[]> buf(new char[size]);
  configFile.readBytes(buf.get(), size);
  JsonDocument doc;
  auto deserializeError = deserializeJson(doc, buf.get());

  if (deserializeError) {
    Serial.println("Failed to parse config file");
    return;
  }

  strncpy(mqtt_server, doc["mqtt_server"], sizeof(mqtt_server));
  mqtt_server[sizeof(mqtt_server) - 1] = '\0';

  const char* sensor_username = doc["sensor_username"];
  const char* sensor_password = doc["sensor_password"];
  mqtt_rate = doc["mqtt_rate"].as<int>();

  // add values to struct
  my_config.sensor_UUID = doc["sensor_UUID"].as<String>();
  my_config.sensor_name = doc["sensor_name"].as<String>();
  my_config.sensor_username = doc["sensor_username"].as<String>();
  my_config.sensor_password = doc["sensor_password"].as<String>();
  my_config.sensor_location = doc["sensor_location"].as<String>();
  my_config.units = doc["units"].as<String>();
  my_config.x_loc = doc["x_loc"].as<int>();
  my_config.y_loc = doc["y_loc"].as<int>();
  my_config.mqtt_server = doc["mqtt_server"].as<String>();
  my_config.mqtt_port = doc["mqtt_port"].as<int>();
  my_config.mqtt_username = doc["mqtt_username"].as<String>();
  my_config.mqtt_password = doc["mqtt_password"].as<String>();
  my_config.mqtt_rate = doc["mqtt_rate"].as<int>();

  configFile.close();


// WIFI MANAGER SETUP
  WifiManager.startBackgroundTask();
  WifiManager.fallbackToSoftAp();
  WifiManager.attachWebServer(&webServer);

  // Server the landing pages for both the STA and AP
  webServer
    .serveStatic("/", SPIFFS, "/www")
    .setDefaultFile("index.html")
    .setAuthentication(sensor_username, sensor_password)
    .setFilter(ON_STA_FILTER);

  webServer
    .serveStatic("/", SPIFFS, "/ap")
    .setDefaultFile("index.html")
    .setFilter(ON_AP_FILTER);


  webServer.on("/submit", HTTP_POST, [](AsyncWebServerRequest *request){
      Serial.println("this route was submitted ");
      int params = request->params();
      Serial.print("Number of params: ");
      Serial.println(params);
      String ssid;
      String password;
      for(int i=0;i<params;i++){
          AsyncWebParameter* p = request->getParam(i);
          Serial.print("Param name: ");
          Serial.println(p->name());
          Serial.print("Param value: ");
          Serial.println(p->value());
          if(p->name() == "ssid"){
            ssid = p->value();
            } else if (p->name() == "password"){
              password = p->value();
            }
          }
          
      if(!ssid.isEmpty() && !password.isEmpty()){
        Serial.println("this route was submitted ");
        if(WifiManager.addWifi(ssid, password)){
          request->redirect("/success");
        } else {
            request->send(500, "text/plain", "Error");
        }
      } else {
        request->send(400, "text/plain", "Bad Request");
      }
  });

  webServer.on("/success", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(SPIFFS, "/ap/success.html");
  });

  webServer.on("/restart", HTTP_GET, [](AsyncWebServerRequest *request){
    delay(1000);
    request->redirect("/");
    ESP.restart();
  });

  webServer.on("/mqttStop", HTTP_GET, [](AsyncWebServerRequest *request){
    run_mqtt = false;
    request->redirect("/");
  });

  webServer.on("/mqttStart", HTTP_GET, [](AsyncWebServerRequest *request){
    run_mqtt = true;
    request->redirect("/");
  });

  // UPDATE SENSOR CONFIG DATA
  webServer.on("/update/sensordata", HTTP_POST, [](AsyncWebServerRequest *request){
    bool isValid = true;
    int params = request->params();
    for(int i=0;i<params;i++){
      AsyncWebParameter* p = request->getParam(i);
      if(p->name() == "sensor_name"){
        my_config.sensor_name = p->value();
      } else if (p->name() == "sensor_username"){
        my_config.sensor_username = p->value();
      } else if (p->name() == "sensor_password"){
        my_config.sensor_password = p->value();
      } else if (p->name() == "sensor_confPassword"){
        String confPassword = p->value();
        if(confPassword != my_config.sensor_password){
          isValid = false;
        }
      } else {
        Serial.println("Debug Data (Name): " + p->name() + " (Value): " + p->value());
        isValid = false;
      }
    }
    if(isValid){
      writeConfig(my_config, "/secrets/config.json");

      request->redirect("/");
    } else {
      request->send(400, "text/plain", "Bad Request, failed the validity test");
    }
  });

  webServer.on("/update/sensorlocation", HTTP_POST, [](AsyncWebServerRequest *request){
    bool isValid = true;
    int params = request->params();
    for(int i=0;i<params;i++){
      AsyncWebParameter* p = request->getParam(i);
      if(p->name() == "sensor_location"){
        my_config.sensor_location = p->value();
      } else if (p->name() == "units"){
        my_config.units = p->value();
      } else if (p->name() == "x_loc"){
        my_config.x_loc = p->value().toInt();
      } else if (p->name() == "y_loc"){
        my_config.y_loc = p->value().toInt();
      } else {
        Serial.println("Debug Data (Name): " + p->name() + " (Value): " + p->value());
        isValid = false;
      }
    }
    if(isValid){
      writeConfig(my_config, "/secrets/config.json");
      request->redirect("/");
    } else {
      request->send(400, "text/plain", "Bad Request, failed the validity test");
    }
  });

  webServer.on("/update/mqttsettings", HTTP_POST, [](AsyncWebServerRequest *request) {
    bool isValid = true;
    int params = request->params();
    for(int i=0;i<params;i++){
      AsyncWebParameter* p = request->getParam(i);
      if(p->name() == "mqtt_server"){
        my_config.mqtt_server = p->value();
      } else if (p->name() == "mqtt_port"){
        my_config.mqtt_port = p->value().toInt();
      } else if (p->name() == "mqtt_user"){
        my_config.mqtt_username = p->value();
      } else if (p->name() == "mqtt_pass"){
        my_config.mqtt_password = p->value();
      } else if (p->name() == "mqtt_rate"){
        my_config.mqtt_rate = p->value().toInt();
      } else {
        Serial.println("Debug Data (Name): " + p->name() + " (Value): " + p->value());
        isValid = false;
      }
    }
    if(isValid){
      writeConfig(my_config, "/secrets/config.json");
      request->redirect("/");
    } else {
      request->send(400, "text/plain", "Bad Request, failed the validity test");
    }
  });

  // SENSOR API

  webServer.on("/api/config", HTTP_GET, [](AsyncWebServerRequest *request){
    String json;
    JsonDocument doc;
    doc["sensor_name"] = my_config.sensor_name;
    doc["sensor_username"] = my_config.sensor_username;
    doc["sensor_password"] = my_config.sensor_password;
    doc["sensor_location"] = my_config.sensor_location;
    doc["units"] = my_config.units;
    doc["x_loc"] = my_config.x_loc;
    doc["y_loc"] = my_config.y_loc;
    doc["mqtt_server"] = my_config.mqtt_server;
    doc["mqtt_port"] = my_config.mqtt_port;
    doc["mqtt_username"] = my_config.mqtt_username;
    doc["mqtt_password"] = my_config.mqtt_password;
    doc["mqtt_rate"] = my_config.mqtt_rate;
    serializeJson(doc, json);
    request->send(200, "application/json", json);
    doc.clear();
  });

  // Serve the Favicon file
  webServer
    .serveStatic("/favicon.ico", SPIFFS, "/www")
    .setDefaultFile("favicon.ico");
    // .setFilter(ON_STA_FILTER);

  // Server static files for the AP
  webServer
    .serveStatic("/style.css", SPIFFS, "/ap")
    .setDefaultFile("style.css")
    .setFilter(ON_AP_FILTER);

  webServer
    .serveStatic("/index.js", SPIFFS, "/ap")
    .setDefaultFile("index.js")
    .setFilter(ON_AP_FILTER);

  // Server static files for the STA
  webServer
    .serveStatic("/style.css", SPIFFS, "/www")
    .setDefaultFile("style.css")
    .setFilter(ON_STA_FILTER);
  
  webServer
    .serveStatic("/index.js", SPIFFS, "/www")
    .setDefaultFile("index.js")
    .setFilter(ON_STA_FILTER);

  // handle any unknown routes
  webServer.onNotFound([&](AsyncWebServerRequest *request){
    request->send(404, "text/plain", "Not Found");
  });

  webServer.begin();

  // MQTT CONNECTION
  if (WiFi.getMode() == WIFI_STA) {
      // Connect to the MQTT server
      client.setServer(mqtt_server, 1885);
      while (!client.connected()) {
          Serial.println("Connecting to MQTT...");
          Serial.println(mqtt_server);
          if (client.connect(mqtt_server)) {
              Serial.println("connected"); 
          } else {
              Serial.print("failed with state ");
              Serial.print(client.state());
              delay(2000);
          }
      }
  }


  // SETUP DB SENSOR
  #if isI2c
  dbmeter.begin(I2C_SDA, I2C_SCL, 100000);
  uint8_t dbm_version = dbmeter_readreg(&dbmeter, DBM_REG_VERSION);
  Serial.printf("Version = 0x%02X\r\n", dbm_version);

  uint8_t id[4];
  id[0] = dbmeter_readreg(&dbmeter, DBM_REG_ID3);
  id[1] = dbmeter_readreg(&dbmeter, DBM_REG_ID2);
  id[2] = dbmeter_readreg(&dbmeter, DBM_REG_ID1);
  id[3] = dbmeter_readreg(&dbmeter, DBM_REG_ID0);

  Serial.printf("ID = %02X %02X %02X %02X\r\n", id[0], id[1], id[2], id[3]);
  #endif
}

unsigned long lastTime = 0;

// MQTT RECONNECT FUNCTION
void reconnect(){
  client.setServer(mqtt_server, 1885);
  if(!client.connected() && WiFi.getMode() == WIFI_STA) {
    Serial.println("Attempting MQTT connection...");
    Serial.println(mqtt_server);
    if (client.connect(mqtt_server)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(3000);
    }
  }
}

bool isOn = false;
bool isFlashing = true;

void statusLed(){
  if(isOn && isFlashing){
    // turns off led if it is on and set to flash
    neopixelWrite(RGB_BUILTIN, 0,0,0);
    isOn = false;
    return;
  }
  if (WiFi.getMode()==WIFI_AP){
    // if in AP mode flash the blue led
    neopixelWrite(RGB_BUILTIN, 0,0,100);
    isOn = true;
    isFlashing = true;
    return;
  }
  if (WiFi.getMode()==3){
    // in ap mode and searching and setting a station
    neopixelWrite(RGB_BUILTIN, 0,0,100);
    isOn = true;
    isFlashing = false; 
    return;
  }
  if (WiFi.getMode()==WIFI_STA && !WiFi.isConnected()){
    // if in STA Mode but not connected solid red
    neopixelWrite(RGB_BUILTIN, 100,0,0);
    isOn = true;
    isFlashing = false;
    return;
  }
  if (WiFi.getMode()==WIFI_STA && WiFi.isConnected() && !client.connected()){
    // if in STA Mode and connected to wifi but not connected to mqtt server flash yellow
    neopixelWrite(RGB_BUILTIN, 100,100,0);
    isOn = true;
    isFlashing = true;
    return;
  }
  if (WiFi.getMode()==WIFI_STA && WiFi.isConnected() && client.connected() && run_mqtt){
    // if in STA Mode and connected to wifi and connected to mqtt server flash green
    neopixelWrite(RGB_BUILTIN, 0,100,0);
    isOn = true;
    isFlashing = true;
    return;
  }
  if (WiFi.getMode()==WIFI_STA && WiFi.isConnected() && client.connected() && !run_mqtt){
    // if in STA Mode and connected to wifi and connected to mqtt server but mqtt is set to stop flash red
    neopixelWrite(RGB_BUILTIN, 100,0,0);
    isOn = true;
    isFlashing = true;
    return;
  }
}

uint8_t db, dbmin, dbmax;
String DBMJson;

void loop() 
{
  // SET STATUS LED
  
  Serial.println("Beginning of Loop");
  // IF CONNECTED TO STATION DO THE FOLLOWING ELSE DO NOTHING
  if(WiFi.getMode() == WIFI_STA){
    // GET SENSOR DATA
    // Read the decibel level from the sensor
    // Add fake data in case the sensor is not connected
    #if isI2c
    db = dbmeter_readreg(&dbmeter, DBM_REG_DECIBEL);
    dbmin = dbmeter_readreg(&dbmeter, DBM_REG_MIN);
    dbmax = dbmeter_readreg(&dbmeter, DBM_REG_MAX);
    #else
    db = 255;
    dbmin = 0;
    dbmax = 0;
    #endif

    // CREATE MESSAGE TO SEND TO MQTT SERVER
    JsonDocument doc;
    String msg;
    doc["sensorId"] = ESP.getEfuseMac(); 
    doc["sensor_name"] = my_config.sensor_name;
    doc["dbLevel"] = String(db);
    doc["timeStamp"] = NTP.millis();
    serializeJson(doc, msg);
    doc.clear();
    

    if(client.connected() && run_mqtt){
      client.publish("DBMeter", msg.c_str());
      msg = "";
    } else if (client.connected() && !run_mqtt){
      JsonDocument sDoc;
      String sMsg;
      sDoc["sensorId"] = ESP.getEfuseMac();
      sDoc["sensor_name"] = my_config.sensor_name;
      sDoc["status"] = "Stopped";
      sDoc["timeStamp"] = NTP.millis();
      serializeJson(sDoc, sMsg);
      client.publish("DBMeter", sMsg.c_str());
      sDoc.clear();
      sMsg = "";
    } else {
      reconnect();
    }

    if (millis() - lastTime > 5000) {
      client.loop();
      lastTime = millis();
    }
  }
  // SETS HOW OFTEN THE MQTT CLIENT WILL SEND A MESSAGE
  delay(mqtt_rate);
  statusLed();
}

