import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainScreen from './MainScreen';
import FileUpload from './FileUpload';
import CharacterData from './CharacterData'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainScreen />} />
        <Route path="/upload" element={<FileUpload />} />
        <Route path="/talents/:characterName" element={<CharacterData />} />
      </Routes>
    </Router>
  );
}

export default App;