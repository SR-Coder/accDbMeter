import Comparables from "../Comparables/Comparables";
import { NumberFormatter } from "../NumberFormatter/NumberFormatter";
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import PropTypes from "prop-types";
import "./dbmeter.scss";

function getDbColor(db) {
  if (db >= 90) return '#ff1744';
  if (db >= 85) return '#ffd740';
  return '#00e676';
}

function Dbmeter({ sensor }) {
  const last = sensor[sensor.length - 1];
  const dbLevel = parseFloat(last.dbLevel);
  const formattedDB = Math.round(dbLevel);
  const time = new Date(last.timestamp).toLocaleTimeString([], {
    hour: "2-digit", minute: "2-digit", second: "2-digit",
  }).replace(/ AM| PM/, "");

  const data = sensor.map(d => ({
    ...d,
    dbLevel: parseFloat(d.dbLevel),
    time: new Date(d.timestamp).toLocaleTimeString([], {
      hour: "2-digit", minute: "2-digit", second: "2-digit",
    }).replace(/ AM| PM/, ""),
  }));

  const dbColor = getDbColor(formattedDB);
  const vuPercent = Math.min(100, Math.max(0, ((formattedDB - 40) / 65) * 100));
  const gradientId = `fill-${String(last.sensorId).replace(/\W/g, '')}`;
  const axisStyle = { fill: '#444', fontSize: 10, fontFamily: 'JosefinSans, Arial, sans-serif' };

  return (
    <div className="sensor-card">
      <div className="sensor-card-header">
        <h2 className="sensor-card-name">{last.sensorName}</h2>
        <div className="sensor-card-meta">
          <span>#{last.sensorId}</span>
          <span>{time}</span>
        </div>
      </div>

      <div className="sensor-card-display">
        <div
          className="color-ring"
          style={{ borderColor: dbColor, boxShadow: `0 0 20px ${dbColor}44` }}
        >
          <div className="lcd-screen" style={{ '--db-color': dbColor }}>
            <NumberFormatter number={formattedDB} />
            <p className="lcd-backdrop">000</p>
          </div>
        </div>
        <span className="db-unit" style={{ color: dbColor }}>dB SPL</span>
      </div>

      <div className="vu-bar">
        <div className="vu-bar-mask" style={{ width: `${100 - vuPercent}%` }} />
      </div>

      <Comparables decibel={formattedDB} />

      <div className="sensor-chart">
        <ResponsiveContainer width="100%" height={150}>
          <AreaChart data={data} margin={{ top: 5, right: 5, left: -10, bottom: 0 }}>
            <defs>
              {/* Y-axis gradient: hard stops at 90 dB (16.7% from top) and 85 dB (25% from top)
                  based on fixed domain [40, 100] → range of 60 dB */}
              <linearGradient id={`${gradientId}-stroke`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%"    stopColor="#ff1744" />
                <stop offset="16.7%" stopColor="#ff1744" />
                <stop offset="16.7%" stopColor="#ffd740" />
                <stop offset="25%"   stopColor="#ffd740" />
                <stop offset="25%"   stopColor="#00e676" />
                <stop offset="100%"  stopColor="#00e676" />
              </linearGradient>
              <linearGradient id={`${gradientId}-fill`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%"    stopColor="#ff1744" stopOpacity={0.4} />
                <stop offset="16.7%" stopColor="#ff1744" stopOpacity={0.4} />
                <stop offset="16.7%" stopColor="#ffd740" stopOpacity={0.3} />
                <stop offset="25%"   stopColor="#ffd740" stopOpacity={0.3} />
                <stop offset="25%"   stopColor="#00e676" stopOpacity={0.2} />
                <stop offset="100%"  stopColor="#00e676" stopOpacity={0}   />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e1e1e" />
            <XAxis tick={axisStyle} dataKey="time" />
            <YAxis tick={axisStyle} domain={[40, 100]} />
            <Tooltip
              contentStyle={{ backgroundColor: '#141414', border: `1px solid ${dbColor}44`, borderRadius: '0.4em' }}
              labelStyle={{ color: '#555' }}
              itemStyle={{ color: dbColor }}
            />
            <Area
              type="monotone"
              dataKey="dbLevel"
              stroke={`url(#${gradientId}-stroke)`}
              strokeWidth={1.5}
              fillOpacity={1}
              fill={`url(#${gradientId}-fill)`}
              isAnimationActive={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

Dbmeter.propTypes = {
  sensor: PropTypes.array.isRequired,
};

export default Dbmeter;
