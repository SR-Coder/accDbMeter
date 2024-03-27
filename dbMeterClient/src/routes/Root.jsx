import "../style/Style.scss";
import TheRack from "../components/TheRack/TheRack";

function App() {
  return (
    <div className="app">
      <h1 className="app-header">DB Meter</h1>
      <TheRack />
      <ul>
        <li>
          <a href="debug">Debug</a>
        </li>
      </ul>
    </div>
  );
}

export default App;
