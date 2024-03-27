import PropTypes from "prop-types";

export function NumberFormatter({ number }) {
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
