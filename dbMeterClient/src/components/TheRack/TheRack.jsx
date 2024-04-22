import { useEffect, useState } from "react";
import Dbmeter from "../DBMeter/dbmeter";
import mqtt from "mqtt";
import { PlayCircleOutlined } from "@ant-design/icons";
import "./therack.scss";
const MAX_NUMBER_OF_DATA_POINTS = 24;
const DISTANCE_BETWEEN_SAMPLES_MILLIS = 5000;
function TheRack() {
  const [sensorData, setSensorData] = useState([]);

  useEffect(() => {
    const topic = "DBMeter";
    const mqttOptions = {
      clean: true,
      clientId: "dbmeterclient_"+Math.random().toString(16).substr(2, 8),
      connectTimeout: 30000,
      reconnectPeriod: 1000,
    };
    const client = mqtt.connect(import.meta.env.VITE_MQTT_URL, mqttOptions);

    client.on("connect", () => {
      client.subscribe(topic, (err) => {
        if (!err) {
          console.log("subscribed");
        }
      });
    });
    client.on("message", (topic, message) => {
      const jsonMessage = JSON.parse(message);
      setSensorData((prevSensorData) => {
        // Check if sensor with the same sensorId already exists
        const existingSensorIndex = prevSensorData.findIndex(
          (sensorArray) => sensorArray[0].sensorId === jsonMessage.sensorId
        );
        if (existingSensorIndex !== -1) {
          // Add the new datapoint to the sensor data array.
          const updatedSensorData = [...prevSensorData];
          let newArray = updatedSensorData[existingSensorIndex];
          // Remove data points that are too close to each other
          if (newArray.length > 2 && newArray[newArray.length-2].timestamp +DISTANCE_BETWEEN_SAMPLES_MILLIS >= newArray[newArray.length-1].timestamp) {
            newArray.pop();
          }
          // always add the new data point -- we will remove it later if it is too close to the previous point
          newArray.push(jsonMessage);
          // Remove oldest data point if number of data points exceeds the maximum
          if (newArray.length > MAX_NUMBER_OF_DATA_POINTS) {
            newArray.shift();
          }
          updatedSensorData[existingSensorIndex] = [...newArray];
          return updatedSensorData;
        } else {
          // Add new sensor data if it doesn't exist
          return [...prevSensorData, [jsonMessage]];
        }
      });
    });

    return () => {
      client.end();
    };
  }, []); // Empty dependency array to run effect only once

  return (
    <div className="the-rack">
      <button>
        <PlayCircleOutlined />
      </button>
      <div className="the-rack-sensors">
        {sensorData.map((sensor) => (
          <Dbmeter key={sensor[0].sensorId} sensor={sensor} />
        ))}
      </div>
    </div>
  );
}

export default TheRack;
