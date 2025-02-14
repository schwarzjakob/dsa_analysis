import React from "react";
import { Routes, Route } from "react-router-dom";
import NavBar from "./components/NavBar";
import CharactersView from "./views/CharactersView";
import CharacterView from "./views/CharacterView";

const Dsa5App = () => {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<CharactersView />} />
        <Route path="/characters" element={<CharactersView />} />
        <Route path="/character/:id" element={<CharacterView />} />
      </Routes>
    </>
  );
};

export default Dsa5App;
