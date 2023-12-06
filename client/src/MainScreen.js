import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './App.css'
import Header from './Header.js'

function MainScreen() {
  const navigate = useNavigate();
  const [selectedCharacter, setSelectedCharacter] = useState('');

  const handleCharacterChange = (e) => {
    //console.log(e)
    setSelectedCharacter(e.target.value);
  };

  const [characters, setCharacters] = useState([]);

  useEffect(() => {
      const fetchCharacters = async () => {
          try {
              const response = await axios.get('http://127.0.0.1:5000/characters');
              console.log(response.data);
              setCharacters(response.data.characters);
          } catch (error) {
              console.error('Error fetching characters', error);
          }
      };

      fetchCharacters();
  }, []);

  const handleAddCharacter = () => {
    alert("This function is not available at the moment. We are working on it :)")
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    if (selectedCharacter) {
      navigate(`/talents/${selectedCharacter}`);
      console.log(selectedCharacter)
    } else {
      console.log("No character selected");
    }
  };
  


  return (
    <><div>
      <Header />
    </div>
    <div className="main-container">
        <div className="form-container">
          <div>
            <button onClick={() => navigate('/upload')}>Upload a new Chatlog</button>
            <form onSubmit={handleSubmit}>
              <select onChange={handleCharacterChange} value={selectedCharacter}>
                <option value="">Select a Character</option>
                {characters.map((character, index) => (
                  <option key={index} value={character}>{character}</option>
                ))}
              </select>
              <button type="submit">Submit Character</button>
            </form>
            <button type="submit" onClick={handleAddCharacter}>Add new Character</button>
            {/* Other main screen content */}
          </div>
        </div>
      </div></>
  );

  
}

export default MainScreen;
