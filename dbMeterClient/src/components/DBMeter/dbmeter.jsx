import { useState } from "react";
import Comparables from "../Comparables/Comparables";
import { PlayCircleOutlined } from "@ant-design/icons";
import { NumberFormatter } from "../NumberFormatter/NumberFormatter";
import PropTypes from "prop-types";
import "./dbmeter.scss";

function Dbmeter({ decibelLevel }) {
  console.log(decibelLevel);
  const title = "Front";
  const [decibel, setDecibel] = useState(0);

  const updateDecibel = () => {
    setDecibel(decibelLevel);
  };

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
        {decibel && <Comparables decibel={decibel} />}
      </div>
    </>
  );
}

Dbmeter.propTypes = {
  decibelLevel: PropTypes.number,
};

export default Dbmeter;
