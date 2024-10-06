from flask import Flask, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import os
import sys
import json
import logging
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import execute_values
from sqlalchemy import create_engine
from dsa_analysis_app.auth.google_auth import google_authorization
from dsa_analysis_app.chat_processing.chat_log_parser import DsaStats
from dsa_analysis_app.character_analysis import character_analysis
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
        talents_output = character_analysis.get_character_talents(character_name)
        logger.debug(f"Getting talents of: {character_name}")
        traits_values_output = character_analysis.get_character_traits_values(character_name)
        logger.debug(f"Getting traits values of: {character_name}")
        traits_relative_output = character_analysis.get_character_relative_traits_usage(character_name)
        logger.debug(f"Getting traits distribution usage of: {character_name}")
        categories_relative_output = character_analysis.get_character_relative_talents_categories_usage(character_name)
        logger.debug(f"Getting categories distribution usage of: {character_name}")
    except Exception as error:
        logger.error(f"Error getting values for {character_name}: {error}")
        # Initialize with default values in case of error
        talents_output = []
        traits_values_output = []
        traits_relative_output = []
        categories_relative_output = []

    data = {
        "talents": talents_output,
        "traits_relative": traits_relative_output,
        "traits_values": traits_values_output,
        "categories_relative": categories_relative_output,
    }
    return jsonify(data)


@app.route("/character_analysis/analyze-talent", methods=["POST"])
def analyze_talent():
    data = request.json
    character_name = data.get("characterName")
    talent_name = data.get("talentName")

    try:
        talent_statistics = character_analysis.get_character_talent_statistics(character_name, talent_name)
        logger.debug(f"Talent Statistics of:  {character_name}, {talent_name}")
        talent_line_chart_output = character_analysis.get_character_talent_line_chart(character_name, talent_name)
        logger.debug(f"Talent Line Chart of:  {character_name}, {talent_name}")
        talent_investment_recommendation = character_analysis.get_character_talent_investment_recommendation(
            talent_statistics
        )
        logger.debug(f"Talent Investment Recommendation of:  {character_name}, {talent_name}")

    except Exception as error:
        logger.error(f"Error getting values for {character_name}: {error}")

    data = {
        "talent_statistics": talent_statistics,
        "talent_line_chart": talent_line_chart_output,
        "talent_investment_recommendation": talent_investment_recommendation,
    }

    return jsonify(data)


@app.route("/character_analysis/attacks/<character_name>", methods=["GET"])
def get_attacks(character_name):
    attacks_output = {}  # Initialize attacks_output with an empty dictionary
    try:
        attacks_output = character_analysis.get_character_attacks(character_name)
        logger.debug(f"Getting attacks of:  {character_name}")
    except Exception as error:
        logger.error(f"Error getting values for {character_name}: {error}")
        # attacks_output will remain an empty dictionary in case of an error

    data = {"attacks": attacks_output}

    return jsonify(data)


@app.route("/character_analysis/analyze-attack", methods=["POST"])
def analyze_attack():
    data = request.json
    character_name = data.get("characterName")
    attack_name = data.get("attackName")

    try:
        attack_statistics = character_analysis.get_character_attack_statistics(character_name, attack_name)
        logger.debug(f"Attack Statistics of:  {character_name}, {attack_name}")
        attack_line_chart_output = character_analysis.get_character_attack_line_chart(character_name, attack_name)
        logger.debug(f"Attack Line Chart of:  {character_name}, {attack_name}")

    except Exception as error:
        logger.error(f"Error getting values for {character_name}: {error}")

    data = {
        "attack_statistics": attack_statistics,
        "attack_line_chart": attack_line_chart_output,
    }

    return jsonify(data)


# Characters management
@app.route("/characters_management/characters", methods=["GET"])
def get_characters():
    try:
        characters_file_path = os.path.join(base_dir, "dsa_analysis_app", "data", "json", "characters.json")
        with open(characters_file_path) as file:
            characters_data = json.load(file)
        return characters_data
    except FileNotFoundError:
        return "File not found", 404
    except Exception as e:
        logger.error(f"Error getting characters: {e}")
        return "Error getting characters", 500


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
