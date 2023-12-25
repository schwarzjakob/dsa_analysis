# flask-server/dsa_analysis_app/chat_processing/__init__.py
from flask import Blueprint

chat_log_parser_blueprint = Blueprint('chat_log_parser', __name__)

from . import routes