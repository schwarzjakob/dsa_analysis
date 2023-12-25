from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import sys
import logging

# Add the path to the directory containing dsa_analysis.py and dsa_stats.py to the system path
sys.path.append('/Users/jakobschwarz/Documents/Coding/Python/dsa_rolls_webapp/flask-server/dsa_analysis_app')

# Now you can import from dsa_analysis.py
#from dsa_analysis_app import dsa_analysis
#from dsa_analysis_app import dsa_stats

# New modular approach
from dsa_analysis_app import create_app

# Consider importing the constants from dsa_analysis.py
# from dsa_analysis_app.dsa_analysis import CSV_BASE_PATH, TALENTS_CSV, TRAITS_CSV, TRAIT_VALUES_CSV, ATTACKS_CSV, CHARACTER_KEY, CATEGORY_KEY, TALENT_KEY, TALENT_POINTS_KEY

# Configure logger
logger = logging.getLogger(__name__)
# Format containts the [time filename->funcName():lineno] level: message
FORMAT = '[%(asctime)s %(filename)s->%(funcName)s():%(lineno)d] %(levelname)s: %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)

app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True)
