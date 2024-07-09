import Comparables from "../Comparables/Comparables";
import { NumberFormatter } from "../NumberFormatter/NumberFormatter";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import PropTypes from "prop-types";
import "./dbmeter.scss";

function Dbmeter(sensor) {
  const last = sensor.sensor[sensor.sensor.length - 1];
  const dbLevel = last.dbLevel;
  const formattedDB = Math.round(last.dbLevel);
  const time = new Date(last.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }).replace(/ AM| PM/, "");
  last.time = time;
  const sensorName = last.sensorName;
  const sensorId = last.sensorId;
  const data = sensor.sensor;
  const font = { fill: '#ffffff', fontSize: 12, fontFamily: 'JosefinSans, Arial, sans-serif', fontWeight: '400' }


  return (
    <div className="zone">
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
      <div className="graph">
        <div style={{ backgroundColor: '#777', borderRadius: '1em', boxShadow: 'inset 0 0 5px rgba(0, 0, 0, 0.2)' }}>
          <ResponsiveContainer width={310} height={240}>
            <AreaChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <defs>
              <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#F2F700" stopOpacity={0.8}/>
                <stop offset="95%" stopColor="#F2F700" stopOpacity={0}/>
              </linearGradient>
            </defs>
              <CartesianGrid className="grid" strokeDasharray="3 3" fill="#777777" />
              <XAxis tick={font} dataKey="time"/>
              <YAxis tick={font} domain={[40,100]}/>
              <Tooltip 
                contentStyle={{ backgroundColor: '#777777', borderRadius: '1em', boxShadow: 'inset 0 0 5px rgba(0, 0, 0, 0.2)' }}
                wrapperStyle={{ borderRadius: '1em', boxShadow: '0 0 5px 5px rgba(0, 0, 0, .25)' }}
              />
              <Area type="monotone" dataKey="dbLevel" stroke="#F2F700" fillOpacity={1} fill="url(#colorUv)"  isAnimationActive={false}/>

            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

Dbmeter.propTypes = {
  decibelLevel: PropTypes.number,
  sensor: PropTypes.array,
};

export default Dbmeter;
