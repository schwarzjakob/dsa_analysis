from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import sys
import logging

# Add the path to the directory containing dsa_analysis.py and dsa_stats.py to the system path
sys.path.append('/Users/jakobschwarz/Documents/Coding/Python/dsa_rolls_webapp/flask-server/dsa_analysis')

# Now you can import from dsa_analysis.py
from dsa_analysis import dsa_analysis
from dsa_analysis import dsa_stats

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def file_upload():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filename = "chatlog.txt"

        # Make sure the uploads folder exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        
        # Save the file to the uploads folder
        chatlog_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(chatlog_file_path)

        # Run your Python script here passing the uploaded file as a command line argument
        current_dsa_stats = dsa_stats.DsaStats()
        chatlogLines = current_dsa_stats.process_chatlog(chatlog_file_path)
        current_dsa_stats.main(chatlogLines)

        logger.debug(f'File uploaded successfully to {chatlog_file_path}')
        return f'File uploaded successfully to {chatlog_file_path}', 200

@app.route("/character-data/<character_name>", methods=['GET'])
def get_character_data(character_name):
    # Logic to fetch data for the given character name
    # This can be reading from a CSV file or a database query
    # Return the data in JSON format
    return f'We have to check the character. Working in Progress', 200

@app.route("/characters", methods=['GET'])
def get_characters():
    try:
        with open('./dsa_analysis/data/json/characters.json') as file:
            characters_data = json.load(file)
        return characters_data
    except FileNotFoundError:
        return "File not found", 404

@app.route('/talents/<character_name>', methods=['GET'])
def get_talents(character_name):

    # Initialize outputs to default values
    talents_output = None
    traits_values_output = None
    traits_relative_output = None
    categories_relative_output = None
    
    # Call the dsa_analysis.py script with necessary arguments
    try:
        talents_output = dsa_analysis.get_character_talents(character_name)
        logger.debug(f'Talents of:  {character_name}, : {talents_output}')
        traits_values_output = dsa_analysis.get_character_traits_values(character_name)
        logger.debug(f'Traits Values of:  {character_name}, : {traits_values_output}')
        traits_relative_output = dsa_analysis.get_character_relative_traits_usage(character_name)
        logger.debug(f'Traits Distribution Usage of:  {character_name}, : {traits_relative_output}')
        categories_relative_output = dsa_analysis.get_character_relative_talents_categories_usage(character_name)
        logger.debug(f'Categories Distribution Usage of:  {character_name}, : {categories_relative_output}')
    except Exception as error:
        logger.error(f'Error getting values for {character_name}: {error}')

    data = {
        "talents": talents_output,
        "traits_relative": traits_relative_output,
        "traits_values": traits_values_output,
        "categories_relative": categories_relative_output
    }
    #logger.debug(f'Test for Categories for:  {character_name}, : {categories_relative_output}')
    return jsonify(data)

@app.route('/analyze-talent', methods=['POST'])
def analyze_talent():
    data = request.json
    character_name = data.get('characterName')
    talent_name = data.get('talentName')

    #Initialize output to default values
    talent_line_chart_output = None

    # Call the dsa_analysis.py script with necessary arguments
    try:
        talent_line_chart_output = dsa_analysis.get_character_talent_line_chart(character_name, talent_name)
        logger.debug(f'Talent Line Chart of:  {character_name}, : {talent_line_chart_output}')
    except Exception as error:
        logger.error(f'Error getting talent line chart for {character_name} and {talent_name}: {error}')
    
    return jsonify(talent_line_chart_output)



if __name__ == '__main__':
    # Format containts the [time filename->funcName():lineno] level: message
    FORMAT = '[%(asctime)s %(filename)s->%(funcName)s():%(lineno)d] %(levelname)s: %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    app.run(debug=True)
