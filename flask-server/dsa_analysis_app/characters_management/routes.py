from flask import request, jsonify
from . import characters_management_blueprint
import os
import json
import logging

logger = logging.getLogger(__name__)


# Character management routes
@characters_management_blueprint.route("/characters", methods=["GET"])
def get_characters():
    try:
        with open("./dsa_analysis_app/data/json/characters.json") as file:
            characters_data = json.load(file)
        return characters_data
    except FileNotFoundError:
        return "File not found", 404
    except Exception as e:
        logger.error(f"Error getting characters: {e}")
        return "Error getting characters", 500


@characters_management_blueprint.route("/add-alias", methods=["POST"])
def add_alias():
    # Logic to add alias
    return


@characters_management_blueprint.route("/update-alias", methods=["POST"])
def update_alias():
    # Logic to update alias
    return


@characters_management_blueprint.route("/archive-character", methods=["POST"])
def archive_character():
    try:
        character_data = request.json
        # Load current characters
        with open("./dsa_analysis_app/data/json/characters.json", "r") as file:
            characters = json.load(file)

        # Find and remove the character to archive
        characters["characters"] = [
            char
            for char in characters["characters"]
            if char["name"] != character_data["name"]
        ]

        # Update characters.json
        with open("./dsa_analysis_app/data/json/characters.json", "w") as file:
            json.dump(characters, file, indent=4)

        # Load archived characters
        archived_file_path = "./dsa_analysis_app/data/json/archived_characters.json"
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


@characters_management_blueprint.route("/add-character", methods=["POST"])
def add_character():
    try:
        character_data = request.json
        with open("./dsa_analysis_app/data/json/characters.json", "r+") as file:
            characters = json.load(file)
            characters["characters"].append(character_data)
            file.seek(0)
            json.dump(characters, file, indent=4)
        return jsonify({"message": "Character added successfully"}), 200
    except Exception as e:
        logger.error(f"Error adding character: {e}")
        return jsonify({"error": "An error occurred"}), 500
