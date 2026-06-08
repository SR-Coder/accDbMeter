# ACC dB Meter — Client

React + Vite front-end for the ACC dB Meter system. Connects to a Mosquitto MQTT broker via WebSocket and displays real-time decibel readings from one or more wireless sensors.

---

## Running with Docker (recommended)

```sh
# From this directory
docker build -t acc-dbmeter-client:latest .
docker run -d \
  --name acc-dbmeter-client \
  --restart unless-stopped \
  --network br0 \
  acc-dbmeter-client:latest
```

The app is served by nginx on port 80 at the container's assigned IP.

---

## Local Development

**1. Configure environment**

```sh
cp .env.sample .env.local
```

Edit `.env.local` and set `VITE_MQTT_URL` to your broker's WebSocket address:

```
VITE_MQTT_URL=ws://<broker-ip>:8885
```

**2. Install and run**

```sh
npm install
npm run dev
```

---

## Simulating Sensor Data

To test the UI without physical sensors, use the included message sender from this directory:

```sh
node sample_messages/send_messages.js
```

Edit the top of `send_messages.js` to adjust the sensor list and publish interval.

You can also publish a single test message directly:

```sh
mosquitto_pub -h <broker-ip> -p 1885 -t DBMeter -f sample_messages/green_low.json
```

---

## MQTT Message Format

The client subscribes to the `DBMeter` topic and expects JSON in this shape:

```json
{
  "sensorId": 57243727616732,
  "sensorName": "Back of Church",
  "dbLevel": 74,
  "timestamp": 1708206580764
}
```

The client also accepts legacy field names (`sensor_name`, `timeStamp`) for backwards compatibility with older firmware.

---

## dB Colour Zones

| Range | Colour | Meaning |
|-------|--------|---------|
| < 85 dB | Green | Safe |
| 85 – 89 dB | Yellow | Caution |
| 90 dB + | Red | Danger |

These thresholds are reflected in the ring border, VU bar, and chart line.

---

## Routes

| Path | Description |
|------|-------------|
| `/` | Main dashboard — live sensor cards |
| `/debug` | Raw MQTT connection and message inspector |
