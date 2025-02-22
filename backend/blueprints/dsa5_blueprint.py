from flask import jsonify
from flask_smorest import Blueprint

from services.dsa5_database_service import Dsa5DatabaseService as DatabaseService


class Dsa5Blueprint:
    def __init__(self):
        self.blueprint = Blueprint("dsa5", "dsa5", url_prefix="/dsa5")
        self.database_service = DatabaseService()

        self.__setup_routes()

    def __setup_routes(self):
        self.blueprint.add_url_rule("/characters", "get_characters", self.get_characters, methods=["GET"])
        self.blueprint.add_url_rule(
            "/characters/<string:character_id>", "get_character", self.get_character, methods=["GET"]
        )

    def get_characters(self):
        characters = self.database_service.get_characters()
        return jsonify(characters)

    def get_character(self, character_id):
        character = self.database_service.get_character(character_id)
        return jsonify(character)
