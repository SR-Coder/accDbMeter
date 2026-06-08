import "../style/Style.scss";
import TheRack from "../components/TheRack/TheRack";

function App() {
  return (
    <div className="app">
      <h1 className="app-header">ACC dB Meter</h1>
      <TheRack />
    </div>
  );
}

export default App;
