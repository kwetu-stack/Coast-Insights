from sqlalchemy import func
from flask import render_template
from flask_login import login_required

from . import dashboard_bp
from extensions import db
from models import Sale


@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    # --------------------------------------------------
    # KPI SUMMARY
    # --------------------------------------------------

    stats = db.session.query(
        func.coalesce(func.sum(Sale.value), 0),
        func.count(Sale.id),
        func.count(func.distinct(Sale.customer_name)),
        func.coalesce(func.avg(Sale.value), 0),
        func.coalesce(func.max(Sale.value), 0),
        func.coalesce(func.min(Sale.value), 0),
    ).first()

    dashboard = {
        "total_sales": float(stats[0] or 0),
        "transactions": int(stats[1] or 0),
        "customers": int(stats[2] or 0),
        "average_sale": float(stats[3] or 0),
        "highest_sale": float(stats[4] or 0),
        "lowest_sale": float(stats[5] or 0),
    }

    # --------------------------------------------------
    # DAILY SALES TREND
    # --------------------------------------------------

    daily_sales = (
        db.session.query(
            Sale.sale_date,
            func.sum(Sale.value)
        )
        .group_by(Sale.sale_date)
        .order_by(Sale.sale_date)
        .all()
    )

    chart_labels = [
        sale_date.strftime("%d %b")
        for sale_date, _ in daily_sales
    ]

    chart_values = [
        float(total)
        for _, total in daily_sales
    ]

    # --------------------------------------------------
    # SALES BY CHANNEL
    # --------------------------------------------------

    channel_sales = (
        db.session.query(
            Sale.channel,
            func.sum(Sale.value)
        )
        .group_by(Sale.channel)
        .order_by(func.sum(Sale.value).desc())
        .all()
    )

    channel_labels = [
        channel if channel else "Unknown"
        for channel, _ in channel_sales
    ]

    channel_values = [
        float(total)
        for _, total in channel_sales
    ]

    # --------------------------------------------------
    # TOP 10 CUSTOMERS
    # --------------------------------------------------

    top_customers = (
        db.session.query(
            Sale.customer_name,
            func.sum(Sale.value).label("total_sales")
        )
        .group_by(Sale.customer_name)
        .order_by(func.sum(Sale.value).desc())
        .limit(10)
        .all()
    )

    top_customer_labels = [
        customer if customer else "Unknown"
        for customer, _ in top_customers
    ]

    top_customer_values = [
        float(total)
        for _, total in top_customers
    ]
        # --------------------------------------------------
    # SALES BY LOCATION
    # --------------------------------------------------

    location_sales = (
        db.session.query(
            Sale.location,
            func.sum(Sale.value).label("total_sales")
        )
        .group_by(Sale.location)
        .order_by(func.sum(Sale.value).desc())
        .all()
    )

    location_labels = [
        location if location else "Unknown"
        for location, _ in location_sales
    ]

    location_values = [
        float(total)
        for _, total in location_sales
    ]
        # --------------------------------------------------
    # EXECUTIVE INTELLIGENCE
    # --------------------------------------------------

    executive = {
        "summary": [
            f"Total Coast sales stand at KES {dashboard['total_sales']:,.2f}.",
            f"The region has recorded {dashboard['transactions']} transactions from {dashboard['customers']} unique customers.",
            f"The average transaction value is KES {dashboard['average_sale']:,.2f}.",
            f"The highest recorded sale is KES {dashboard['highest_sale']:,.2f}.",
            f"The lowest recorded sale is KES {dashboard['lowest_sale']:,.2f}.",
            "Sales performance can now be analysed by customer, channel and location.",
            "Recommendation: Protect high-value customers while prioritising growth in lower-performing locations and channels."
        ]
    }

    # --------------------------------------------------
    # RENDER PAGE
    # --------------------------------------------------

    return render_template(
        "dashboard/index.html",
        dashboard=dashboard,
        chart_labels=chart_labels,
        chart_values=chart_values,
               channel_labels=channel_labels,
        channel_values=channel_values,
        top_customer_labels=top_customer_labels,
               top_customer_values=top_customer_values,
        location_labels=location_labels,
        location_values=location_values,
        executive=executive,
    )