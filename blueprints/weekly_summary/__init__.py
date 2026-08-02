from flask import Blueprint

weekly_summary_bp = Blueprint(
    "weekly_summary",
    __name__,
    url_prefix="/weekly-summary"
)

from . import routes