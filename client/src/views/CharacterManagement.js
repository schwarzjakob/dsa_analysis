import React, { useState, useEffect } from "react";
import axios from "axios";
import Home from "../components/layout/Home.js";
import "../App.css";

const CharacterManagement = () => {
  const [characters, setCharacters] = useState([]);
  const [newCharacterName, setNewCharacterName] = useState("");
  const [newCharacterAliases, setNewCharacterAliases] = useState("");

  useEffect(() => {
    fetchCharacters();
  }, []);

  const fetchCharacters = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/characters_management/characters");
      setCharacters(response.data.characters);
    } catch (error) {
      console.error("Error fetching characters", error);
    }
  };

  const addAlias = async (characterName) => {
    // Implement the logic to add an alias
  };

  const updateAlias = async (characterName) => {
    // Implement the logic to update an alias
  };

  const archiveCharacter = async (characterName, aliases) => {
    try {
        await axios.post("http://127.0.0.1:5000/characters_management/archive-character", { name: characterName, alias: aliases});
        fetchCharacters(); // Refresh the characters list
    } catch (error) {
        console.error("Error archiving character", error);
    }
  };

  const addCharacter = async () => {
    if (!newCharacterName.trim()) {
        alert("Character name cannot be empty.");
        return;
      }
    try {
      const characterData = {
        name: newCharacterName,
        alias: newCharacterAliases.split(",").map(alias => alias.trim())
      };
      await axios.post("http://127.0.0.1:5000/characters_management/add-character", characterData);
      fetchCharacters(); // Refresh the characters list

      // Clear the input fields
      setNewCharacterName("");
      setNewCharacterAliases("");
    } catch (error) {
        alert("Error adding character", error);
      console.error("Error adding character", error);
    }
  };
  

  return (
    <>
      <div>
        <Home />
      </div>
      <div className="table-container">
        <h1>Character Management</h1>
        <table className="">
          <thead>
            <tr>
              <th>Name</th>
              <th>Aliases</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {characters.map((character) => (
              <tr key={character.name}>
                <td>{character.name}</td>
                <td>
                  {character.alias && character.alias.length > 0 ? (
                    character.alias.map((alias) => (
                      <div key={alias}>{alias}</div>
                    ))
                  ) : (
                    <div>No Aliases</div>
                  )}
                </td>
                <td>
                  <button
                    className="button"
                    onClick={() => addAlias(character.name)}
                  >
                    Add Alias
                  </button>
                  <button
                    className="button"
                    onClick={() => updateAlias(character.name)}
                  >
                    Update Alias
                  </button>
                  <button
                    className="button"
                    onClick={() => archiveCharacter(character.name, character.alias)}
                  >
                    Archive Character
                  </button>
                </td>
              </tr>
            ))}
            <tr>
              <td>
                <input className="custom-input"
                  placeholder="Character name"
                  value={newCharacterName}
                  onChange={(e) => setNewCharacterName(e.target.value)}
                />
              </td>
              <td>
                <input className="custom-input"
                  placeholder="Character aliases (separate with commas)"
                  value={newCharacterAliases}
                  onChange={(e) => setNewCharacterAliases(e.target.value)}
                />
              </td>
              <td>
                <button className="button" onClick={() => addCharacter()}>
                  Add Character
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </>
  );
};

export default CharacterManagement;
