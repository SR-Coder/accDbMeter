import Comparables from "../Comparables/Comparables";
import { NumberFormatter } from "../NumberFormatter/NumberFormatter";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import PropTypes from "prop-types";
import "./dbmeter.scss";

function Dbmeter(sensor) {
  const last = sensor.sensor[sensor.sensor.length - 1];
  const dbLevel = last.dbLevel;
  const formattedDB = Math.round(last.dbLevel);
  const time = new Date(last.timestamp).toLocaleTimeString();
  last.time = time;
  const sensorName = last.sensorName;
  const sensorId = last.sensorId;
  const data = sensor.sensor;
  console.log(data);
  return (
    <>
      <div className="meter">
        <div className="meter-header">
          <h1 className="meter-name">{sensorName}</h1>
          <div className="meter-header-subheader">
            <p>Sensor ID:{sensorId}</p>
            <p>{time}</p>
          </div>
        </div>
        <div className="meter-output">
          <div className="meter-output-color-ring">
            <div className="meter-output-screen">
              <NumberFormatter number={formattedDB} />
              <p className="meter-output-screen-backdrop">000</p>
            </div>
          </div>
        </div>
        {dbLevel && <Comparables decibel={formattedDB} />}
        <ResponsiveContainer height={250}>
          <LineChart data={data}
            margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="dbLevel" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </>
  );
}

Dbmeter.propTypes = {
  decibelLevel: PropTypes.number,
  sensor: PropTypes.array,
};

export default Dbmeter;
