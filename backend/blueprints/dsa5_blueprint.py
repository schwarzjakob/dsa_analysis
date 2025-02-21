from flask import request, jsonify
from flask_smorest import Blueprint


from config.logger_config import logger
from services.dsa5_database_service import Dsa5DatabaseService as DatabaseService


class Dsa5Blueprint:
    def __init__(self):
        self.blueprint = Blueprint("dsa5", "dsa5", url_prefix="/dsa5")
        self.database_service = DatabaseService()

        self.__setup_routes()

    def __setup_routes(self):
        self.blueprint.add_url_rule("/characters", "get_characters", self.get_characters, methods=["GET"])

    def get_characters(self):
        characters = self.database_service.get_characters()
        logger.info(f"Characters: {characters}")
        return jsonify(characters)
