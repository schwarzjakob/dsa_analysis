from typing import Optional, List, Any, Dict
from psycopg2.extras import execute_values

from config.logger_config import logger
from models.database import Database


class Dsa5DatabaseService:
    def __init__(self):
        self.database = Database()

    def get_characters(self) -> List[Dict[str, Any]]:
        """
        Get all characters from the database.

        :return: List of characters.
        """
        query = "SELECT * FROM dsa5.actors;"
        characters = self.database.fetch_query(query)

        return characters
