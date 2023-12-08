import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FileUpload from './FileUpload';
import CharacterData from './CharacterData'
import StartScreen from './StartScreen';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<StartScreen />} />
        <Route path="/upload" element={<FileUpload />} />
        <Route path="/talents/:characterName" element={<CharacterData />} />
      </Routes>
    </Router>
  );
}

export default App;