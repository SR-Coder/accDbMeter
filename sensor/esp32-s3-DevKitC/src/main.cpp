#ifndef SPIFFS
#define SPIFFS LittleFS
#endif

#include <Arduino.h>
#include <ArduinoJson.h>
#include <LittleFS.h>
#include "wifimanager.h"
#include "HWCDC.h"
#include <HardwareSerial.h>
#include <WiFi.h> 
#include <PubSubClient.h>

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

// Create a instance of the WifiManager
WIFIMANAGER WifiManager;

AsyncWebServer webServer(80);

void setup()
{

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

// WIFI MANAGER SETUP
  WifiManager.startBackgroundTask();
  WifiManager.fallbackToSoftAp();
  WifiManager.attachWebServer(&webServer);

  // Server the landing pages for both the STA and AP
  webServer
    .serveStatic("/", SPIFFS, "/www")
    .setDefaultFile("index.html")
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
    request->send(200, "text/plain", "Resetting");
    delay(1000);
    ESP.restart();
  });

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

void loop() 
{
  // put your main code here, to run repeatedly:

  String msg = "Message Number: " + String(counter);

  if(client.connected()){
    client.publish("test", msg.c_str());
    counter++;
  } else {
    Serial.println("Client not connected");
    reconnect();
  }

  if (millis() - lastTime > 5000) {
    client.loop();
    lastTime = millis();
  }



  delay(50);

  if (false) {
    WifiManager.runSoftAP();
  }
}

