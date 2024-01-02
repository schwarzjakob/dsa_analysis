from flask_cors import CORS
import os
import sys
import logging
from dotenv import load_dotenv
from dsa_analysis_app.auth.google_auth import google_authorization


# Enabling logging (must come first to enable it globally, also for imported modules and packages)
logger_format = (
    "[%(asctime)s %(filename)s->%(funcName)s():%(lineno)d] %(levelname)s: %(message)s"
)
logging.basicConfig(format=logger_format, level=logging.DEBUG)

load_dotenv()

# Add the path to the directory containing the dsa_analysis_app package to the system path
sys.path.append(
    "/Users/jakobschwarz/Documents/Coding/Python/dsa_rolls_webapp/flask-server/dsa_analysis_app"
)
from dsa_analysis_app import create_app

# TB: I wouldn't outsource the mounting of the controllers/blueprints to a separate file.
#     It just adds more indirection and makes it harder to understand the code.
#     This file is called server so I expect to see the server setup (i.e. controller mounting) here.
app = create_app()
CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = os.getenv("SECRET_KEY")
google_authorization(app)


if __name__ == "__main__":
    app.run(debug=True)
