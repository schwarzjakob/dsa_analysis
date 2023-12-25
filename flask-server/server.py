from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import sys
import logging

# Add the path to the directory containing dsa_analysis.py and dsa_stats.py to the system path
sys.path.append('/Users/jakobschwarz/Documents/Coding/Python/dsa_rolls_webapp/flask-server/dsa_analysis_app')

# Now you can import from dsa_analysis.py
from dsa_analysis_app import dsa_analysis
from dsa_analysis_app import dsa_stats

# New modular approach
from dsa_analysis_app import create_app

# Consider importing the constants from dsa_analysis.py
# from dsa_analysis_app.dsa_analysis import CSV_BASE_PATH, TALENTS_CSV, TRAITS_CSV, TRAIT_VALUES_CSV, ATTACKS_CSV, CHARACTER_KEY, CATEGORY_KEY, TALENT_KEY, TALENT_POINTS_KEY

# Configure logger
logger = logging.getLogger(__name__)
# Format containts the [time filename->funcName():lineno] level: message
FORMAT = '[%(asctime)s %(filename)s->%(funcName)s():%(lineno)d] %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route("/character-data/<character_name>", methods=['GET'])
def get_character_data(character_name):
    # Logic to fetch data for the given character name
    # This can be reading from a CSV file or a database query
    # Return the data in JSON format
    return f'We have to check the character. Working in Progress', 200

@app.route("/characters", methods=['GET'])
def get_characters():
    try:
        with open('./dsa_analysis_app/data/json/characters.json') as file:
            characters_data = json.load(file)
        return characters_data
    except FileNotFoundError:
        return "File not found", 404
    except Exception as e:
        logger.error(f"Error getting characters: {e}")
        return "Error getting characters", 500

# Character management routes
@app.route('/add-alias', methods=['POST'])
def add_alias():
    # Logic to add alias
    return

@app.route('/update-alias', methods=['POST'])
def update_alias():
    # Logic to update alias
    return

@app.route('/archive-character', methods=['POST'])
def archive_character():
    try:
        character_data = request.json
        # Load current characters
        with open('./dsa_analysis_app/data/json/characters.json', 'r') as file:
            characters = json.load(file)
        
        # Find and remove the character to archive
        characters["characters"] = [char for char in characters["characters"] if char["name"] != character_data["name"]]

        # Update characters.json
        with open('./dsa_analysis_app/data/json/characters.json', 'w') as file:
            json.dump(characters, file, indent=4)

        # Load archived characters
        archived_file_path = './dsa_analysis_app/data/json/archived_characters.json'
        if not os.path.exists(archived_file_path):
            with open(archived_file_path, 'w') as file:
                json.dump({"characters": []}, file)

        with open(archived_file_path, 'r+') as file:
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

@app.route('/add-character', methods=['POST'])
def add_character():
    try:
        character_data = request.json
        with open('./dsa_analysis_app/data/json/characters.json', 'r+') as file:
            characters = json.load(file)
            characters["characters"].append(character_data)
            file.seek(0)
            json.dump(characters, file, indent=4)
        return jsonify({"message": "Character added successfully"}), 200
    except Exception as e:
        logger.error(f"Error adding character: {e}")
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
