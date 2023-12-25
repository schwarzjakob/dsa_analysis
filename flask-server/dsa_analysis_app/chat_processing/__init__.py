from flask import Blueprint

chat_log_parser_blueprint = Blueprint('chat_log_parser', __name__)

from . import routes