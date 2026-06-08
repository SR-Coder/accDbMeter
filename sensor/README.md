# ACC dB Meter — Sensor Firmware

Firmware for the wireless decibel sensor nodes. Two hardware targets are supported:

| Directory | Hardware | Language |
|-----------|----------|----------|
| `RPiPicoW/` | Raspberry Pi Pico W | MicroPython |
| `esp32-s3-DevKitC/` | ESP32-S3 DevKitC | Arduino / PlatformIO |

Both targets connect to a Wi-Fi network, read decibel levels over I²C, and publish readings to a Mosquitto MQTT broker on the `DBMeter` topic.

---

## Initial Setup

### Raspberry Pi Pico W

**Prerequisites**
- MicroPython flashed to the Pico W
- [VSCode + PyMakr plugin](https://marketplace.visualstudio.com/items?itemName=pycom.Pymakr) or [Thonny IDE](https://thonny.org)

**Steps**
1. Clone the repo and open the `RPiPicoW/` folder in your IDE
2. Transfer all files to the Pico W
3. Hard reset the device
4. Connect to the `ACCDBMeter-WifiManager` access point
5. Navigate to `192.168.4.1:8080` and select your Wi-Fi network
6. The device will reboot, join the network, and appear on your router

> **Note:** The Wi-Fi manager will attempt to connect to any previously saved network before the one just configured. If the device does not appear on your network, power cycle it once more.

### ESP32-S3 DevKitC

**Prerequisites**
- [PlatformIO](https://platformio.org) (VSCode extension or CLI)

**Steps**
1. Open the `esp32-s3-DevKitC/` folder in PlatformIO
2. Edit `data/secrets/config.json` with your MQTT broker address and sensor name (see [Configuration](#configuration) below)
3. Upload the filesystem: `pio run --target uploadfs`
4. Build and upload firmware: `pio run --target upload`
5. On first boot the device enters access point mode — connect and configure Wi-Fi via the captive portal

---

## Configuration

Once a sensor is on the network, browse to its IP address to configure it via the web dashboard. All settings are stored on the device and persist across reboots.

| Setting | Description |
|---------|-------------|
| **Sensor Name** | Display name shown on the dashboard |
| **MQTT Broker Address** | IP or hostname of the Mosquitto broker |
| **MQTT Port** | Default: `1885` |
| **Publish Rate** | How frequently readings are sent (ms) |

The ESP32 can also be pre-configured by editing `data/secrets/config.json` before flashing:

```json
{
  "sensor_name": "Front of House",
  "mqtt_server": "192.168.1.100",
  "mqtt_port": 1885,
  "mqtt_rate": 100
}
```

---

## Status LED (ESP32-S3)

The onboard RGB LED indicates connection state:

| Colour | State |
|--------|-------|
| Blue (flashing) | Access point mode — awaiting Wi-Fi configuration |
| Red (solid) | Wi-Fi connected, MQTT disconnected |
| Yellow (flashing) | Wi-Fi connected, attempting MQTT connection |
| Green (flashing) | Fully connected and publishing |
| Red (flashing) | Connected but publishing paused (`/mqttStop`) |

---

## MQTT Message Format

```json
{
  "sensorId": 57243727616732,
  "sensorName": "Front of House",
  "dbLevel": 74,
  "timestamp": 1708206580764
}
```

Topic: `DBMeter`
Broker port: `1885` (standard MQTT)

---

## Wi-Fi Manager

On first boot, the device creates a `ACCDBMeter-WifiManager` access point. Connecting to it presents a simple web page where you can select an available SSID and enter the password. Credentials are saved to persistent storage and used on all subsequent boots.

Based on the [Raspberry Pi Pico W Wi-Fi Manager](https://microcontrollerslab.com/raspberry-pi-pico-w-wi-fi-manager-web-server/) guide.

---

## Roadmap

- [x] Wi-Fi manager for network provisioning
- [x] Web dashboard for sensor configuration
- [x] Cookie-based authentication for the config dashboard
- [x] MQTT publish with configurable rate
- [x] Unique sensor ID per device
- [ ] Restrict Wi-Fi manager to password-protected networks only
- [ ] OTA firmware update support
