import React, { useState, useEffect } from "react";
import axios from "axios";
import Home from "../components/layout/Home";
import { fetchCharacters } from "../hooks/characters/fetchCharacters";
import "../App.css";

const CharacterManagement = () => {
  const [characters, setCharacters] = useState([]);
  const [selectedCharacter, setSelectedCharacter] = useState(null);
  const [editing, setEditing] = useState(false);
  const [characterDetails, setCharacterDetails] = useState({
    name: "",
    alias: [],
    Mut: "",
    Klugheit: "",
    Intuition: "",
    Charisma: "",
    Fingerfertigkeit: "",
    Gewandtheit: "",
    Konstitution: "",
    Körperkraft: "",
  });

  useEffect(() => {
    const loadCharacters = async () => {
      try {
        const charactersData = await fetchCharacters();
        setCharacters(charactersData);
      } catch (error) {
        console.error("Error fetching characters", error);
      }
    };

    loadCharacters();
  }, []);

  const handleCharacterSelect = (e) => {
    const characterName = e.target.value;
    const character = characters.find((c) => c.name === characterName);
    setSelectedCharacter(characterName);
    setCharacterDetails({
      ...character.traits,
      alias: character.alias || [], // This line handles aliases
      name: character.name,
    });
    setEditing(false); // Reset editing mode
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCharacterDetails((prevDetails) => ({
      ...prevDetails,
      [name]: value,
    }));
  };

  const handleAliasChange = (index, value) => {
    const updatedAliases = [...characterDetails.alias];
    updatedAliases[index] = value;
    setCharacterDetails((prevDetails) => ({
      ...prevDetails,
      alias: updatedAliases,
    }));
  };

  const addAlias = () => {
    setCharacterDetails((prevDetails) => ({
      ...prevDetails,
      alias: [...prevDetails.alias, ""],
    }));
  };

  const removeAlias = (index) => {
    const updatedAliases = characterDetails.alias.filter((_, i) => i !== index);
    setCharacterDetails((prevDetails) => ({
      ...prevDetails,
      alias: updatedAliases,
    }));
  };

  const saveCharacter = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:5000/characters_management/update-character",
        characterDetails
      );
      alert("Character updated successfully");
      const charactersData = await fetchCharacters();
      setCharacters(charactersData); // Refresh the characters list
      setEditing(false); // Exit editing mode
    } catch (error) {
      console.error("Error updating character", error);
      alert("Error updating character");
    }
  };

  return (
    <>
      <div>
        <Home />
      </div>
      <div className="main-container">
        <h1>Character Management</h1>
        <div className="character-select-container">
          <select
            value={selectedCharacter || ""}
            onChange={handleCharacterSelect}
          >
            <option value="">Select a Character</option>
            {characters.map((character) => (
              <option key={character.name} value={character.name}>
                {character.name}
              </option>
            ))}
          </select>
        </div>

        {selectedCharacter && (
          <div className="character-details-container">
            <h3>Attributes</h3>
            {!editing ? (
              <>
                <table className="character-attributes">
                  <tbody>
                    {Object.entries(characterDetails).map(([key, value]) =>
                      key !== "alias" && key !== "name" ? (
                        <tr key={key}>
                          <td className="attribute-label">{key}</td>
                          <td className="attribute-value">{value}</td>
                        </tr>
                      ) : null
                    )}
                  </tbody>
                </table>
                <div className="character-aliases">
                  <h3>Aliases</h3>
                  {characterDetails.alias.length > 0 ? (
                    <ul>
                      {characterDetails.alias.map((alias, index) => (
                        <li key={index}>{alias}</li>
                      ))}
                    </ul>
                  ) : (
                    <p>No aliases</p>
                  )}
                </div>
                <button className="button" onClick={() => setEditing(true)}>
                  Edit Character
                </button>
              </>
            ) : (
              <>
                <table className="character-attributes-edit">
                  <tbody>
                    {Object.entries(characterDetails).map(([key, value]) =>
                      key !== "alias" && key !== "name" ? (
                        <tr key={key}>
                          <td className="attribute-label">{key}</td>
                          <td>
                            <input
                              type="number"
                              name={key}
                              value={value}
                              onChange={handleInputChange}
                            />
                          </td>
                        </tr>
                      ) : null
                    )}
                  </tbody>
                </table>
                <div className="character-aliases-edit">
                  <h3>Aliases</h3>
                  {characterDetails.alias.map((alias, index) => (
                    <div key={index} className="alias-input">
                      <input
                        type="text"
                        value={alias}
                        onChange={(e) =>
                          handleAliasChange(index, e.target.value)
                        }
                      />
                      <button onClick={() => removeAlias(index)}>Remove</button>
                    </div>
                  ))}
                  <button className="button" onClick={addAlias}>
                    Add Alias
                  </button>
                </div>
                <div className="edit-actions">
                  <button className="button" onClick={saveCharacter}>
                    Save
                  </button>
                  <button className="button" onClick={() => setEditing(false)}>
                    Cancel
                  </button>
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </>
  );
};

export default CharacterManagement;
