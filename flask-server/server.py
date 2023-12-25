from flask import Flask
from flask_cors import CORS
import sys

# Add the path to the directory containing the dsa_analysis_app package to the system path
sys.path.append('/Users/jakobschwarz/Documents/Coding/Python/dsa_rolls_webapp/flask-server/dsa_analysis_app')

# New modular approach
from dsa_analysis_app import create_app

app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True)
