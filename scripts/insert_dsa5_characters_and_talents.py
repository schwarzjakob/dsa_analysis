#!/usr/bin/env python3
import os
import json
import psycopg2

# Set file paths for JSON data
CHARACTERS_FILE = "integrations/_temp/mvp_character_actors.json"
TALENTS_FILE = "integrations/_temp/mvp_talent_messages.json"


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
    INSERT INTO dsa5.actors
    (id, name, type, mut, klugheit, intuition, charisma, fingerfertigkeit, gewandtheit, konstitution, köperkraft,
     life_points_value, life_points_max, astral_energy_value, astral_energy_max, initiative, species, culture, career,
     experience_total, experience_spent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """
    with conn.cursor() as cur:
        for char in characters:
            cur.execute(
                query,
                (
                    char["id"],
                    char["name"],
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


# Insert talent rolls into the database
def insert_talent_rolls(conn, talent_rolls):
    query = """
    INSERT INTO dsa5.talent_rolls 
    (message_id, timestamp, talent_name, talent_group, talent_value, talent_trait_1, talent_trait_2, talent_trait_3,
     modifier, actor, result, quality_step, description, success_level, roll_type)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (message_id) DO NOTHING;
    """

    check_actor_query = "SELECT EXISTS(SELECT 1 FROM dsa5.actors WHERE id = %s);"

    with conn.cursor() as cur:
        for talent in talent_rolls:
            cur.execute(check_actor_query, (talent["actor"],))
            exists = cur.fetchone()[0]

            if not exists:
                print(f"Skipping talent roll {talent['message_id']} - Actor {talent['actor']} not found.")
                continue  # Skip insertion for missing actors

            cur.execute(
                query,
                (
                    talent["message_id"],
                    talent["timestamp"],
                    talent["talent_name"],
                    talent["talent_group"],
                    talent["talent_value"],
                    talent["talent_trait_1"],
                    talent["talent_trait_2"],
                    talent["talent_trait_3"],
                    talent["modifier"],
                    talent["actor"],
                    talent["result"],
                    talent["quality_step"],
                    talent["description"],
                    talent["success_level"],
                    talent["roll_type"],
                ),
            )
    conn.commit()


# Main function to load JSON and insert data
def main():
    conn = connect_db()
    try:
        # Load character and talent data
        characters = load_json_data(CHARACTERS_FILE)
        talent_rolls = load_json_data(TALENTS_FILE)

        # Print first line of each data set
        print(f"Characters: {characters[0]}")
        print(f"Talent Rolls: {talent_rolls[0]}")

        if not characters:
            print("No characters found. Skipping character insertion.")
        else:
            print("Inserting characters into DSA5 schema...")
            insert_characters(conn, characters)

        if not talent_rolls:
            print("No talent rolls found. Skipping talent roll insertion.")
        else:
            print("Inserting talent rolls into DSA5 schema...")
            insert_talent_rolls(conn, talent_rolls)

        print("✅ Data insertion complete.")

    except Exception as e:
        print(f"❌ Error during data insertion: {e}")
        conn.rollback()

    finally:
        conn.close()


if __name__ == "__main__":
    main()
