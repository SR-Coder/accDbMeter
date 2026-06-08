import { useEffect, useState } from "react";
import Dbmeter from "../DBMeter/dbmeter";
import mqtt from "mqtt";
import "./therack.scss";

const MAX_NUMBER_OF_DATA_POINTS = 600;
const DISTANCE_BETWEEN_SAMPLES_MILLIS = 2000;

function TheRack() {
  const [sensorData, setSensorData] = useState([]);

  useEffect(() => {
    const topic = "DBMeter";
    const mqttOptions = {
      clean: true,
      clientId: "dbmeterclient_" + Math.random().toString(16).substr(2, 8),
      connectTimeout: 30000,
      reconnectPeriod: 1000,
    };
    const client = mqtt.connect(import.meta.env.VITE_MQTT_URL, mqttOptions);

    client.on("connect", () => {
      client.subscribe(topic, (err) => {
        if (!err) console.log("subscribed to", topic);
      });
    });

    client.on("message", (topic, message) => {
      const jsonMessage = JSON.parse(message);

      // legacy field name support
      if (jsonMessage.timestamp === undefined) jsonMessage.timestamp = jsonMessage.timeStamp;
      if (jsonMessage.sensorName === undefined) jsonMessage.sensorName = jsonMessage.sensor_name;

      // normalise dbLevel to a number
      jsonMessage.dbLevel = parseFloat(jsonMessage.dbLevel);

      if (jsonMessage.dbLevel < 40) return;

      setSensorData((prevSensorData) => {
        const existingIndex = prevSensorData.findIndex(
          (arr) => arr[0].sensorId === jsonMessage.sensorId
        );

        if (existingIndex !== -1) {
          const updatedSensorData = [...prevSensorData];
          let arr = updatedSensorData[existingIndex];

          // drop whichever of the last two points is quieter when they're too close together
          if (arr.length > 2 && arr[arr.length - 2].timestamp + DISTANCE_BETWEEN_SAMPLES_MILLIS >= arr[arr.length - 1].timestamp) {
            const latest = arr.pop();
            const prev   = arr.pop();
            arr.push(latest.dbLevel > prev.dbLevel ? latest : prev);
          }

          arr.push(jsonMessage);
          if (arr.length > MAX_NUMBER_OF_DATA_POINTS) arr.shift();

          updatedSensorData[existingIndex] = [...arr];
          return updatedSensorData;
        } else {
          return [...prevSensorData, [jsonMessage]];
        }
      });
    });

    return () => client.end();
  }, []);

  return (
    <div className="the-rack">
      <div className="the-rack-sensors">
        {sensorData.length === 0 ? (
          <p className="the-rack-empty">Waiting for sensors&hellip;</p>
        ) : (
          sensorData.map((sensor) => (
            <Dbmeter key={sensor[0].sensorId} sensor={sensor} />
          ))
        )}
      </div>
    </div>
  );
}

export default TheRack;
