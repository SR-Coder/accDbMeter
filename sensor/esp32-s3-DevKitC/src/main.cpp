#ifndef SPIFFS
#define SPIFFS LittleFS
#endif

#include <Arduino.h>
#include <LittleFS.h>
#include "wifimanager.h"
#include "HWCDC.h"
#include <HardwareSerial.h>

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

  Serial.println("THIS IS THE FILE SYSTEM STUFF!");
  listDir(LittleFS, "/", 3);
  delay(10000);

  WifiManager.startBackgroundTask();
  WifiManager.fallbackToSoftAp();
  WifiManager.attachWebServer(&webServer);

  webServer
    .serveStatic("/", SPIFFS, "/www")
    .setDefaultFile("index.html")
    .setFilter(ON_STA_FILTER);

  webServer
    .serveStatic("/", SPIFFS, "/ap")
    .setDefaultFile("index.html")
    .setFilter(ON_AP_FILTER);

  webServer.on("/home", HTTP_GET, [](AsyncWebServerRequest *request){
    Serial.print(request->method());
    request->send(SPIFFS, "/templates/index.html");
  });

  webServer.onNotFound([&](AsyncWebServerRequest *request){
    request->send(404, "text/plain", "Not Found");
  });

  webServer.begin();

}



void loop() 
{
  // put your main code here, to run repeatedly:
  delay(200);

  if (false) {
    WifiManager.runSoftAP();
  }
}

