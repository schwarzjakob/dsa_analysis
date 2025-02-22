import React, { useEffect } from "react";
import { Routes, Route } from "react-router-dom";
import CharacterData from "./views/CharacterDashboard";
import StartScreen from "./views/StartScreen";
import CharacterManagement from "./views/CharacterManagement";
import TraitsForSelectedTalents from "./views/TraitsForSelectedTalents";

function App() {
  // Use for styling
  useEffect(() => {
    document.body.classList.add("dsa4");
    return () => {
      document.body.classList.remove("dsa4");
    };
  }, []);

  return (
    <Routes>
      <Route path="/" element={<StartScreen />} />
      <Route path="/talents/:characterName" element={<CharacterData />} />
      <Route path="/characters" element={<CharacterManagement />} />
      <Route
        path="/traits-for-selected-talents"
        element={<TraitsForSelectedTalents />}
      />
    </Routes>
  );
}

export default App;
