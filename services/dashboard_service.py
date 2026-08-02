from sqlalchemy import func
from sqlalchemy import extract, func

from extensions import db
from models import Sale


# ==========================================================
# DASHBOARD KPI SUMMARY
# ==========================================================

def get_dashboard_summary():

    stats = db.session.query(
        func.coalesce(func.sum(Sale.value), 0),
        func.count(Sale.id),
        func.count(func.distinct(Sale.customer_name)),
        func.coalesce(func.avg(Sale.value), 0),
        func.coalesce(func.max(Sale.value), 0),
        func.coalesce(func.min(Sale.value), 0),
    ).first()

    return {
        "total_sales": float(stats[0] or 0),
        "transactions": int(stats[1] or 0),
        "customers": int(stats[2] or 0),
        "average_sale": float(stats[3] or 0),
        "highest_sale": float(stats[4] or 0),
        "lowest_sale": float(stats[5] or 0),
    }


# ==========================================================
# DAILY SALES TREND
# ==========================================================

def get_daily_sales():

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

    return chart_labels, chart_values


# ==========================================================
# SALES BY CHANNEL
# ==========================================================

def get_channel_analysis():

    channel_sales = (
        db.session.query(
            Sale.channel,
            func.sum(Sale.value).label("total_sales")
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

    total_sales = sum(channel_values)

    channel_breakdown = []

    for channel, total in channel_sales:

        value = float(total)

        percentage = 0

        if total_sales > 0:
            percentage = round((value / total_sales) * 100, 2)

        channel_breakdown.append({
            "channel": channel if channel else "Unknown",
            "sales": value,
            "percentage": percentage
        })

    return (
        channel_labels,
        channel_values,
        channel_breakdown
    )
    # ==========================================================
# TOP 10 CUSTOMERS
# ==========================================================

def get_top_customers():

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

    return (
        top_customer_labels,
        top_customer_values
    )


# ==========================================================
# SALES BY LOCATION
# ==========================================================

def get_location_analysis():

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

    return (
        location_labels,
        location_values
    )


# ==========================================================
# CUSTOMER PROFILING
# ==========================================================

def get_customer_profiles():

    customer_sales = (
        db.session.query(
            Sale.customer_name,
            func.sum(Sale.value).label("total_sales")
        )
        .group_by(Sale.customer_name)
        .order_by(func.sum(Sale.value).desc())
        .all()
    )

    profiles = {
        "platinum": [],
        "gold": [],
        "silver": [],
        "bronze": []
    }

    for customer, total in customer_sales:

        total = float(total or 0)

        customer_record = {
            "customer": customer,
            "sales": total
        }

        if total >= 500000:

            profiles["platinum"].append(customer_record)

        elif total >= 250000:

            profiles["gold"].append(customer_record)

        elif total >= 100000:

            profiles["silver"].append(customer_record)

        else:

            profiles["bronze"].append(customer_record)

    profile_summary = {

        "platinum": len(profiles["platinum"]),

        "gold": len(profiles["gold"]),

        "silver": len(profiles["silver"]),

        "bronze": len(profiles["bronze"]),
    }

    return profiles, profile_summary


# ==========================================================
# GROWTH TARGETS
# ==========================================================

def get_growth_targets():

    # ---------------------------------------------
    # Detect latest month in the database
    # ---------------------------------------------

    latest_date = db.session.query(
        func.max(Sale.sale_date)
    ).scalar()

    if latest_date is None:
        return []

    current_month = latest_date.month
    current_year = latest_date.year

    previous_month = current_month - 1
    previous_year = current_year

    if previous_month == 0:
        previous_month = 12
        previous_year -= 1

    # ---------------------------------------------
    # Previous Month Sales (Baseline)
    # ---------------------------------------------

    baseline_sales = (
        db.session.query(
            Sale.customer_name,
            func.sum(Sale.value).label("baseline_sales")
        )
        .filter(
            extract("month", Sale.sale_date) == previous_month,
            extract("year", Sale.sale_date) == previous_year,
        )
        .group_by(Sale.customer_name)
        .all()
    )

    # ---------------------------------------------
    # Current Month Sales
    # ---------------------------------------------

    current_sales = (
        db.session.query(
            Sale.customer_name,
            func.sum(Sale.value).label("current_sales")
        )
        .filter(
            extract("month", Sale.sale_date) == current_month,
            extract("year", Sale.sale_date) == current_year,
        )
        .group_by(Sale.customer_name)
        .all()
    )

    current_lookup = {
        customer: float(total or 0)
        for customer, total in current_sales
    }

    targets = []

    for customer, baseline in baseline_sales:

        baseline = float(baseline or 0)

        current = current_lookup.get(customer, 0)

        target = baseline * 1.15

        achievement = 0

        if target > 0:
            achievement = round((current / target) * 100, 2)

        targets.append({

            "customer": customer,

            "baseline_sales": baseline,

            "current_sales": current,

            "target": target,

            "achievement": achievement

        })

    targets.sort(
        key=lambda x: x["baseline_sales"],
        reverse=True
    )

    return targets
# ==========================================================
# EXECUTIVE INTELLIGENCE
# ==========================================================

def get_executive_summary(dashboard):

    return {
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


# ==========================================================
# PREDICTIVE INSIGHTS
# ==========================================================

def get_predictive_insights(profile_summary):

    insights = []

    if profile_summary["platinum"] > 0:
        insights.append(
            f"{profile_summary['platinum']} Platinum customers require priority retention."
        )

    if profile_summary["gold"] > 0:
        insights.append(
            f"{profile_summary['gold']} Gold customers present strong growth opportunities."
        )

    if profile_summary["silver"] > 0:
        insights.append(
            f"{profile_summary['silver']} Silver customers should be developed into Gold accounts."
        )

    if profile_summary["bronze"] > 0:
        insights.append(
            f"{profile_summary['bronze']} Bronze customers require increased market coverage."
        )

    return insights


# ==========================================================
# AI ASSISTED RECOMMENDATIONS
# ==========================================================

def get_ai_recommendations(profile_summary):

    recommendations = [

        "Protect and retain all Platinum customers.",

        "Focus weekly visits on Gold customers with growth potential.",

        "Develop Silver customers through increased product penetration.",

        "Convert Bronze customers into higher-value accounts using structured sales visits."

    ]

    return recommendations


# ==========================================================
# COMPLETE DASHBOARD DATA
# ==========================================================

def get_dashboard_data():

    dashboard = get_dashboard_summary()

    chart_labels, chart_values = get_daily_sales()

    (
        channel_labels,
        channel_values,
        channel_breakdown
    ) = get_channel_analysis()

    (
        top_customer_labels,
        top_customer_values
    ) = get_top_customers()

    (
        location_labels,
        location_values
    ) = get_location_analysis()

    (
        customer_profiles,
        profile_summary
    ) = get_customer_profiles()

    growth_targets = get_growth_targets()

    predictive_insights = get_predictive_insights(
        profile_summary
    )

    ai_recommendations = get_ai_recommendations(
        profile_summary
    )

    executive = get_executive_summary(
        dashboard
    )

    return {

        "dashboard": dashboard,

        "chart_labels": chart_labels,
        "chart_values": chart_values,

        "channel_labels": channel_labels,
        "channel_values": channel_values,
        "channel_breakdown": channel_breakdown,

        "top_customer_labels": top_customer_labels,
        "top_customer_values": top_customer_values,

        "location_labels": location_labels,
        "location_values": location_values,

        "customer_profiles": customer_profiles,
        "profile_summary": profile_summary,

        "growth_targets": growth_targets,

        "predictive_insights": predictive_insights,

        "ai_recommendations": ai_recommendations,

        "executive": executive,

    }