from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import logging
from dotenv import load_dotenv

from services.database_service import DatabaseService
from services.chat_log_processing_service import ChatLogProcessingService
from services import exploratory_analysis


# TODO: Remove traits_values_output (also from frontend) as its not used at all.
# TODO: Implement data models such as Character, BaseEvent, Talent, Spell, Attack, etc.


# Enabling logging
logger_format = "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)d] %(levelname)s: %(message)s"
logging.basicConfig(format=logger_format, level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

# Setup base directory if needed
base_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(base_dir)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Instantiate the database service once, use globally
database_service = DatabaseService()

# -------------------------------------------------------------------
# Chat processing
# -------------------------------------------------------------------


@app.route("/chat_processing/process_chatlog", methods=["POST"])
def process_chatlog_route():
    logger.debug("process_chatlog_route called")
    try:
        if "file" not in request.files:
            return "No file part", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400

        # 1) Read the uploaded file into memory
        chatlog_lines = file.read().decode("utf-8").splitlines()

        # 2) Fetch all relevant game data
        characters_and_aliases = database_service.get_characters_and_aliases()
        known_talents = database_service.get_talents()
        known_spells = database_service.get_spells()
        known_attacks = database_service.get_attacks()

        # 3) Pass them into the chat processor
        chat_processor = ChatLogProcessingService(characters_and_aliases, known_talents, known_spells, known_attacks)
        dice_events = chat_processor.process_chat_log(chatlog_lines)

        # 4) Use DatabaseService to insert events
        database_service.insert_traits_rolls(dice_events["traits"])
        database_service.insert_talents_rolls(dice_events["talents"])
        database_service.insert_spells_rolls(dice_events["spells"])
        database_service.insert_attacks_rolls(dice_events["attacks"])
        database_service.insert_initiatives(dice_events["initiatives"])
        database_service.insert_total_damage(dice_events["total_damage"])

        logger.debug("Chat log processed and events inserted.")
        return "Chat log processed and events inserted.", 200

    except Exception as e:
        logger.error(e)
        return f"Error: {e}", 500


# -------------------------------------------------------------------
# Characters management
# -------------------------------------------------------------------


@app.route("/characters_management/characters", methods=["GET"])
def get_characters():
    """
    Returns a list of all characters.
    """
    try:
        character_data = database_service.get_characters()
        return jsonify({"characters": character_data}), 200

    except Exception as e:
        logger.error(f"Error getting characters: {e}")
        return jsonify({"error": "Error getting characters"}), 500


@app.route("/characters_management/update-character", methods=["POST"])
def update_character():
    """
    Update a character's attributes & aliases.
    """
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

        success = database_service.update_character(character_name, attributes, aliases)
        if not success:
            return jsonify({"error": "Failed to update character"}), 500

        return jsonify({"message": "Character updated successfully"}), 200

    except Exception as e:
        logger.error(f"Error updating character: {e}")
        return jsonify({"error": "An error occurred"}), 500


@app.route("/characters_management/add-character", methods=["POST"])
def add_character():
    """
    Add a new character to the database.
    """
    # TODO: Implement


# -------------------------------------------------------------------
# Character analysis: Talents
# -------------------------------------------------------------------


@app.route("/character_analysis/talents/<character_name>", methods=["GET"])
def get_talents(character_name):
    """
    Fetch aggregated talents data for a specific character.
    """
    try:
        # 1) Get character_id
        character_id = database_service.get_character_id_by_name(character_name)
        if character_id is None:
            return jsonify({"error": f"Character '{character_name}' not found"}), 404

        # 2) Fetch talents
        talents_output = database_service.fetch_talents_for_character(character_id) or []

        # Convert to list of lists
        talents_result = [
            (
                row["talent"],
                int(row["talent_count"]),
                float(row["success_rate"]),
                float(row["failure_rate"]),
                float(row["avg_score"]),
                float(row["std_dev"]),
            )
            for row in talents_output
        ]

        # 3) Fetch traits values and usage
        traits_values_output = database_service.fetch_traits_values_for_character(character_id) or []

        # Initialize a dictionary to hold trait averages
        traits_dict = {row["trait"]: float(row["avg_value"]) for row in traits_values_output}

        # Assuming we have exactly three traits: Trait 1, Trait 2, Trait 3
        # Pad with 0 if any trait is missing
        traits_values = [
            ("Trait 1", traits_dict.get("Trait 1", 0.0)),
            ("Trait 2", traits_dict.get("Trait 2", 0.0)),
            ("Trait 3", traits_dict.get("Trait 3", 0.0)),
        ]

        # 4) Fetch traits_relative and categories_relative
        traits_relative_output = database_service.fetch_traits_relative_for_character(character_id) or []
        traits_relative = [(row["trait"], row["trait_count"]) for row in traits_relative_output]

        categories_relative_output = database_service.fetch_categories_for_character(character_id) or []
        categories_relative = [(row["category"], row["category_count"]) for row in categories_relative_output]

        # Format response to match frontend expectations
        data = {
            "talents": talents_result if talents_result else [],
            "traits_relative": traits_relative if traits_relative else [],
            "traits_values": traits_values if traits_values else [],
            "categories_relative": categories_relative if categories_relative else [],
        }

        return jsonify(data), 200

    except Exception as error:
        logger.error(f"Error getting talents for {character_name}: {error}")
        return jsonify({"talents": [], "traits_relative": [], "traits_values": [], "categories_relative": []}), 500


@app.route("/character_analysis/analyze-talent", methods=["POST"])
def analyze_talent():
    """
    Detailed analysis of a single talent for a character.
    """
    data = request.json
    character_name = data.get("characterName")
    talent_name = data.get("talentName")

    try:
        character_id = database_service.get_character_id_by_name(character_name)
        if character_id is None:
            return jsonify({"error": f"Character '{character_name}' not found"}), 404

        # Fetch summary stats
        talent_stats = database_service.fetch_talent_statistics(character_id, talent_name)
        if not talent_stats:
            return jsonify({"talent_statistics": {}, "talent_line_chart": {}, "talent_investment_recommendation": ""})

        row = talent_stats[0]
        attempts = int(row["attempts"]) if row["attempts"] else 0
        success_rate = float(row["success_rate"]) if row["success_rate"] else 0.0
        avg_score = float(row["avg_score"]) if row["avg_score"] else 0.0
        std_dev = float(row["std_dev"]) if row["std_dev"] else 0.0

        # Simple recommendation
        recommendation = "Consider investing more" if success_rate < 0.5 else "Well trained"

        # Fetch line chart data
        line_chart_data = database_service.fetch_talent_line_chart(character_id, talent_name) or []
        timestamps = [int(r["sequence"]) for r in line_chart_data]
        scores = [float(r["tap_zfp"]) for r in line_chart_data]

        logger.info(line_chart_data)

        data = {
            "talent_statistics": {
                "attempts": attempts,
                "success_rate": success_rate,
                "avg_score": avg_score,
                "std_dev": std_dev,
            },
            "talent_line_chart": {
                "timestamps": timestamps,
                "scores": scores,
            },
            "talent_investment_recommendation": recommendation,
        }
        return jsonify(data), 200

    except Exception as error:
        logger.error(f"Error analyzing talent for {character_name}: {error}")
        return jsonify({"error": str(error)}), 500


# -------------------------------------------------------------------
# Character analysis: Attacks
# -------------------------------------------------------------------


@app.route("/character_analysis/attacks/<character_name>", methods=["GET"])
def get_attacks(character_name):
    """
    Fetch aggregated attack data for a specific character.
    """
    try:
        # 1) Get character_id
        character_id = database_service.get_character_id_by_name(character_name)
        if character_id is None:
            return jsonify({"error": f"Character '{character_name}' not found"}), 404

        # 2) Fetch attacks
        attacks_output = database_service.fetch_attacks_for_character(character_id) or []

        # Ensure result is a list of tuples (not dictionaries)
        attacks_result = [
            (
                row["attack"],
                int(row["attack_count"]),
                row["success_rate"],
                row["failure_rate"],
                row["avg_score"],
                row["std_dev"],
            )
            for row in attacks_output
        ]

        # Format response to match previous behavior
        data = {"attacks": attacks_result}

        return jsonify(data), 200

    except Exception as error:
        logger.error(f"Error getting attacks for {character_name}: {error}")
        return jsonify({"attacks": []}), 500


@app.route("/character_analysis/analyze-attack", methods=["POST"])
def analyze_attack():
    """
    Detailed analysis of a single attack for a character.
    """
    data = request.json
    character_name = data.get("characterName")
    attack_name = data.get("attackName")

    try:
        character_id = database_service.get_character_id_by_name(character_name)
        if character_id is None:
            return jsonify({"error": f"Character '{character_name}' not found"}), 404

        # Fetch summary stats
        attack_stats = database_service.fetch_attack_statistics(character_id, attack_name) or []
        if not attack_stats:
            return jsonify({"attack_statistics": {}, "attack_line_chart": {}}), 200

        row = attack_stats[0]
        attempts = int(row["attempts"]) if row["attempts"] else 0
        success_rate = float(row["success_rate"]) if row["success_rate"] else 0.0
        avg_score = float(row["avg_score"]) if row["avg_score"] else 0.0
        std_dev = float(row["std_dev"]) if row["std_dev"] else 0.0

        # Fetch line chart
        line_chart_data = database_service.fetch_attack_line_chart(character_id, attack_name) or []
        timestamps = [int(r["sequence"]) for r in line_chart_data]
        scores = [float(r["tap_zfp"]) for r in line_chart_data]

        data = {
            "attack_statistics": {
                "attempts": attempts,
                "success_rate": success_rate,
                "avg_score": avg_score,
                "std_dev": std_dev,
            },
            "attack_line_chart": {
                "timestamps": timestamps,
                "scores": scores,
            },
        }
        return jsonify(data), 200

    except Exception as error:
        logger.error(f"Error analyzing attack for {character_name}: {error}")
        return jsonify({"error": str(error)}), 500


# -------------------------------------------------------------------
# Data exploration
# -------------------------------------------------------------------


@app.route("/traits-for-selected-talents", methods=["POST"])
def get_traits_for_selected_talents():
    """
    Example endpoint to fetch traits for a list of talent names.
    """
    data = request.json
    talents_name_list = data.get("talentsNameList", [])

    if not talents_name_list:
        return jsonify({"error": "No talents provided"}), 400

    try:
        fetched_talents = database_service.fetch_traits_for_talents(talents_name_list) or []
        # Flatten
        traits_list = [trait for row in fetched_talents for trait in row]
        # Use your existing function for counting
        trait_counts = exploratory_analysis.get_trait_counts(traits_list)
        return jsonify(trait_counts), 200

    except Exception as e:
        logger.error(f"Error fetching traits for talents: {e}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/talents-options", methods=["GET"])
def get_talents_options():
    """
    Return all talents grouped by category.
    """
    try:
        talents_data = database_service.fetch_talents_and_categories() or []
        talents_by_category = {}
        for row in talents_data:
            talent_name = row["talent_name"]
            category_name = row["talent_category_name"]
            if category_name not in talents_by_category:
                talents_by_category[category_name] = []
            talents_by_category[category_name].append(talent_name)

        return jsonify({"talents": talents_by_category}), 200

    except Exception as error:
        logger.error(f"Error fetching talents options: {error}")
        return jsonify({"talents": {}}), 500


if __name__ == "__main__":
    # Run the Flask application
    app.run(debug=True)
