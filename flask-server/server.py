from flask import Flask, request, jsonify
from flask_cors import CORS
import os
#from werkzeug.utils import secure_filename
import subprocess
import json
import sys

# Add the path to the directory containing dsa_analysis.py
sys.path.append('/Users/jakobschwarz/Documents/Coding/Python/dsa_rolls_webapp/flask-server/dsa_analysis')

# Now you can import from dsa_analysis.py
from dsa_analysis import dsa_analysis

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
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Run your Python script here
        script_path = os.path.join('./dsa_analysis', 'dsa_stats.py')
        # Assuming your script takes the file path as an argument
        subprocess.run(['python3', script_path, file_path], check=True)

        return f'File uploaded successfully to {file_path}', 200

@app.route("/character-data/<character_name>", methods=['GET'])
def get_character_data(character_name):
    # Logic to fetch data for the given character name
    # This can be reading from a CSV file or a database query
    # Return the data in JSON format
    return f'We have to check the character. Working in Progress', 200

@app.route("/characters", methods=['GET'])
def get_characters():
    print("Current working directory:", os.getcwd())
    try:
        with open('./dsa_analysis/data/json/characters.json') as file:
            characters_data = json.load(file)
        return characters_data
    except FileNotFoundError:
        return "File not found", 404

@app.route('/talents/<character_name>', methods=['GET'])
def get_talents(character_name):
    print(character_name)
    script_path = os.path.join('./dsa_analysis', 'dsa_analysis.py')
    
    talents_output = dsa_analysis.process_talents(character_name)
    traits_relative_output = dsa_analysis.process_traits(character_name)
    
    try:
        traits_values_output = dsa_analysis.get_traits_values(character_name)
    except Exception as error:
        print(error)

    data = {
        "talents": talents_output,
        "traits_relative": traits_relative_output,
        "traits_values": traits_values_output
    }
    #print(data)
    return jsonify(data)

@app.route('/analyze-talent', methods=['POST'])
def analyze_talent():
    data = request.json
    character_name = data.get('characterName')
    talent_name = data.get('talentName')
    print(talent_name)
    # Call the dsa_analysis.py script with necessary arguments
    talent_line_chart_output = dsa_analysis.talent_line_chart(character_name, talent_name)

    print(talent_line_chart_output)
    return jsonify(talent_line_chart_output)



if __name__ == '__main__':
    app.run(debug=True)
