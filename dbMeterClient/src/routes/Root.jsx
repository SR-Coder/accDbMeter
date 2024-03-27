import "../style/Style.scss";
import TheRack from "../components/TheRack/TheRack";

function App() {
  return (
    <>
      <h1>ACC DB Meter Application</h1>
      <TheRack />

      <ul>
        <li>
          <a href="debug">Debug</a>
        </li>
      </ul>
    </>
  );
}

export default App;
