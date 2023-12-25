# flask-server/dsa_analysis_app/__init__.py
from flask import Flask
from .chat_processing import chat_log_parser_blueprint

def create_app():
    dsa_analysis_app = Flask(__name__)
    dsa_analysis_app.register_blueprint(chat_log_parser_blueprint, url_prefix='/chat_processing')
    return dsa_analysis_app