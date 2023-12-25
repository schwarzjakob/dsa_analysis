from flask import Blueprint

characters_management_blueprint = Blueprint('characters_management', __name__,)

from . import routes