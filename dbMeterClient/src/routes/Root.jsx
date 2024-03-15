import "../style/Style.css";
import Dbmeter from "../components/DBMeter/dbmeter";

function App() {
  return (
    <>
      <h1>ACC DB Meter Application</h1>
      <Dbmeter />

      <ul>
        <li>
          <a href="debug">Debug</a>
        </li>
      </ul>
    </>
  );
}

export default App;
