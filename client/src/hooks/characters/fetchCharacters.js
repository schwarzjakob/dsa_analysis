import axios from "axios";

export const fetchCharacters = async () => {
  try {
    const response = await axios.get(
      "http://127.0.0.1:5000/characters_management/characters"
    );
    const characterNames = response.data.characters.map((char) => char.name);
    return characterNames;
  } catch (error) {
    console.error("Error fetching characters", error);
  }
};
