import logging
from typing import Optional, List, Any, Dict
import pandas as pd

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

    def get_characters_and_aliases(self):
        """
        Fetch all characters and their aliases as a single flat list.

        Returns:
            [ "Character One", "Character Two", "Alias Three", "Alias Four" ]
        """
        query = "SELECT name, alias FROM characters"
        results = self.database.fetch_query(query)

        if not results:
            return []

        # Flatten the list: Include the character name and all aliases
        return [name for row in results for name in ([row["name"]] + (row["alias"] if row["alias"] else []))]

    def get_talents(self):
        """
        Fetch all valid talent names from the database and return as a dictionary.
        """
        query = "SELECT talent_name FROM talents"
        results = self.database.fetch_query(query)
        return {row["talent_name"]: row for row in results} if results else {}

    def get_spells(self):
        """
        Fetch all valid spell names from the database and return as a set.
        """
        query = "SELECT spell_name FROM spells"
        results = self.database.fetch_query(query)
        return {row["spell_name"] for row in results} if results else {}

    def get_attacks(self):
        """
        Fetch all valid attack names from the database and return as a set.
        """
        query = "SELECT attack_name FROM attacks"
        results = self.database.fetch_query(query)
        return {row["attack_name"] for row in results} if results else {}

    def insert_traits_rolls(self, traits: pd.DataFrame) -> None:
        """
        Insert rows from traits into traits_rolls.
        """
        if not traits:
            return

        # A row-by-row example
        insert_query = """
            INSERT INTO traits_rolls
                (character_id, trait_id, modifier, success, tap_zfp, taw_zfw)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        with self.database.get_connection() as conn:
            with conn.cursor() as cur:
                for row in traits:
                    character_id = self.get_character_id_by_name(row["character_name"])

                    trait_id_query_result = self.database.fetch_query(
                        "SELECT trait_id FROM character_traits WHERE trait_name = %s", [row["talent"]]
                    )

                    trait_id = trait_id_query_result[0][0] if trait_id_query_result else None

                    if character_id is None:
                        self.logger.warning(f"Character '{row['character_name']}' not found in database. Skipping...")
                        continue

                    cur.execute(
                        insert_query,
                        [
                            character_id,
                            trait_id,
                            row["modifier"],
                            row["success"],
                            row["tap_zfp"],
                            row["taw_zfw"],
                        ],
                    )
                conn.commit()

    def insert_talents_rolls(self, talents: pd.DataFrame) -> None:
        """
        Insert rows from talents into talents_rolls, dynamically resolving character_id, category, and traits.
        """
        if not talents:

            return

        insert_query = """
            INSERT INTO talents_rolls
                (character_id, talent_id, modifier, success,
                tap_zfp, taw_zfw, trait_value1, trait_value2, trait_value3)
            SELECT
                %s AS character_id,
                t.talent_id AS talent_id,
                %s AS modifier,
                %s AS success,
                %s AS tap_zfp,
                %s AS taw_zfw,
                %s AS trait_value1,
                %s AS trait_value2,
                %s AS trait_value3
            FROM talents t
            WHERE t.talent_name = %s
        """

        with self.database.get_connection() as conn:
            with conn.cursor() as cur:
                for row in talents:
                    character_id = self.get_character_id_by_name(row["character_name"])

                    if character_id is None:
                        self.logger.warning(f"Character '{row['character_name']}' not found in database. Skipping...")
                        continue

                    cur.execute(
                        insert_query,
                        [
                            character_id,
                            row["modifier"],
                            row["success"],
                            row["tap_zfp"],
                            row["taw_zfw"],
                            row["trait_value1"],
                            row["trait_value2"],
                            row["trait_value3"],
                            row["talent"],
                        ],
                    )
                    conn.commit()

    def insert_spells_rolls(self, spells: pd.DataFrame) -> None:
        """
        Insert rows from spells into spells_rolls.
        """
        if not spells:
            return

        insert_query = """
            INSERT INTO spells_rolls
                (character_id, spell_id, modifier, success,
                 tap_zfp, taw_zfw, trait_value1, trait_value2, trait_value3)
            SELECT
                %s AS character_id,
                s.spell_id AS spell_id,
                %s AS modifier,
                %s AS success,
                %s AS tap_zfp,
                %s AS taw_zfw,
                %s AS trait_value1,
                %s AS trait_value2,
                %s AS trait_value3
            FROM spells s
            WHERE s.spell_name = %s
        """

        with self.database.get_connection() as conn:
            with conn.cursor() as cur:
                for row in spells:
                    character_id = self.get_character_id_by_name(row["character_name"])

                    if character_id is None:
                        self.logger.warning(f"Character '{row['character_name']}' not found in database. Skipping...")
                        continue

                    cur.execute(
                        insert_query,
                        [
                            character_id,
                            row["modifier"],
                            row["success"],
                            row["tap_zfp"],
                            row["taw_zfw"],
                            row["trait_value1"],
                            row["trait_value2"],
                            row["trait_value3"],
                            row["spell"],
                        ],
                    )
                conn.commit()

    def insert_attacks_rolls(self, attacks: pd.DataFrame) -> None:
        """
        Insert rows from attacks into attacks_rolls.
        """
        if not attacks:
            return

        insert_query = """
            INSERT INTO attacks_rolls
                (character_id, attack_id, modifier, success, tap_zfp, taw_zfw)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        with self.database.get_connection() as conn:
            with conn.cursor() as cur:
                for row in attacks:
                    character_id = self.get_character_id_by_name(row["character_name"])
                    attack_id_query_result = self.database.fetch_query(
                        "SELECT attack_id FROM attacks WHERE attack_name = %s", [row["attack"]]
                    )

                    attack_id = attack_id_query_result[0][0] if attack_id_query_result else None

                    if character_id is None:
                        self.logger.warning(f"Character '{row['character_name']}' not found. Skipping...")
                        continue

                    if attack_id is None:
                        self.logger.warning(f"Attack '{row['attack']}' not found. Skipping...")
                        continue

                    cur.execute(
                        insert_query,
                        [
                            character_id,
                            attack_id,
                            row["modifier"],
                            row["success"],
                            row["tap_zfp"],
                            row["taw_zfw"],
                        ],
                    )
                conn.commit()

    def insert_initiatives(self, initiatives: pd.DataFrame) -> None:
        """
        Insert rows from initiatives into initiative_rolls.
        """
        if not initiatives:
            return

        insert_query = """
            INSERT INTO initiative_rolls
                (character_id, rolled_ini, current_ini, modifier)
            VALUES(%s, %s, %s, %s)
        """
        with self.database.get_connection() as conn:
            with conn.cursor() as cur:
                for row in initiatives:
                    character_id = self.get_character_id_by_name(row["character_name"])

                    if character_id is None:
                        self.logger.warning(f"Character '{row['character_name']}' not found in database. Skipping...")
                        continue

                    cur.execute(
                        insert_query,
                        [
                            character_id,
                            row["rolled_ini"],
                            row["current_ini"],
                            row["modifier"],
                        ],
                    )
                conn.commit()

    def insert_total_damage(self, total_damage: pd.DataFrame) -> None:
        """
        Insert rows into total_damage if they don't exist.
        If they do exist, update the total_damage value.
        """
        if not total_damage:
            return

        with self.database.get_connection() as conn:
            with conn.cursor() as cur:
                for row in total_damage:
                    character_name = row["character_name"]
                    damage_value = row["total_damage"]

                    # Use the updated function to fetch character_id (handles name & alias)
                    character_id = self.get_character_id_by_name(character_name)

                    if character_id is None:
                        self.logger.warning(f"Character '{character_name}' not found in database. Skipping...")
                        continue  # Skip if character is not found

                    # Check if total_damage entry exists
                    cur.execute("SELECT total_damage FROM total_damage WHERE character_id = %s", (character_id,))
                    existing = cur.fetchone()

                    if existing:
                        # Update the existing row
                        cur.execute(
                            "UPDATE total_damage SET total_damage = total_damage + %s WHERE character_id = %s",
                            (damage_value, character_id),
                        )
                    else:
                        # Insert a new row
                        cur.execute(
                            "INSERT INTO total_damage (character_id, total_damage) VALUES (%s, %s)",
                            (character_id, damage_value),
                        )

                    conn.commit()

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
        Returns the character_id given a character name or alias, or None if not found.
        """
        query = """
            SELECT id FROM characters
            WHERE name = %s OR %s = ANY(alias)
            LIMIT 1
        """
        result = self.database.fetch_query(query, [character_name, character_name])

        if result:
            character_id = result[0]["id"]
            return character_id

        return None

    def fetch_talents_for_character(self, character_id: int):
        """
        Fetch talents data for a given character_id.
        """
        query = """
            SELECT
                talents.talent_name AS talent,
                COUNT(*) AS talent_count,
                COALESCE(AVG(success::int), 0) AS success_rate,
                COALESCE(1 - AVG(success::int), 0) AS failure_rate,
                COALESCE(AVG(tap_zfp), 0) AS avg_score,
                COALESCE(STDDEV(tap_zfp), 0) AS std_dev
            FROM talents_rolls
            JOIN talents ON talents.talent_id = talents_rolls.talent_id
            WHERE character_id = %s
            GROUP BY talents.talent_name
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
            SELECT character_traits.trait_abbreviation AS trait, COUNT(*) AS trait_count
            FROM (
                SELECT talent_trait_one_id AS trait_id
                FROM talents
                LEFT JOIN talents_rolls ON talents.talent_id = talents_rolls.talent_id
                WHERE character_id = %s
                UNION ALL
                SELECT talent_trait_two_id AS trait_id
                FROM talents
                LEFT JOIN talents_rolls ON talents.talent_id = talents_rolls.talent_id 
                WHERE character_id = %s
                UNION ALL
                SELECT talent_trait_three_id AS trait_id
                FROM talents
                LEFT JOIN talents_rolls ON talents.talent_id = talents_rolls.talent_id
                WHERE character_id = %s
            ) AS combined_trait_ids
            LEFT JOIN character_traits ON character_traits.trait_id = combined_trait_ids.trait_id
            GROUP BY trait_abbreviation
        """
        return self.database.fetch_query(query, [character_id, character_id, character_id])

    def fetch_categories_for_character(self, character_id: int):
        """
        Get how many times each category was used from talents_rolls.
        """
        query = """
            SELECT talent_categories.talent_category_name AS category, COUNT(*) AS category_count
            FROM talents_rolls
            LEFT JOIN talents ON talents.talent_id = talents_rolls.talent_id
            LEFT JOIN talent_categories ON talent_categories.talent_category_id = talents.talent_category_id
            WHERE character_id = %s
            GROUP BY talent_category_name
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
            LEFT JOIN talents ON talents.talent_id = talents_rolls.talent_id
            WHERE character_id = %s AND talent_name = %s
        """
        return self.database.fetch_query(query, [character_id, talent_name])

    def fetch_talent_line_chart(self, character_id: int, talent_name: str):
        """
        Return line chart data (id as sequence, tap_zfp) for a given talent
        """
        query = """
            SELECT id AS sequence, tap_zfp
            FROM talents_rolls
            LEFT JOIN talents ON talents.talent_id = talents_rolls.talent_id
            WHERE character_id = %s AND talent_name = %s
            ORDER BY id
        """
        return self.database.fetch_query(query, [character_id, talent_name])

    def fetch_attacks_for_character(self, character_id: int):
        """
        Summaries for all attacks for a given character
        """
        query = """
            SELECT
                attacks.attack_name AS attack,
                COUNT(*) AS attack_count,
                AVG(success::int) AS success_rate,
                1 - AVG(success::int) AS failure_rate,
                AVG(tap_zfp) AS avg_score,
                STDDEV(tap_zfp) AS std_dev
            FROM attacks_rolls
            LEFT JOIN attacks ON attacks.attack_id = attacks_rolls.attack_id
            WHERE character_id = %s
            GROUP BY attacks.attack_name
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
            LEFT JOIN attacks ON attacks.attack_id = attacks_rolls.attack_id
            WHERE character_id = %s AND attack_name = %s
        """
        return self.database.fetch_query(query, [character_id, attack_name])

    def fetch_attack_line_chart(self, character_id: int, attack_name: str):
        """
        Return line chart data (id as sequence, tap_zfp) for a given attack
        """
        query = """
            SELECT id AS sequence, tap_zfp
            FROM attacks_rolls
            LEFT JOIN attacks ON attacks.attack_id = attacks_rolls.attack_id
            WHERE character_id = %s AND attack_name = %s
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
