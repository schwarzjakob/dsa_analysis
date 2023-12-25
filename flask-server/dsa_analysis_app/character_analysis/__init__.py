from flask import Blueprint

character_analysis_blueprint = Blueprint('character_analysis', __name__)

from . import routes