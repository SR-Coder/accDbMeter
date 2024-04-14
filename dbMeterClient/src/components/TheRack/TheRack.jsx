import { useEffect, useState } from "react";
import Dbmeter from "../DBMeter/dbmeter";
import mqtt from "mqtt";
import { PlayCircleOutlined } from "@ant-design/icons";
import "./therack.scss";

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
          (sensor) => sensor.sensorId === jsonMessage.sensorId
        );
        if (existingSensorIndex !== -1) {
          // Update existing sensor with new data
          const updatedSensorData = [...prevSensorData];
          updatedSensorData[existingSensorIndex] = {
            ...updatedSensorData[existingSensorIndex],
            ...jsonMessage,
          };
          return updatedSensorData;
        } else {
          // Add new sensor data if it doesn't exist
          return [...prevSensorData, jsonMessage];
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
          <Dbmeter key={sensor.sensorId} sensor={sensor} />
        ))}
      </div>
    </div>
  );
}

export default TheRack;
