import logging
from typing import Optional, List, Any, Dict

from models.database import Database


class DatabaseService:
    """
    Encapsulates higher-level database queries/updates.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.database = Database()

    def get_characters(self):
        """
        Fetch all characters with their attributes.
        Returns a list of dicts or an empty list if none.
        """
        query = """
            SELECT 
                id, 
                name, 
                mut, 
                klugheit, 
                intuition, 
                charisma,
                fingerfertigkeit, 
                gewandtheit, 
                konstitution, 
                körperkraft, 
                alias
            FROM characters
        """
        results = self.database.fetch_query(query)
        if not results:
            return []

        character_list = []
        for row in results:
            character_list.append(
                {
                    "id": row["id"],
                    "name": row["name"],
                    "traits": {
                        "Mut": row["mut"],
                        "Klugheit": row["klugheit"],
                        "Intuition": row["intuition"],
                        "Charisma": row["charisma"],
                        "Fingerfertigkeit": row["fingerfertigkeit"],
                        "Gewandtheit": row["gewandtheit"],
                        "Konstitution": row["konstitution"],
                        "Körperkraft": row["körperkraft"],
                    },
                    "alias": row["alias"] if row["alias"] else [],
                }
            )
        return character_list

    def update_character(self, character_name: str, attributes: dict, aliases: list) -> bool:
        """
        Update the specified character with new attributes and aliases.
        """
        query = """
            UPDATE characters
            SET 
                mut = %s, 
                klugheit = %s, 
                intuition = %s, 
                charisma = %s,
                fingerfertigkeit = %s, 
                gewandtheit = %s, 
                konstitution = %s, 
                körperkraft = %s,
                alias = %s
            WHERE name = %s
        """
        params = [
            attributes["Mut"],
            attributes["Klugheit"],
            attributes["Intuition"],
            attributes["Charisma"],
            attributes["Fingerfertigkeit"],
            attributes["Gewandtheit"],
            attributes["Konstitution"],
            attributes["Körperkraft"],
            aliases,
            character_name,
        ]
        return self.database.execute_query(query, params)

    def insert_character(self, character_data: dict) -> bool:
        """
        Inserts a new character into the characters table.
        (Adjust fields as needed based on your schema)
        """
        query = """
            INSERT INTO characters (
                name, 
                mut, 
                klugheit, 
                intuition, 
                charisma,
                fingerfertigkeit, 
                gewandtheit, 
                konstitution, 
                körperkraft,
                alias
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = [
            character_data["name"],
            character_data["traits"]["Mut"],
            character_data["traits"]["Klugheit"],
            character_data["traits"]["Intuition"],
            character_data["traits"]["Charisma"],
            character_data["traits"]["Fingerfertigkeit"],
            character_data["traits"]["Gewandtheit"],
            character_data["traits"]["Konstitution"],
            character_data["traits"]["Körperkraft"],
            character_data.get("alias", []),
        ]
        return self.database.execute_query(query, params)

    def get_character_id_by_name(self, character_name: str) -> Optional[int]:
        """
        Returns the character_id given a character name, or None if not found.
        """
        query = "SELECT id FROM characters WHERE name = %s"
        results = self.database.fetch_query(query, [character_name])
        if results and len(results) > 0:
            return results[0]["id"]
        return None

    def fetch_talents_for_character(self, character_id: int):
        """
        Fetch talents data for a given character_id.
        """
        query = """
            SELECT 
                talent, 
                COUNT(*) AS talent_count,
                COALESCE(AVG(success::int), 0) AS success_rate,
                COALESCE(1 - AVG(success::int), 0) AS failure_rate,
                COALESCE(AVG(tap_zfp), 0) AS avg_score,
                COALESCE(STDDEV(tap_zfp), 0) AS std_dev
            FROM talents_rolls
            WHERE character_id = %s
            GROUP BY talent
        """
        return self.database.fetch_query(query, [character_id])

    def fetch_traits_values_for_character(self, character_id: int):
        """
        For each trait slot (1,2,3), get the average trait_value from talents_rolls
        """
        query = """
            SELECT 'Trait 1' AS trait, COALESCE(AVG(trait_value1), 0) AS avg_value 
            FROM talents_rolls 
            WHERE character_id = %s
            UNION ALL
            SELECT 'Trait 2' AS trait, COALESCE(AVG(trait_value2), 0) AS avg_value 
            FROM talents_rolls 
            WHERE character_id = %s
            UNION ALL
            SELECT 'Trait 3' AS trait, COALESCE(AVG(trait_value3), 0) AS avg_value 
            FROM talents_rolls 
            WHERE character_id = %s
        """
        return self.database.fetch_query(query, [character_id, character_id, character_id])

    def fetch_traits_relative_for_character(self, character_id: int):
        """
        Count usage of each trait (trait1, trait2, trait3) in talents_rolls.
        """
        query = """
            SELECT trait, COUNT(*) AS trait_count
            FROM (
                SELECT trait1 AS trait FROM talents_rolls WHERE character_id = %s
                UNION ALL
                SELECT trait2 AS trait FROM talents_rolls WHERE character_id = %s
                UNION ALL
                SELECT trait3 AS trait FROM talents_rolls WHERE character_id = %s
            ) AS combined_traits
            GROUP BY trait
        """
        return self.database.fetch_query(query, [character_id, character_id, character_id])

    def fetch_categories_for_character(self, character_id: int):
        """
        Get how many times each category was used from talents_rolls.
        """
        query = """
            SELECT category, COUNT(*) AS category_count
            FROM talents_rolls
            WHERE character_id = %s
            GROUP BY category
        """
        return self.database.fetch_query(query, [character_id])

    def fetch_talent_statistics(self, character_id: int, talent_name: str):
        """
        Example: number of attempts, success_rate, avg_score for a specific talent
        """
        query = """
            SELECT COUNT(*) AS attempts,
                   AVG(success::int) AS success_rate,
                   AVG(tap_zfp) AS avg_score,
                   STDDEV(tap_zfp) AS std_dev
            FROM talents_rolls
            WHERE character_id = %s AND talent = %s
        """
        return self.database.fetch_query(query, [character_id, talent_name])

    def fetch_talent_line_chart(self, character_id: int, talent_name: str):
        """
        Return line chart data (id as sequence, tap_zfp) for a given talent
        """
        query = """
            SELECT id AS sequence, tap_zfp
            FROM talents_rolls
            WHERE character_id = %s AND talent = %s
            ORDER BY id
        """
        return self.database.fetch_query(query, [character_id, talent_name])

    def fetch_attacks_for_character(self, character_id: int):
        """
        Summaries for all attacks for a given character
        """
        query = """
            SELECT 
                attack, 
                COUNT(*) AS attack_count,
                AVG(success::int) AS success_rate,
                1 - AVG(success::int) AS failure_rate,
                AVG(tap_zfp) AS avg_score,
                STDDEV(tap_zfp) AS std_dev
            FROM attacks_rolls
            WHERE character_id = %s
            GROUP BY attack
        """
        return self.database.fetch_query(query, [character_id])

    def fetch_attack_statistics(self, character_id: int, attack_name: str):
        """
        Summaries for a specific attack
        """
        query = """
            SELECT 
                COUNT(*) AS attempts,
                AVG(success::int) AS success_rate,
                AVG(tap_zfp) AS avg_score,
                STDDEV(tap_zfp) AS std_dev
            FROM attacks_rolls
            WHERE character_id = %s AND attack = %s
        """
        return self.database.fetch_query(query, [character_id, attack_name])

    def fetch_attack_line_chart(self, character_id: int, attack_name: str):
        """
        Return line chart data (id as sequence, tap_zfp) for a given attack
        """
        query = """
            SELECT id AS sequence, tap_zfp
            FROM attacks_rolls
            WHERE character_id = %s AND attack = %s
            ORDER BY id
        """
        return self.database.fetch_query(query, [character_id, attack_name])

    def fetch_traits_for_talents(self, talents_name_list: List[str]):
        """
        Return trait abbreviations for each talent in the list.
        """
        query = """
            SELECT ct1.trait_abbreviation, ct2.trait_abbreviation, ct3.trait_abbreviation
            FROM talents t
            JOIN character_traits ct1 ON t.talent_trait_one_id = ct1.trait_id
            JOIN character_traits ct2 ON t.talent_trait_two_id = ct2.trait_id
            JOIN character_traits ct3 ON t.talent_trait_three_id = ct3.trait_id
            WHERE t.talent_name = ANY(%s);
        """
        return self.database.fetch_query(query, [talents_name_list])

    def fetch_talents_and_categories(self):
        """
        Return all talents with their category name.
        """
        query = """
            SELECT t.talent_name, tc.talent_category_name
            FROM talents t
            JOIN talent_categories tc ON t.talent_category_id = tc.talent_category_id
        """
        return self.database.fetch_query(query)

    def close(self):
        """Close the database pool."""
        self.database.close()
