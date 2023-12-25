import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CharacterData from './CharacterData'
import Login from './Login';
import StartScreen from './StartScreen';
import CharacterManagement from './CharacterManagement';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/start" element={<StartScreen />} />
        <Route path="/talents/:characterName" element={<CharacterData />} />
        <Route path="/characters" element={<CharacterManagement />} />
      </Routes>
    </Router>
  );
}

export default App;