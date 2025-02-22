from typing import Optional, List, Any, Dict

from models.database import Database


class Dsa5DatabaseService:
    def __init__(self):
        self.database = Database()

    def get_characters(self) -> List[Dict[str, Any]]:
        """
        Get all characters from the database.

        :return: List of characters.
        """
        query = "SELECT id, name, image_url FROM dsa5.characters;"
        characters = self.database.fetch_query(query)

        return characters if characters is not None else []

    def get_character(self, character_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a character from the database.

        :param character_id: Character ID.
        :return: Character.
        """
        query = "SELECT * FROM dsa5.characters WHERE id = %s;"
        result = self.database.fetch_query(query, (character_id,))
        character = result[0] if result is not None and len(result) > 0 else None

        return character
