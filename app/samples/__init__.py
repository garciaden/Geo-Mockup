from flask import Blueprint

bp = Blueprint('samples', __name__, template_folder='templates')

from app.samples import routes
