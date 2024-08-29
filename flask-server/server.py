from flask import Flask, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import os
import sys
import json
import logging
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine
from dsa_analysis_app.auth.google_auth import google_authorization
from dsa_analysis_app.chat_processing.chat_log_parser import DsaStats
from dsa_analysis_app.traits_needed_for_some_talents import traits_needed_for_some_talents

# Enabling logging (must come first to enable it globally, also for imported modules and packages)
logger_format = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)d] %(levelname)s: %(message)s"
logging.basicConfig(format=logger_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

# Automatically determine the base directory and add it to sys.path
base_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(base_dir, "dsa_analysis_app"))

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# Database connection setup
DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


app.secret_key = os.getenv("GOOGLE_CLIENT_SECRET")
google_authorization(app)


# Authorization for the Google API
@app.route("/auth/login")
def login():
    google = app.config.get("google")
    logger.debug(f"Google: {google}")
    return google.authorize_redirect(redirect_uri=url_for("authorize", _external=True))


@app.route("/auth/login/authorize")
def authorize():
    google = app.config.get("google")
    logger.debug(f"Google: {google}")
    google.authorize_access_token()
    user_info = google.get("https://www.googleapis.com/oauth2/v1/userinfo").json()
    session["user"] = user_info
    logger.debug(f"User info: {user_info}")
    return redirect("http://127.0.0.1:3000/start")  # Redirect to the start page


# Chatlog parsing
UPLOAD_FOLDER = os.path.join(base_dir, "uploads")


@app.route("/chat_processing/process_chatlog", methods=["POST"])
def process_chatlog_route():
    logger.debug("process_chatlog_route called")
    try:
        if "file" not in request.files:
            return "No file part", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        if file:
            filename = "chatlog.txt"

            # Make sure the uploads folder exists
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            # Save the file to the uploads folder
            chatlog_file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(chatlog_file_path)

            # Establish database connection and SQLAlchemy engine
            conn = get_db_connection()
            engine = create_engine(DATABASE_URL)  # Create SQLAlchemy engine

            # Pass the connection and engine to DsaStats
            current_dsa_stats = DsaStats(conn, engine)
            chatlogLines = current_dsa_stats.process_chatlog(chatlog_file_path)
            current_dsa_stats.main(chatlogLines)

            logger.debug(f"File uploaded successfully to {chatlog_file_path}")
            return f"File uploaded successfully to {chatlog_file_path}", 200

    except Exception as e:
        logger.error(e)
        return f"Error: {e}", 500


