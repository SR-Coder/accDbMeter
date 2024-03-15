import PropTypes from "prop-types";
import { useState } from "react";
import "../../style/dbmeter.css";

function NumberFormatter({ number }) {
  const formattedNumber = String(number).padStart(3, "0");

  const characters = formattedNumber.split("");

  return (
    <div className="meter-output-screen-num">
      {characters.map((char, index) => (
        <p key={index} className="meter-output-screen-character">
          {char}
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
  const [decibel, setDecibel] = useState(0);

  const updateDecibel = () => {
    setDecibel(decibel + 5);
  };

  return (
    <>
      <button onClick={updateDecibel}>Play</button>
      <div className="meter">
        <h1 className="meter-name">{title}</h1>
        <div className="meter-output">
          <div className="meter-output-color-ring">
            <div className="meter-output-screen">
              <p className="meter-output-screen-text">{decibel}</p>
              {/* <NumberFormatter number={decibel} /> */}
              <NumberFormatter number={0} />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default Dbmeter;
