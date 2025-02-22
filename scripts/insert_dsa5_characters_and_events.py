import os
import json
import psycopg2

# Set file paths for JSON data
CHARACTERS_FILE = "integrations/_temp/events/characters.json"
TRAITS_FILE = "integrations/_temp/events/traits.json"
TALENTS_FILE = "integrations/_temp/events/talents.json"
SPELLS_FILE = "integrations/_temp/events/spells.json"
ATTACKS_FILE = "integrations/_temp/events/attacks.json"
PARRY_FILE = "integrations/_temp/events/parries.json"
DODGE_FILE = "integrations/_temp/events/dodges.json"


# Function to load JSON data from file
def load_json_data(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file {file_path}: {e}")
        return []


# Establish database connection
def connect_db():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise EnvironmentError("DATABASE_URL environment variable is not set.")
    return psycopg2.connect(database_url)


# Insert characters into the database
def insert_characters(conn, characters):
    query = """
    INSERT INTO dsa5.characters
    (id, name, image_url, type, mut, klugheit, intuition, charisma, fingerfertigkeit, gewandtheit, konstitution, köperkraft,
     life_points_value, life_points_max, astral_energy_value, astral_energy_max, initiative, species, culture, career,
     experience_total, experience_spent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """
    with conn.cursor() as cur:
        for char in characters:
            cur.execute(
                query,
                (
                    char["id"],
                    char["name"],
                    char["image_url"],
                    char.get("type"),
                    char["mu"],
                    char["kl"],
                    char["in"],
                    char["ch"],
                    char["ff"],
                    char["ge"],
                    char["ko"],
                    char["kk"],
                    char["life_points_value"],
                    char["life_points_max"],
                    char["astral_energy_value"],
                    char["astral_energy_max"],
                    char["initiative"],
                    char.get("species"),
                    char.get("culture"),
                    char.get("career"),
                    char.get("experience_total"),
                    char.get("experience_spent"),
                ),
            )
    conn.commit()


# Insert trait rolls into the database
def insert_trait_rolls(conn, trait_rolls):
    # Fetch all trait abbreviations and their corresponding IDs into a dictionary
    trait_lookup = {}
    with conn.cursor() as cur:
        cur.execute("SELECT trait_abbreviation, id FROM dsa5.traits;")
        rows = cur.fetchall()
        trait_lookup = {row[0]: row[1] for row in rows}  # {trait_abbreviation: trait_id}

    query = """
    INSERT INTO dsa5.trait_rolls
    (event_id, character_id, timestamp, trait_id, trait_value, modifier, roll_result, success_level)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (event_id) DO NOTHING;
    """

    check_character_query = "SELECT EXISTS(SELECT 1 FROM dsa5.characters WHERE id = %s);"

    with conn.cursor() as cur:
        for trait in trait_rolls:
            # Check if the character exists
            cur.execute(check_character_query, (trait["character_id"],))
            exists = cur.fetchone()[0]

            if not exists:
                print(f"Skipping trait roll {trait['event_id']} - Character {trait['character_id']} not found.")
                continue  # Skip insertion for missing characters

            # Get trait_id based on trait abbreviation
            trait_id = trait_lookup.get(trait["trait_abbreviation"])

            if not trait_id:
                print(
                    f"Skipping trait roll {trait['event_id']} - Trait abbreviation {trait['trait_abbreviation']} not found."
                )
                continue  # Skip insertion for unknown trait abbreviation

            # Insert the trait roll data
            cur.execute(
                query,
                (
                    trait["event_id"],
                    trait["character_id"],
                    trait["timestamp"],
                    trait_id,
                    trait["trait_value"],
                    trait["modifier"],
                    trait["roll_result"],
                    trait["success_level"],
                ),
            )
    conn.commit()


# Insert talent rolls into the database
def insert_talent_rolls(conn, talent_rolls):
    # Fetch all trait abbreviations and their corresponding IDs into a dictionary
    trait_lookup = {}
    with conn.cursor() as cur:
        cur.execute("SELECT trait_abbreviation, id FROM dsa5.traits;")
        rows = cur.fetchall()
        trait_lookup = {row[0]: row[1] for row in rows}  # {trait_abbreviation: trait_id}

    query = """
    INSERT INTO dsa5.talent_rolls 
    (event_id, character_id, timestamp, talent_name, talent_group, talent_value, talent_trait_1_id, talent_trait_2_id, talent_trait_3_id,
     modifier, result, quality_step, success_level, description)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (event_id) DO NOTHING;
    """

    check_character_query = "SELECT EXISTS(SELECT 1 FROM dsa5.characters WHERE id = %s);"

    with conn.cursor() as cur:
        for talent in talent_rolls:
            # Check if the character exists
            cur.execute(check_character_query, (talent["character_id"],))
            exists = cur.fetchone()[0]

            if not exists:
                print(f"Skipping talent roll {talent['event_id']} - Character {talent['character_id']} not found.")
                continue  # Skip insertion for missing characters

            # Fetch trait IDs from the lookup dictionary (default to None if not found)
            trait_1_id = trait_lookup.get(talent.get("talent_trait_1"))
            trait_2_id = trait_lookup.get(talent.get("talent_trait_2"))
            trait_3_id = trait_lookup.get(talent.get("talent_trait_3"))

            # Insert the talent roll data
            cur.execute(
                query,
                (
                    talent["event_id"],
                    talent["character_id"],
                    talent["timestamp"],
                    talent["talent_name"],
                    talent["talent_group"],
                    talent["talent_value"],
                    trait_1_id,
                    trait_2_id,
                    trait_3_id,
                    talent["modifier"],
                    talent["result"],
                    talent["quality_step"],
                    talent["success_level"],
                    talent["description"],
                ),
            )
    conn.commit()


# Insert spell rolls into the database
def insert_spell_rolls(conn, spell_rolls):
    # Fetch all trait abbreviations and their corresponding IDs into a dictionary
    trait_lookup = {}
    with conn.cursor() as cur:
        cur.execute("SELECT trait_abbreviation, id FROM dsa5.traits;")
        rows = cur.fetchall()
        trait_lookup = {row[0]: row[1] for row in rows}  # {trait_abbreviation: trait_id}

    query = """
    INSERT INTO dsa5.spell_rolls
    (event_id, character_id, timestamp, spell_name, spell_value, spell_trait_1_id, spell_trait_2_id, spell_trait_3_id,
     modifier, result, quality_step, success_level, description)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (event_id) DO NOTHING;
    """

    check_character_query = "SELECT EXISTS(SELECT 1 FROM dsa5.characters WHERE id = %s);"

    with conn.cursor() as cur:
        for spell in spell_rolls:
            # Check if the character exists
            cur.execute(check_character_query, (spell["character_id"],))
            exists = cur.fetchone()[0]

            if not exists:
                print(f"Skipping spell roll {spell['event_id']} - Character {spell['character_id']} not found.")
                continue  # Skip insertion for missing characters

            # Fetch trait IDs from the lookup dictionary (default to None if not found)
            trait_1_id = trait_lookup.get(spell.get("talent_trait_1"))
            trait_2_id = trait_lookup.get(spell.get("talent_trait_2"))
            trait_3_id = trait_lookup.get(spell.get("talent_trait_3"))

            # Insert the spell roll data
            cur.execute(
                query,
                (
                    spell["event_id"],
                    spell["character_id"],
                    spell["timestamp"],
                    spell["talent_name"],
                    spell["talent_value"],
                    trait_1_id,
                    trait_2_id,
                    trait_3_id,
                    spell["modifier"],
                    spell["result"],
                    spell["quality_step"],
                    spell["success_level"],
                    spell["description"],
                ),
            )
    conn.commit()


# Insert attack rolls into the database
def insert_attack_rolls(conn, attack_rolls):

    query = """
    INSERT INTO dsa5.attack_rolls
    (event_id, character_id, timestamp, attack_name, attack_type, attack_value, modifier, roll_result,
     damage, description)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (event_id) DO NOTHING;
    """

    check_character_query = "SELECT EXISTS(SELECT 1 FROM dsa5.characters WHERE id = %s);"

    with conn.cursor() as cur:
        for attack in attack_rolls:
            # Check if the character exists
            cur.execute(check_character_query, (attack["character_id"],))
            exists = cur.fetchone()[0]

            if not exists:
                print(f"Skipping attack roll {attack['event_id']} - Character {attack['character_id']} not found.")
                continue  # Skip insertion for missing characters

            # Insert the attack roll data
            cur.execute(
                query,
                (
                    attack["event_id"],
                    attack["character_id"],
                    attack["timestamp"],
                    attack["attack_name"],
                    attack["attack_type"],
                    attack["attack_value"],
                    attack["modifier"],
                    attack["roll_result"],
                    attack["damage"],
                    attack["description"],
                ),
            )
    conn.commit()


# Insert parry rolls into the database
def insert_parry_rolls(conn, parry_rolls):
    query = """
    INSERT INTO dsa5.parry_rolls
    (event_id, character_id, timestamp, parry_name, parry_type, parry_value, modifier, roll_result, description)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (event_id) DO NOTHING;
    """

    check_character_query = "SELECT EXISTS(SELECT 1 FROM dsa5.characters WHERE id = %s);"

    with conn.cursor() as cur:
        for parry in parry_rolls:
            # Check if the character exists
            cur.execute(check_character_query, (parry["character_id"],))
            exists = cur.fetchone()[0]

            if not exists:
                print(f"Skipping parry roll {parry['event_id']} - Character {parry['character_id']} not found.")
                continue  # Skip insertion for missing characters

            # Insert the parry roll data
            cur.execute(
                query,
                (
                    parry["event_id"],
                    parry["character_id"],
                    parry["timestamp"],
                    parry["parry_name"],
                    parry["parry_type"],
                    parry["parry_value"],
                    parry["modifier"],
                    parry["roll_result"],
                    parry["description"],
                ),
            )
    conn.commit()


# Insert dodge rolls into the database
def insert_dodge_rolls(conn, dodge_rolls):
    query = """
    INSERT INTO dsa5.dodge_rolls
    (event_id, character_id, timestamp, dodge_value, modifier, roll_result, description)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (event_id) DO NOTHING;
    """

    check_character_query = "SELECT EXISTS(SELECT 1 FROM dsa5.characters WHERE id = %s);"

    with conn.cursor() as cur:
        for dodge in dodge_rolls:
            # Check if the character exists
            cur.execute(check_character_query, (dodge["character_id"],))
            exists = cur.fetchone()[0]

            if not exists:
                print(f"Skipping dodge roll {dodge['event_id']} - Character {dodge['character_id']} not found.")
                continue  # Skip insertion for missing characters

            # Insert the dodge roll data
            cur.execute(
                query,
                (
                    dodge["event_id"],
                    dodge["character_id"],
                    dodge["timestamp"],
                    dodge["dodge_value"],
                    dodge["modifier"],
                    dodge["roll_result"],
                    dodge["description"],
                ),
            )
    conn.commit()


def insert_data(conn, characters, trait_rolls, talent_rolls, spells, attacks, parry_rolls, dodge_rolls):
    if not characters:
        print("No characters found. Skipping character insertion.")
    else:
        print("Inserting characters into DSA5 schema...")
        insert_characters(conn, characters)

    if not trait_rolls:
        print("No trait rolls found. Skipping trait roll insertion.")
    else:
        print("Inserting trait rolls into DSA5 schema...")
        insert_trait_rolls(conn, trait_rolls)

    if not talent_rolls:
        print("No talent rolls found. Skipping talent roll insertion.")
    else:
        print("Inserting talent rolls into DSA5 schema...")
        insert_talent_rolls(conn, talent_rolls)

    if not spells:
        print("No spells found. Skipping spell insertion.")
    else:
        print("Inserting spells into DSA5 schema...")
        insert_spell_rolls(conn, spells)

    if not attacks:
        print("No attacks found. Skipping attack insertion.")
    else:
        print("Inserting attacks into DSA5 schema...")
        insert_attack_rolls(conn, attacks)

    if not parry_rolls:
        print("No parry rolls found. Skipping parry roll insertion.")
    else:
        print("Inserting parry rolls into DSA5 schema...")
        insert_parry_rolls(conn, parry_rolls)

    if not dodge_rolls:
        print("No dodge rolls found. Skipping dodge roll insertion.")
    else:
        print("Inserting dodge rolls into DSA5 schema...")
        insert_dodge_rolls(conn, dodge_rolls)

    print("✅ Data insertion complete.")


def main():
    """
    Function to load JSON data from files and insert it into the DSA5 database schema.
    """
    conn = connect_db()
    try:
        # Load character and talent data
        characters = load_json_data(CHARACTERS_FILE)
        trait_rolls = load_json_data(TRAITS_FILE)
        talent_rolls = load_json_data(TALENTS_FILE)
        spells = load_json_data(SPELLS_FILE)
        attacks = load_json_data(ATTACKS_FILE)
        parry_rolls = load_json_data(PARRY_FILE)
        dodge_rolls = load_json_data(DODGE_FILE)

        # Insert data into the database
        insert_data(conn, characters, trait_rolls, talent_rolls, spells, attacks, parry_rolls, dodge_rolls)

    except Exception as e:
        print(f"❌ Error during data insertion: {e}")
        conn.rollback()

    finally:
        conn.close()


if __name__ == "__main__":
    main()
