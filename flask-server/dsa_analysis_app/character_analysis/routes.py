# flask-server/dsa_analysis_app/character_analysis/routes.py
from flask import jsonify, request
from . import character_analysis_blueprint
from . import character_analysis
import logging

logger = logging.getLogger(__name__)


@character_analysis_blueprint.route("/talents/<character_name>", methods=["GET"])
def get_talents(character_name):
    # Initialize outputs to default values
    talents_output = None
    traits_values_output = None
    traits_relative_output = None
    categories_relative_output = None
    attacks_output = None

    # Call the character_analysis.py script with necessary arguments
    try:
        talents_output = character_analysis.get_character_talents(character_name)
        logger.debug(f"Getting talents of: {character_name}")
        traits_values_output = character_analysis.get_character_traits_values(
            character_name
        )
        logger.debug(f"Getting traits values of: {character_name}")
        traits_relative_output = character_analysis.get_character_relative_traits_usage(
            character_name
        )
        logger.debug(f"Getting traits distribution usage of: {character_name}")
        categories_relative_output = (
            character_analysis.get_character_relative_talents_categories_usage(
                character_name
            )
        )
        logger.debug(f"Getting categories distribution usage of: {character_name}")
    except Exception as error:
        logger.error(f"Error getting values for {character_name}: {error}")

    data = {
        "talents": talents_output,
        "traits_relative": traits_relative_output,
        "traits_values": traits_values_output,
        "categories_relative": categories_relative_output,
    }
    return jsonify(data)


@character_analysis_blueprint.route("/analyze-talent", methods=["POST"])
def analyze_talent():
    data = request.json
    character_name = data.get("characterName")
    talent_name = data.get("talentName")

    # Initialize output to default values
    talent_statistics = None
    talent_line_chart_output = None
    talent_investment_recommendation = None

    # Call the character_analysis.py script with necessary arguments
    try:
        talent_statistics = character_analysis.get_character_talent_statistics(
            character_name, talent_name
        )
        logger.debug(f"Talent Statistics of:  {character_name}, {talent_name}")
        talent_line_chart_output = character_analysis.get_character_talent_line_chart(
            character_name, talent_name
        )
        logger.debug(f"Talent Line Chart of:  {character_name}, {talent_name}")
        talent_investment_recommendation = (
            character_analysis.get_character_talent_investment_recommendation(
                talent_statistics
            )
        )
        logger.debug(
            f"Talent Investment Recommendation of:  {character_name}, {talent_name}"
        )

    except Exception as error:
        logger.error(f"Error getting values for {character_name}: {error}")

    data = {
        "talent_statistics": talent_statistics,
        "talent_line_chart": talent_line_chart_output,
        "talent_investment_recommendation": talent_investment_recommendation,
    }

    return jsonify(data)


@character_analysis_blueprint.route("/attacks/<character_name>", methods=["GET"])
def get_attacks(character_name):
    # Logic to fetch data for the given character name"""

    # Initialize outputs to default values
    attacks_output = None

    # Call the character_analysis.py script with necessary arguments
    try:
        attacks_output = character_analysis.get_character_attacks(character_name)
        logger.debug(f"Getting attacks of:  {character_name}")
    except Exception as error:
        logger.error(f"Error getting values for {character_name}: {error}")

    data = {"attacks": attacks_output}

    return jsonify(data)


@character_analysis_blueprint.route("/analyze-attack", methods=["POST"])
def analyze_attack():
    data = request.json
    character_name = data.get("characterName")
    attack_name = data.get("attackName")

    # Initialize output to default values
    attack_statistics = None
    attack_line_chart_output = None

    # Call the character_analysis.py script with necessary arguments
    try:
        attack_statistics = character_analysis.get_character_attack_statistics(
            character_name, attack_name
        )
        logger.debug(f"Attack Statistics of:  {character_name}, {attack_name}")
        attack_line_chart_output = character_analysis.get_character_attack_line_chart(
            character_name, attack_name
        )
        logger.debug(f"Attack Line Chart of:  {character_name}, {attack_name}")

    except Exception as error:
        logger.error(f"Error getting values for {character_name}: {error}")

    data = {
        "attack_statistics": attack_statistics,
        "attack_line_chart": attack_line_chart_output,
    }

    return jsonify(data)
