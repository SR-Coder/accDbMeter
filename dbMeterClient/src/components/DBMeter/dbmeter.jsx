import PropTypes from "prop-types";
import { useState } from "react";
import Comparables from "../Comparables/Comparables";
import { PlayCircleOutlined } from "@ant-design/icons";
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
  const [decibel, setDecibel] = useState(
    Math.floor(Math.random() * (50 - 10 + 1)) + 10
  );

  const updateDecibel = () => {
    setDecibel(decibel + 5);
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
        <Comparables decibel={decibel} />
      </div>
    </>
  );
}

export default Dbmeter;
