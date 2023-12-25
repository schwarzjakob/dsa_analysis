import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CharacterData from './CharacterData'
import StartScreen from './StartScreen';
import CharacterManagement from './CharacterManagement';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<StartScreen />} />
        <Route path="/talents/:characterName" element={<CharacterData />} />
        <Route path="/characters" element={<CharacterManagement />} />
      </Routes>
    </Router>
  );
}

export default App;