import Comparables from "../Comparables/Comparables";
import { NumberFormatter } from "../NumberFormatter/NumberFormatter";
import PropTypes from "prop-types";
import "./dbmeter.scss";

function Dbmeter({ sensor: { sensorId, dbLevel, sensorName, timestamp } }) {
  const formattedDB = Math.round(dbLevel);
  const time = new Date(timestamp).toLocaleTimeString();

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
      </div>
    </>
  );
}

Dbmeter.propTypes = {
  decibelLevel: PropTypes.number,
  sensor: PropTypes.object,
};

export default Dbmeter;
