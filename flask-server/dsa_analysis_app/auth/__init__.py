# flask-server/dsa_analysis_app/auth/__init__.py
from flask import Blueprint

google_auth_blueprint = Blueprint('google_auth', __name__,)

from . import routes