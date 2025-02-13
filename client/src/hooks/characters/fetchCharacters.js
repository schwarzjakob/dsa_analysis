export const fetchCharacters = async () => {
  try {
    const response = await fetch("/dsa4/characters_management/characters");
    const data = await response.json();
    return (
      data.characters.map((char) => ({
        name: char.name,
        traits: char.traits,
      })) || []
    );
  } catch (error) {
    console.error("Error fetching characters:", error);
    return [];
  }
};
