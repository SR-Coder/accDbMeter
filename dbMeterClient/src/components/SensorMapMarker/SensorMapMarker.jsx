import {Marker} from '@vis.gl/react-google-maps';
import PropTypes from "prop-types";
import React, {useState} from 'react';
import {
  AdvancedMarker,
  InfoWindow,
  useAdvancedMarkerRef
} from '@vis.gl/react-google-maps';

function SensorMapMarker({ sensor }) {
    const [infowindowOpen, setInfowindowOpen] = useState(true);
  const [markerRef, marker] = useAdvancedMarkerRef();

  return (
    <>
      <AdvancedMarker
        ref={markerRef}
        onClick={() => setInfowindowOpen(true)}
        position={{lat: sensor.latitude, lng: sensor.longitude}}
        title={sensor.sensorName + " - " + Math.round(sensor.dbLevel) + "dB"}
      />
      {infowindowOpen && (
        <InfoWindow
          anchor={marker}
          maxWidth={200}
          onCloseClick={() => setInfowindowOpen(false)}>
          <h2>{sensor.sensorName}</h2>
          <p>{Math.round(sensor.dbLevel)}dB</p>
        </InfoWindow>
      )}
    </>
    );
           
}


SensorMapMarker.propTypes = {
  sensor: PropTypes.object.isRequired,
};
export default SensorMapMarker;