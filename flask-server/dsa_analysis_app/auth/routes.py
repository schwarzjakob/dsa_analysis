from . import google_auth_blueprint
from flask import current_app, redirect, url_for, session, jsonify
from .google_auth import google_authorization
from dsa_analysis_app.utils.logger_config import setup_logger

logger = setup_logger(__name__)


@google_auth_blueprint.route("/login")
def login():
    google = current_app.config.get("google")
    redirect_uri = url_for("google_auth.authorize", _external=True)
    logger.debug(f"Google: {google}")
    return google.authorize_redirect(
        redirect_uri=url_for("google_auth.authorize", _external=True)
    )


@google_auth_blueprint.route("/login/authorize")
def authorize():
    google = current_app.config.get("google")
    logger.debug(f"Google: {google}")
    token = google.authorize_access_token()
    user_info = google.get("https://www.googleapis.com/oauth2/v1/userinfo").json()
    session["user"] = user_info
    logger.debug(f"User info: {user_info}")
    return redirect("http://127.0.0.1:3000/start")  # Redirect to the start page
