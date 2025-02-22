import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "./landing/LandingPage";
import Dsa5App from "./dsa5/App";
import Dsa4App from "./dsa4/App";
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dsa5/*" element={<Dsa5App />} />
        <Route path="/dsa4/*" element={<Dsa4App />} />
      </Routes>
    </Router>
  );
}

export default App;
