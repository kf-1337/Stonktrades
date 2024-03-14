from flask import Blueprint

# dpow: dashboard, portfolio, orderhistory, watchlist
dpow = Blueprint('dpow', __name__)

from . import routes
