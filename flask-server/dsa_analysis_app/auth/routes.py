# flask-server/dsa_analysis_app/auth/routes.py
from . import google_auth_blueprint
#from .auth import google_auth
from flask import redirect, url_for, session
from .google_auth import google_auhtorization

@google_auth_blueprint.route('/login')
def login():
    return google.authorize_redirect(redirect_uri=url_for('authorize', _external=True))

@google_auth_blueprint.route('/login/authorize')
def authorize():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    session['user'] = user_info
    return redirect(url_for('index'))  # Redirect to the main page or dashboard