# Character analysis
@app.route("/character_analysis/talents/<character_name>", methods=["GET"])
def get_talents(character_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch character_id
        cursor.execute("SELECT id FROM characters WHERE name = %s", (character_name,))
        character_id = cursor.fetchone()[0]

        # Fetch talents
        cursor.execute(
            """
            SELECT talent, COUNT(*) AS talent_count,
                   COALESCE(AVG(success::int), 0) AS success_rate,
                   COALESCE(1 - AVG(success::int), 0) AS failure_rate,
                   COALESCE(AVG(tap_zfp), 0) AS avg_score,
                   COALESCE(STDDEV(tap_zfp), 0) AS std_dev
            FROM talents_rolls
            WHERE character_id = %s
            GROUP BY talent
        """,
            (character_id,),
        )
        talents_output = cursor.fetchall()

        # Convert Decimal to float, handling None values
        talents_output = [
            (
                talent,
                count,
                float(success_rate) if success_rate is not None else 0.0,
                float(failure_rate) if failure_rate is not None else 0.0,
                float(avg_score) if avg_score is not None else 0.0,
                float(std_dev) if std_dev is not None else 0.0,
            )
            for talent, count, success_rate, failure_rate, avg_score, std_dev in talents_output
        ]

        # Fetch traits values and usage
        cursor.execute(
            """
            SELECT 'Trait 1' AS trait, COALESCE(AVG(trait_value1), 0) AS avg_value FROM talents_rolls WHERE character_id = %s
            UNION ALL
            SELECT 'Trait 2' AS trait, COALESCE(AVG(trait_value2), 0) AS avg_value FROM talents_rolls WHERE character_id = %s
            UNION ALL
            SELECT 'Trait 3' AS trait, COALESCE(AVG(trait_value3), 0) AS avg_value FROM talents_rolls WHERE character_id = %s
        """,
            (character_id, character_id, character_id),
        )
        traits_values_output = cursor.fetchall()

        # Convert Decimal to float, handling None values
        traits_values_output = [
            (trait, float(avg_value) if avg_value is not None else 0.0) for trait, avg_value in traits_values_output
        ]

        cursor.execute(
            """
            SELECT trait, COUNT(*) AS trait_count
            FROM (
                SELECT trait1 AS trait FROM talents_rolls WHERE character_id = %s
                UNION ALL
                SELECT trait2 AS trait FROM talents_rolls WHERE character_id = %s
                UNION ALL
                SELECT trait3 AS trait FROM talents_rolls WHERE character_id = %s
            ) AS combined_traits
            GROUP BY trait
        """,
            (character_id, character_id, character_id),
        )
        traits_relative_output = cursor.fetchall()

        # Fetch categories usage
        cursor.execute(
            """
            SELECT category, COUNT(*) AS category_count
            FROM talents_rolls
            WHERE character_id = %s
            GROUP BY category
        """,
            (character_id,),
        )
        categories_relative_output = cursor.fetchall()

        cursor.close()
        conn.close()

        data = {
            "talents": talents_output,
            "traits_relative": traits_relative_output,
            "traits_values": traits_values_output,
            "categories_relative": categories_relative_output,
        }

        print(data)  # Keep for debugging

        return jsonify(data)

    except Exception as error:
        logger.error(f"Error getting values for {character_name}: {error}")
        return jsonify({"talents": [], "traits_relative": [], "traits_values": [], "categories_relative": []})


# Character analysis
@app.route("/character_analysis/analyze-talent", methods=["POST"])
def analyze_talent():
    data = request.json
    character_name = data.get("characterName")
    talent_name = data.get("talentName")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM characters WHERE name = %s", (character_name,))
        character_id = cursor.fetchone()[0]

        # Fetch talent statistics
        cursor.execute(
            """
            SELECT COUNT(*) AS attempts,
                   AVG(success::int) AS success_rate,
                   AVG(tap_zfp) AS avg_score,
                   STDDEV(tap_zfp) AS std_dev
            FROM talents_rolls
            WHERE character_id = %s AND talent = %s
        """,
            (character_id, talent_name),
        )
        talent_statistics = cursor.fetchone()

        # Fetch line chart data - Use id instead of created_at
        cursor.execute(
            """
            SELECT id AS sequence, tap_zfp
            FROM talents_rolls
            WHERE character_id = %s AND talent = %s
            ORDER BY id
        """,
            (character_id, talent_name),
        )
        talent_line_chart_output = cursor.fetchall()

        # Simple recommendation logic based on success rate and average score
        talent_investment_recommendation = "Consider investing more" if talent_statistics[1] < 0.5 else "Well trained"

        cursor.close()
        conn.close()

        data = {
            "talent_statistics": {
                "attempts": talent_statistics[0],
                "success_rate": talent_statistics[1],
                "avg_score": talent_statistics[2],
                "std_dev": talent_statistics[3],
            },
            "talent_line_chart": {
                "timestamps": [row[0] for row in talent_line_chart_output],
                "scores": [row[1] for row in talent_line_chart_output],
            },
            "talent_investment_recommendation": talent_investment_recommendation,
        }
        return jsonify(data)

    except Exception as error:
        logger.error(f"Error getting values for {character_name}: {error}")
        return jsonify({"talent_statistics": {}, "talent_line_chart": {}, "talent_investment_recommendation": ""})


@app.route("/character_analysis/attacks/<character_name>", methods=["GET"])
def get_attacks(character_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch character_id
        cursor.execute("SELECT id FROM characters WHERE name = %s", (character_name,))
        character_id = cursor.fetchone()[0]

        # Fetch attacks
        cursor.execute(
            """
            SELECT attack, COUNT(*) AS attack_count,
                   AVG(success::int) AS success_rate,
                   1 - AVG(success::int) AS failure_rate,
                   AVG(tap_zfp) AS avg_score,
                   STDDEV(tap_zfp) AS std_dev
            FROM attacks_rolls
            WHERE character_id = %s
            GROUP BY attack
        """,
            (character_id,),
        )
        attacks_output = cursor.fetchall()

        cursor.close()
        conn.close()

        data = {"attacks": attacks_output}
        return jsonify(data)

    except Exception as error:
        logger.error(f"Error getting attacks for {character_name}: {error}")
        return jsonify({"attacks": []}), 404


@app.route("/character_analysis/analyze-attack", methods=["POST"])
def analyze_attack():
    data = request.json
    character_name = data.get("characterName")
    attack_name = data.get("attackName")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM characters WHERE name = %s", (character_name,))
        character_id = cursor.fetchone()[0]

        # Fetch attack statistics
        cursor.execute(
            """
            SELECT COUNT(*) AS attempts,
                   AVG(success::int) AS success_rate,
                   AVG(tap_zfp) AS avg_score,
                   STDDEV(tap_zfp) AS std_dev
            FROM attacks_rolls
            WHERE character_id = %s AND attack = %s
        """,
            (character_id, attack_name),
        )
        attack_statistics = cursor.fetchone()

        # Fetch line chart data - Use id instead of created_at
        cursor.execute(
            """
            SELECT id AS sequence, tap_zfp
            FROM attacks_rolls
            WHERE character_id = %s AND attack = %s
            ORDER BY id
        """,
            (character_id, attack_name),
        )
        attack_line_chart_output = cursor.fetchall()

        cursor.close()
        conn.close()

        data = {
            "attack_statistics": {
                "attempts": attack_statistics[0],
                "success_rate": attack_statistics[1],
                "avg_score": attack_statistics[2],
                "std_dev": attack_statistics[3],
            },
            "attack_line_chart": {
                "timestamps": [row[0] for row in attack_line_chart_output],
                "scores": [row[1] for row in attack_line_chart_output],
            },
        }
        return jsonify(data)

    except Exception as error:
        logger.error(f"Error getting values for {character_name}: {error}")
        return jsonify({"attack_statistics": {}, "attack_line_chart": {}})


# Characters management
# Characters management
@app.route("/characters_management/characters", methods=["GET"])
def get_characters():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch character details along with their traits and aliases
        cursor.execute(
            """
            SELECT id, name, mut, klugheit, intuition, charisma, fingerfertigkeit, gewandtheit, konstitution, körperkraft, alias
            FROM characters
        """
        )
        characters = cursor.fetchall()

        # Structure the data
        character_data = []
        for char in characters:
            char_dict = {
                "id": char[0],
                "name": char[1],
                "traits": {
                    "Mut": char[2],
                    "Klugheit": char[3],
                    "Intuition": char[4],
                    "Charisma": char[5],
                    "Fingerfertigkeit": char[6],
                    "Gewandtheit": char[7],
                    "Konstitution": char[8],
                    "Körperkraft": char[9],
                },
                "alias": char[10] if char[10] is not None else [],  # Assuming alias is stored as a list or array
            }
            character_data.append(char_dict)

        return jsonify({"characters": character_data})

    except Exception as e:
        logger.error(f"Error getting characters: {e}")
        return "Error getting characters", 500
    finally:
        cursor.close()
        conn.close()


# Endpoint to update character attributes and aliases
@app.route("/characters_management/update-character", methods=["POST"])
def update_character():
    try:
        data = request.json
        character_name = data.get("name")
        attributes = {
            "Mut": data.get("Mut"),
            "Klugheit": data.get("Klugheit"),
            "Intuition": data.get("Intuition"),
            "Charisma": data.get("Charisma"),
            "Fingerfertigkeit": data.get("Fingerfertigkeit"),
            "Gewandtheit": data.get("Gewandtheit"),
            "Konstitution": data.get("Konstitution"),
            "Körperkraft": data.get("Körperkraft"),
        }
        aliases = data.get("alias", [])

        conn = get_db_connection()
        cursor = conn.cursor()

        # Update the character's attributes and aliases
        cursor.execute(
            """
            UPDATE characters
            SET mut = %s, klugheit = %s, intuition = %s, charisma = %s,
                fingerfertigkeit = %s, gewandtheit = %s, konstitution = %s, körperkraft = %s,
                alias = %s
            WHERE name = %s
            """,
            (
                attributes["Mut"],
                attributes["Klugheit"],
                attributes["Intuition"],
                attributes["Charisma"],
                attributes["Fingerfertigkeit"],
                attributes["Gewandtheit"],
                attributes["Konstitution"],
                attributes["Körperkraft"],
                aliases,  # Ensure that aliases are also updated
                character_name,
            ),
        )
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Character updated successfully"}), 200
    except Exception as e:
        logger.error(f"Error updating character {character_name}: {e}")
        return jsonify({"error": "An error occurred"}), 500


@app.route("/characters_management/archive-character", methods=["POST"])
def archive_character():
    try:
        character_data = request.json
        characters_file_path = os.path.join(base_dir, "dsa_analysis_app", "data", "json", "characters.json")
        archived_file_path = os.path.join(base_dir, "dsa_analysis_app", "data", "json", "archived_characters.json")

        with open(characters_file_path, "r") as file:
            characters = json.load(file)

        # Find and remove the character to archive
        characters["characters"] = [char for char in characters["characters"] if char["name"] != character_data["name"]]

        # Update characters.json
        with open(characters_file_path, "w") as file:
            json.dump(characters, file, indent=4)

        # Load archived characters
        if not os.path.exists(archived_file_path):
            with open(archived_file_path, "w") as file:
                json.dump({"characters": []}, file)

        with open(archived_file_path, "r+") as file:
            archived_characters = json.load(file)
            archived_characters["characters"].append(character_data)

            # Update archived_characters.json
            file.seek(0)
            file.truncate()
            json.dump(archived_characters, file, indent=4)

        logger.debug(f'Character archived successfully: {character_data["name"]}')
        return jsonify({"message": "Character archived successfully"}), 200
    except Exception as e:
        logger.error(f"Error archiving character: {e}")
        return jsonify({"error": "An error occurred"}), 500


@app.route("/characters_management/add-character", methods=["POST"])
def add_character():
    try:
        character_data = request.json
        characters_file_path = os.path.join(base_dir, "dsa_analysis_app", "data", "json", "characters.json")
        with open(characters_file_path, "r+") as file:
            characters = json.load(file)
            characters["characters"].append(character_data)
            file.seek(0)
            json.dump(characters, file, indent=4)
        return jsonify({"message": "Character added successfully"}), 200
    except Exception as e:
        logger.error(f"Error adding character: {e}")
        return jsonify({"error": "An error occurred"}), 500


# Some data exploration
@app.route("/traits-for-selected-talents", methods=["POST"])
def get_traits_for_selected_talents():
    data = request.json
    talents_name_list = data.get("talentsNameList")
    traits_counts = traits_needed_for_some_talents.get_traits_for_selected_talents(talents_name_list)
    return jsonify(traits_counts)


@app.route("/talents-options", methods=["GET"])
def get_talents_options():
    talents_file_path = os.path.join(base_dir, "dsa_analysis_app", "data", "json", "talents.json")
    with open(talents_file_path, "r") as file:
        data = json.load(file)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
