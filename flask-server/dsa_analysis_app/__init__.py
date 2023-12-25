# flask-server/dsa_analysis_app/__init__.py
from flask import Flask
from .chat_processing import chat_log_parser_blueprint
from .character_analysis import character_analysis_blueprint
from .characters_management import characters_management_blueprint
from .auth import google_auth_blueprint

def create_app():
    dsa_analysis_app = Flask(__name__)
    dsa_analysis_app.register_blueprint(chat_log_parser_blueprint, url_prefix='/chat_processing')
    dsa_analysis_app.register_blueprint(character_analysis_blueprint, url_prefix='/character_analysis') 
    dsa_analysis_app.register_blueprint(characters_management_blueprint, url_prefix='/characters_management') 
    dsa_analysis_app.register_blueprint(google_auth_blueprint, url_prefix='/auth')
    return dsa_analysis_app