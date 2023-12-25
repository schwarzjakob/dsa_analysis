from flask import Flask
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv
from dsa_analysis_app.auth.google_auth import google_auhtorization

load_dotenv()

# Add the path to the directory containing the dsa_analysis_app package to the system path
sys.path.append('/Users/jakobschwarz/Documents/Coding/Python/dsa_rolls_webapp/flask-server/dsa_analysis_app')
from dsa_analysis_app import create_app

app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = os.getenv('SECRET_KEY')
google_auhtorization(app)


if __name__ == '__main__':
    app.run(debug=True)
