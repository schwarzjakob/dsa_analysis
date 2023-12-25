# flask-server/dsa_analysis_app/chat_processing/chat_log_parser.py
# Flask imports
from flask import request, jsonify
from . import chat_log_parser_blueprint
from .chat_log_parser import DsaStats
import logging
import os

# Configure logger
logger = logging.getLogger(__name__)
# Format containts the [time filename->funcName():lineno] level: message
FORMAT = '[%(asctime)s %(filename)s->%(funcName)s():%(lineno)d] %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

UPLOAD_FOLDER = './uploads'

@chat_log_parser_blueprint.route('/process_chatlog', methods=['POST'])
def process_chatlog_route():
    logger.debug("process_chatlog_route called")
    try:
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        if file.filename == '':
            return 'No selected file', 400
        if file:
            filename = "chatlog.txt"

            # Make sure the uploads folder exists
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            
            # Save the file to the uploads folder
            chatlog_file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(chatlog_file_path)

            # Run your Python script here passing the uploaded file as a command line argument
            current_dsa_stats = DsaStats()
            chatlogLines = current_dsa_stats.process_chatlog(chatlog_file_path)
            current_dsa_stats.main(chatlogLines)

            logger.debug(f'File uploaded successfully to {chatlog_file_path}')
            return f'File uploaded successfully to {chatlog_file_path}', 200
    
    except Exception as e:
        logger.error(e)
        return f'Error: {e}', 500

