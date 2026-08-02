from datetime import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    abort,
)

from flask_login import (
    login_required,
    current_user,
)

from extensions import db
from models import WeeklySummary

from . import weekly_summary_bp


@weekly_summary_bp.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":

        if current_user.role != "admin":

            flash(
                "Only administrators can submit weekly summaries.",
                "danger"
            )

            return redirect(
                url_for("weekly_summary.index")
            )

        summary = WeeklySummary(

            week_commencing=datetime.strptime(
                request.form["week_commencing"],
                "%Y-%m-%d"
            ).date(),

            route_plan=request.form["route_plan"],

            accounts_opened=request.form["accounts_opened"],

            prospects=request.form["prospects"],

            trade_visits=request.form["trade_visits"]

        )

        db.session.add(summary)
        db.session.commit()

        flash(
            "Weekly Summary saved successfully.",
            "success"
        )

        return redirect(
            url_for("weekly_summary.index")
        )

    summaries = (
        WeeklySummary.query
        .order_by(
            WeeklySummary.week_commencing.desc()
        )
        .all()
    )

    return render_template(
        "weekly_summary/index.html",
        summaries=summaries
    )


@weekly_summary_bp.route("/view/<int:summary_id>")
@login_required
def view(summary_id):

    summary = WeeklySummary.query.get(summary_id)

    if summary is None:
        abort(404)

    return render_template(
        "weekly_summary/view.html",
        summary=summary
    )