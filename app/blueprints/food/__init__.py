from flask import Blueprint

food = Blueprint('food', __name__, url_prefix='/food')

from . import routes, models