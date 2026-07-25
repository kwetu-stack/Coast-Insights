from datetime import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from sqlalchemy import func

from extensions import db
from models import Sale

from . import sales_bp


@sales_bp.route("/", methods=["GET", "POST"])
@login_required
def index():

    # --------------------------------------------------
    # ONLY ADMINS CAN CREATE SALES
    # --------------------------------------------------

    if request.method == "POST":

        if current_user.role != "admin":

            flash(
                "You do not have permission to add sales records.",
                "danger"
            )

            return redirect(
                url_for("sales.index")
            )

        sale_date = request.form.get("sale_date")
        customer_name = request.form.get("customer_name", "").strip()
        channel = request.form.get("channel", "").strip()
        location = request.form.get("location", "").strip()
        value = request.form.get("value", "0")

        if (
            not sale_date
            or not customer_name
            or not channel
            or not location
        ):

            flash(
                "Please fill all required fields.",
                "danger"
            )

            return redirect(
                url_for("sales.index")
            )

        try:

            sales_value = float(value)

        except ValueError:

            sales_value = 0

        sale = Sale(

            sale_date=datetime.strptime(
                sale_date,
                "%Y-%m-%d"
            ).date(),

            customer_name=customer_name,

            channel=channel,

            location=location,

            value=sales_value

        )

        db.session.add(sale)
        db.session.commit()

        flash(
            "Sales record saved successfully.",
            "success"
        )

        return redirect(
            url_for("sales.index")
        )

    # --------------------------------------------------
    # SALES LIST
    # --------------------------------------------------

    sales = (
        Sale.query
        .order_by(Sale.sale_date.desc())
        .all()
    )

    sales_with_totals = []

    for sale in sales:

        total = (
            db.session.query(
                func.coalesce(
                    func.sum(Sale.value),
                    0
                )
            )
            .filter(
                Sale.customer_name == sale.customer_name,
                Sale.sale_date <= sale.sale_date
            )
            .scalar()
        )

        sales_with_totals.append(
            {
                "sale": sale,
                "sales_to_date": float(total)
            }
        )

    # --------------------------------------------------
    # RENDER PAGE
    # --------------------------------------------------

    return render_template(
        "sales/index.html",
        sales=sales_with_totals
    )