import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import CharacterData from "./views/CharacterDashboard";
import StartScreen from "./views/StartScreen";
import CharacterManagement from "./views/CharacterManagement";
import TraitsForSelectedTalents from "./views/TraitsForSelectedTalents";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<StartScreen />} />
        <Route path="/talents/:characterName" element={<CharacterData />} />
        <Route path="/characters" element={<CharacterManagement />} />
        <Route
          path="/traits-for-selected-talents"
          element={<TraitsForSelectedTalents />}
        />
      </Routes>
    </Router>
  );
}

export default App;
