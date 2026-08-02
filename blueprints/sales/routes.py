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
    # CUSTOMER SEARCH
    # --------------------------------------------------

    customer_search = request.args.get(
        "customer",
        ""
    ).strip()

    date_from = request.args.get(
        "date_from",
        ""
    )

    date_to = request.args.get(
        "date_to",
        ""
    )

    # --------------------------------------------------
    # ADD DAILY SALES
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

        customer_name = request.form.get(
            "customer_name",
            ""
        ).strip()

        channel = request.form.get(
            "channel",
            ""
        ).strip()

        location = request.form.get(
            "location",
            ""
        ).strip()

        value = request.form.get(
            "value",
            "0"
        )

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
    # START SALES QUERY
    # --------------------------------------------------

    query = Sale.query
        # --------------------------------------------------
    # CUSTOMER FILTER
    # --------------------------------------------------

    if customer_search:

        query = query.filter(
            Sale.customer_name.ilike(
                f"%{customer_search}%"
            )
        )

    # --------------------------------------------------
    # DATE FILTER
    # --------------------------------------------------

    if date_from:

        query = query.filter(
            Sale.sale_date >= datetime.strptime(
                date_from,
                "%Y-%m-%d"
            ).date()
        )

    if date_to:

        query = query.filter(
            Sale.sale_date <= datetime.strptime(
                date_to,
                "%Y-%m-%d"
            ).date()
        )

    # --------------------------------------------------
    # SALES HISTORY
    # --------------------------------------------------

    sales = (
        query
        .order_by(
            Sale.sale_date.asc()
        )
        .all()
    )

    sales_with_totals = []

    running_total = 0

    for sale in sales:

        running_total += float(
            sale.value or 0
        )

        sales_with_totals.append({

            "sale": sale,

            "sales_to_date": running_total

        })

    # --------------------------------------------------
    # CUSTOMER SUMMARY
    # --------------------------------------------------

    summary = None

    if sales:

        total_sales = sum(
            s.value for s in sales
        )

        average_sale = (
            total_sales / len(sales)
        )

        summary = {

            "customer": sales[0].customer_name,

            "channel": sales[0].channel,

            "location": sales[0].location,

            "transactions": len(sales),

            "total_sales": float(total_sales),

            "average_sale": float(average_sale)

        }
            # --------------------------------------------------
    # CUSTOMER PROFILE
    # --------------------------------------------------

    profile = None

    if summary:

        total = summary["total_sales"]

        if total >= 500000:

            profile = "Platinum"

        elif total >= 250000:

            profile = "Gold"

        elif total >= 100000:

            profile = "Silver"

        else:

            profile = "Bronze"

    # --------------------------------------------------
    # AI RECOMMENDATION
    # --------------------------------------------------

    recommendation = None

    if profile == "Platinum":

        recommendation = (
            "Protect this customer. Increase management engagement "
            "and maintain weekly visits."
        )

    elif profile == "Gold":

        recommendation = (
            "Strong growth opportunity. Focus on range expansion "
            "and increased visit frequency."
        )

    elif profile == "Silver":

        recommendation = (
            "Increase product penetration and convert to a Gold account."
        )

    elif profile == "Bronze":

        recommendation = (
            "Review sales potential and increase prospecting activity."
        )

    # --------------------------------------------------
    # RENDER PAGE
    # --------------------------------------------------

    return render_template(
        "sales/index.html",
        sales=sales_with_totals,
        summary=summary,
        profile=profile,
        recommendation=recommendation,
        customer_search=customer_search,
        date_from=date_from,
        date_to=date_to,
    )
    