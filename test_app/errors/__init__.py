from flask import Blueprint

bp = Blueprint('errors', __name__)

from test_app.errors import handlers