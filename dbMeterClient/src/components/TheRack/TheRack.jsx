import { useEffect, useState } from "react";
import Dbmeter from "../DBMeter/dbmeter";
import mqtt from "mqtt";

function TheRack() {
  const [decibel, setDecibel] = useState(0);
  const sensorId = 12;

  useEffect(() => {
    //TODO This looks like it is being called multiple times -- stop that.
    const topic = "dbMeter/dbLevel";
    const mqttOptions = {
      clean: true,
      clientId: "dbmeterclient_edb260",
      connectTimeout: 30000,
      reconnectPeriod: 1000,
    };
    // this code lives in the rack.
    // the rack should decide which dbMeter to call setDecibel on.
    const client = mqtt.connect("ws://localhost:8885", mqttOptions);
    client.on("connect", () => {
      console.log("connected");
      client.subscribe(topic, (err) => {
        if (!err) {
          console.log("subscribed");
          client.on("message", (topic, message) => {
            console.log("M", message);
            const jsonMessage = JSON.parse(message);
            const dbLevel = jsonMessage.dbLevel;
            if (sensorId == jsonMessage.sensorId) {
              setDecibel(parseInt(dbLevel));

              client.unsubscribe(topic, (err) => {
                !err && console.log("unsubscribed");
              });
            }
          });
        }
      });
    });
    return () => {
      // Disconnect from MQTT broker when the component unmounts
      client.end();
    };
  });

  return (
    <div>
      <Dbmeter decibelLevel={decibel} />
    </div>
  );
}

export default TheRack;
