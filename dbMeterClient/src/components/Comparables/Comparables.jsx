import PropTypes from "prop-types";
import { comparables } from "./data";
import { useEffect, useState } from "react";
import Icon from "../Icon/Icon";
import "./comparables.scss";

function Comparables({ decibel }) {
  const [closestComparable, setClosestComparable] = useState(null);

  function findComparable(decibel) {
    const validComparables = comparables.filter((comp) => comp.db <= decibel);
    const maxDbComparable = validComparables.reduce(
      (max, curr) => (curr.db > max.db ? curr : max),
      validComparables[0]
    );
    return maxDbComparable;
  }

  useEffect(() => {
    const comparable = findComparable(decibel);
    setClosestComparable(comparable);
    console.log(closestComparable);
  });

  return (
    <div className="comparable">
      <div className="comparable-icon">
        {closestComparable && (
          <Icon name={closestComparable?.icon} type={"outlined"} />
        )}
      </div>
      <div className="comparable-text">{closestComparable?.label}</div>
    </div>
  );
}

Comparables.propTypes = {
  decibel: PropTypes.number.isRequired,
};

export default Comparables;
