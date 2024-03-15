import React from "react";
import PropTypes from "prop-types";

function Comparables(decibel) {
  return (
    <div className="comparable">
      <div className="comparable-icon"></div>
      <div className="comparable-text"></div>
    </div>
  );
}

Comparables.propTypes = {
  decibel: PropTypes.number.isRequired,
};

export default Comparables;
