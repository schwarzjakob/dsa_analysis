# flask-server/dsa_analysis_app/auth/google_auth.py
from flask import Blueprint, redirect, request, session, url_for
from authlib.integrations.flask_client import OAuth
import os

oauth = OAuth()

def google_auhtorization(app):
    oauth.init_app(app)
    google = oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'openid email profile'}
    )
    return google
