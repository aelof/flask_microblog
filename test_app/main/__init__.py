from flask import Blueprint

bp = Blueprint('main', __name__)

from test_app.main import routes
