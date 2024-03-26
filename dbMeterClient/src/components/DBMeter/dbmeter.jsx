import PropTypes from "prop-types";
import { useEffect, useState } from "react";
import Comparables from "../Comparables/Comparables";
import { PlayCircleOutlined } from "@ant-design/icons";
import mqtt from 'mqtt';
import "./dbmeter.scss";

function NumberFormatter({ number }) {
  const numbers = number.toString().split("").map(Number);

  return (
    <div className="meter-output-screen-num">
      {numbers.map((number, index) => (
        <p key={index} className="meter-output-screen-character">
          {number}
        </p>
      ))}
    </div>
  );
}

NumberFormatter.propTypes = {
  number: PropTypes.number.isRequired,
  styling: PropTypes.string,
};

function Dbmeter() {
  const title = "Front";
  const sensorId = 12;
  const [decibel, setDecibel] = useState(
    Math.floor(Math.random() * (50 - 10 + 1)) + 10
  );

  const updateDecibel = () => {
    setDecibel(decibel + 5);
  };

  useEffect(() => {
    //TODO This looks like it is being called multiple times -- stop that.
    const topic = "dbMeter/dbLevel";
    const mqttOptions = {
      "clean": true,
      "clientId": "dbmeterclient_edb260",
      "connectTimeout": 30000,
      "reconnectPeriod": 1000
    }
    // this code lives in the rack.
    // the rack should decide which dbMeter to call setDecibel on.
    const client = mqtt.connect("ws://localhost:8885", mqttOptions);
    client.on("connect", () => {
      console.log("connected");
      client.subscribe(topic, (err) => {
        if (!err) {
          console.log("subscribed");
          client.on("message", (topic, message) => {
            const jsonMessage = JSON.parse(message);
            const dbLevel = jsonMessage.dbLevel;
            if (sensorId == jsonMessage.sensorId) {
              setDecibel(parseInt(dbLevel));
            }
          });
        }
      });
    });
  
  });
  
  return (
    <>
      <button onClick={updateDecibel}>
        <PlayCircleOutlined />
      </button>
      <div className="meter">
        <h1 className="meter-name">{title}</h1>
        <div className="meter-output">
          <div className="meter-output-color-ring">
            <div className="meter-output-screen">
              {/* <p className="meter-output-screen-text">{decibel}</p> */}
              <NumberFormatter number={decibel} />
              <p className="meter-output-screen-backdrop">000</p>
            </div>
          </div>
        </div>
        <Comparables decibel={decibel} />
      </div>
    </>
  );
}

export default Dbmeter;
