from flask import Blueprint

bp = Blueprint('auth', __name__)

from test_app.auth import routes