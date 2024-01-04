from flask import Blueprint, redirect, request, session, url_for
from authlib.integrations.flask_client import OAuth
import os

oauth = OAuth()


def google_authorization(app):
    oauth.init_app(app)
    app.config["google"] = oauth.register(
        name="google",
        client_id=os.getenv("GOOGLE_CLIENT_ID"),
        client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
        server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
        client_kwargs={"scope": "openid email profile"},
    )
    return
