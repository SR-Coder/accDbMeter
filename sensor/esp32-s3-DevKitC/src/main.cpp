#ifndef SPIFFS
#define SPIFFS LittleFS
#endif

#define LED LED_BUILTIN
#define rLED 

#include <Arduino.h>
#include <ArduinoJson.h>
#include <LittleFS.h>
#include "wifimanager.h"
#include "HWCDC.h"
#include <HardwareSerial.h>
#include <WiFi.h> 
#include <PubSubClient.h>

// #include "processor.h"

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
// const char* mqtt_server = "192.168.1.187";
WiFiClient espClient;
PubSubClient client(espClient);
char mqtt_name[128];
char mqtt_server[128];
int mqtt_rate;
bool run_mqtt = true;

// Create a instance of the WifiManager
WIFIMANAGER WifiManager;
AsyncWebServer webServer(80);

// create structure to hold file data
struct config_t {
    String sensor_name;
    String sensor_username;
    String sensor_password;
    String sensor_location_name;
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

String processor(const String& var){
    if(var == "SENSOR_NAME"){
        return String(my_config.sensor_name);
    }
    if(var == "USER_NAME"){
        return String(my_config.sensor_username);
    }
    if(var == "SENSOR_PASSWORD"){
        return String(my_config.sensor_password);
    }
    if(var == "LOCATION_NAME"){
        return String(my_config.sensor_location_name);
    }
    if(var == "UNITS"){
        return String(my_config.units);
    }
    if(var == "X_LOC"){
        return String(my_config.x_loc);
    }
    if(var == "Y_LOC"){
        return String(my_config.y_loc);
    }
    if(var == "MQTT_SERVER"){
        return String(my_config.mqtt_server);
    }
    if(var == "MQTT_PORT"){
        return String(my_config.mqtt_port);
    }
    if(var == "MQTT_USER"){
        return String(my_config.mqtt_username);
    }
    if(var == "MQTT_PASSWORD"){
        return String(my_config.mqtt_password);
    }
    if(var == "MQTT_RATE"){
        return String(my_config.mqtt_rate);
    }
    return String();
}

void setup()
{

  // Setup the pins for the led
  pinMode(LED, OUTPUT);
  digitalWrite(LED, LOW);

  Serial.begin(115200);
  Serial.println("Connected");

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
  strncpy(mqtt_name, doc["mqtt_name"], sizeof(mqtt_name));
  mqtt_name[sizeof(mqtt_name) - 1] = '\0';

  const char* username = doc["username"];
  const char* password = doc["password"];
  mqtt_rate = doc["mqtt_rate"].as<int>();

  // add values to struct
  my_config.sensor_name = doc["sensor_name"].as<String>();
  my_config.sensor_username = doc["sensor_username"].as<String>();
  my_config.sensor_password = doc["sensor_password"].as<String>();
  my_config.sensor_location_name = doc["sensor_location_name"].as<String>();
  my_config.units = doc["units"].as<String>();
  my_config.x_loc = doc["x_loc"].as<int>();
  my_config.y_loc = doc["y_loc"].as<int>();
  my_config.mqtt_server = doc["mqtt_server"].as<String>();
  my_config.mqtt_port = doc["mqtt_port"].as<int>();
  my_config.mqtt_username = doc["mqtt_username"].as<String>();
  my_config.mqtt_password = doc["mqtt_password"].as<String>();
  my_config.mqtt_rate = doc["mqtt_rate"].as<int>();



// WIFI MANAGER SETUP
  WifiManager.startBackgroundTask();
  WifiManager.fallbackToSoftAp();
  WifiManager.attachWebServer(&webServer);

  // Server the landing pages for both the STA and AP
  webServer
    .serveStatic("/", SPIFFS, "/www")
    .setDefaultFile("index.html")
    .setAuthentication(username, password)
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
          Serial.println(mqtt_name);
          if (client.connect(mqtt_name)) {
              Serial.println("connected"); 
          } else {
              Serial.print("failed with state ");
              Serial.print(client.state());
              delay(2000);
          }
      }
  }
}

int counter = 0;
unsigned long lastTime = 0;


void reconnect(){
  client.setServer(mqtt_server, 1885);
  while (!client.connected()) {
    Serial.println("Attempting MQTT connection...");
    Serial.println(mqtt_name);
    if (client.connect(mqtt_name)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }

}

bool isOn = false;
// LED Functions
void ledOn(){
  neopixelWrite(RGB_BUILTIN, 0,100,0);
  isOn = true;
}
void ledOff(){
  neopixelWrite(RGB_BUILTIN, 0,0,0);
  isOn = false;
}

void ledRed(){
  neopixelWrite(RGB_BUILTIN, 100,0,0);
}

void loop() 
{
  // put your main code here, to run repeatedly:

  String msg = "Message Number: " + String(counter);

  if(client.connected() && run_mqtt){
    if(isOn){
      ledOff();
    } else {
      ledOn();
    };
    client.publish("test", msg.c_str());
    counter++;
  } else {
    Serial.println("Client not connected");
    ledRed();
    reconnect();
  }

  if (millis() - lastTime > 5000) {
    client.loop();
    lastTime = millis();
  }
  // SETS HOW OFTEN THE MQTT CLIENT WILL SEND A MESSAGE
  delay(mqtt_rate);

}

