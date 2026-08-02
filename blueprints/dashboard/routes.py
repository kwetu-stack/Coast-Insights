from flask import render_template
from flask_login import login_required

from . import dashboard_bp
from services.dashboard_service import get_dashboard_data


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    dashboard_data = get_dashboard_data()

    return render_template(
        "dashboard/index.html",
        **dashboard_data
    )