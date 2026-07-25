from flask import Blueprint

trade_visits_bp = Blueprint(
    "trade_visits",
    __name__,
    template_folder="../../templates/trade_visits"
)

from . import routes