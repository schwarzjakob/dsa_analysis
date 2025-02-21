from flask import Flask, jsonify
from flask.wrappers import Response
from flask_cors import CORS
from flask_smorest import Api

from typing import Literal


from blueprints.dsa4_blueprint import Dsa4Blueprint
from blueprints.dsa5_blueprint import Dsa5Blueprint

backend = Flask(import_name=__name__)
backend.config["API_TITLE"] = "Dsa Analysis Backend"
backend.config["API_VERSION"] = "0.1"
backend.config["OPENAPI_VERSION"] = "3.0.2"
backend.config["OPENAPI_URL_PREFIX"] = "/"
backend.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
api = Api(backend)

# TODO Allow all origins during development, adjust it in production
origins = ["*"]
CORS(backend, resources={r"/*": {"origins": origins}})

dsa4_blueprint = Dsa4Blueprint()
api.register_blueprint(dsa4_blueprint.blueprint)

dsa5_blueprint = Dsa5Blueprint()
api.register_blueprint(dsa5_blueprint.blueprint)


@backend.route("/health", methods=["GET"])
def check_health() -> tuple[Response, Literal[200]]:
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    backend.run(debug=True)
