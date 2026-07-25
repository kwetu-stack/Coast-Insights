import csv
from io import StringIO

from flask import Response
from datetime import datetime

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import login_required, current_user

from extensions import db
from models import TradeVisit
from decorators import admin_required

from . import trade_visits_bp



@trade_visits_bp.route("/trade-visits")
@login_required
def index():

    visits = TradeVisit.query.order_by(
        TradeVisit.created_at.desc()
    ).all()

    return render_template(
        "trade_visits/index.html",
        visits=visits
    )



@trade_visits_bp.route("/trade-visits/<int:id>")
@login_required
def view(id):

    visit = TradeVisit.query.get_or_404(id)

    return render_template(
        "trade_visits/view.html",
        visit=visit
    )



@trade_visits_bp.route(
    "/trade-visits/<int:id>/edit",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def edit(id):

    visit = TradeVisit.query.get_or_404(id)


    if request.method == "POST":

        visit.outlet_name = request.form.get(
            "outlet_name"
        )

        visit.location = request.form.get(
            "location"
        )

        visit.contact_person = request.form.get(
            "contact_person"
        )

        visit.phone_number = request.form.get(
            "phone_number"
        )

        visit.outlet_type = request.form.get(
            "outlet_type"
        )


        visit.buying_razco = request.form.get(
            "buying_razco"
        )

        visit.products_purchased = request.form.get(
            "products_purchased"
        )

        visit.current_supplier = request.form.get(
            "current_supplier"
        )

        visit.restocking_frequency = request.form.get(
            "restocking_frequency"
        )

        visit.average_order_size = request.form.get(
            "average_order_size"
        )


        visit.customer_status = request.form.get(
            "customer_status"
        )


        visit.competitor_brand = request.form.get(
            "competitor_brand"
        )

        visit.competitor_product = request.form.get(
            "competitor_product"
        )

        visit.competitor_price = request.form.get(
            "competitor_price"
        )

        visit.competitor_promotion = request.form.get(
            "competitor_promotion"
        )

        visit.competitor_equipment = request.form.get(
            "competitor_equipment"
        )

        visit.display_observation = request.form.get(
            "display_observation"
        )


        visit.opportunity_type = request.form.get(
            "opportunity_type"
        )

        visit.estimated_potential = request.form.get(
            "estimated_potential"
        )

        visit.next_action = request.form.get(
            "next_action"
        )

        visit.notes = request.form.get(
            "notes"
        )


        db.session.commit()


        flash(
            "Trade visit updated successfully.",
            "success"
        )


        return redirect(
            url_for(
                "trade_visits.view",
                id=visit.id
            )
        )


    return render_template(
        "trade_visits/edit.html",
        visit=visit
    )



@trade_visits_bp.route(
    "/trade-visits/<int:id>/delete"
)
@login_required
@admin_required
def delete(id):

    visit = TradeVisit.query.get_or_404(id)

    db.session.delete(visit)

    db.session.commit()


    flash(
        "Trade visit deleted successfully.",
        "success"
    )


    return redirect(
        url_for(
            "trade_visits.index"
        )
    )



@trade_visits_bp.route(
    "/trade-visits/new",
    methods=["GET", "POST"]
)
@login_required
@admin_required
def create():

    if request.method == "POST":

        visit_date = request.form.get(
            "visit_date"
        )

        follow_up_date = request.form.get(
            "follow_up_date"
        )


        visit = TradeVisit(

            visit_date=datetime.strptime(
                visit_date,
                "%Y-%m-%d"
            ).date(),


            sales_officer=current_user.username,


            outlet_name=request.form.get(
                "outlet_name"
            ),

            location=request.form.get(
                "location"
            ),

            contact_person=request.form.get(
                "contact_person"
            ),

            phone_number=request.form.get(
                "phone_number"
            ),

            outlet_type=request.form.get(
                "outlet_type"
            ),


            buying_razco=request.form.get(
                "buying_razco"
            ),

            products_purchased=request.form.get(
                "products_purchased"
            ),

            current_supplier=request.form.get(
                "current_supplier"
            ),

            restocking_frequency=request.form.get(
                "restocking_frequency"
            ),

            average_order_size=request.form.get(
                "average_order_size"
            ),


            customer_status=request.form.get(
                "customer_status"
            ),


            competitor_brand=request.form.get(
                "competitor_brand"
            ),

            competitor_product=request.form.get(
                "competitor_product"
            ),

            competitor_price=request.form.get(
                "competitor_price"
            ),

            competitor_promotion=request.form.get(
                "competitor_promotion"
            ),

            competitor_equipment=request.form.get(
                "competitor_equipment"
            ),

            display_observation=request.form.get(
                "display_observation"
            ),


            opportunity_type=request.form.get(
                "opportunity_type"
            ),

            estimated_potential=request.form.get(
                "estimated_potential"
            ),

            next_action=request.form.get(
                "next_action"
            ),


            follow_up_date=datetime.strptime(
                follow_up_date,
                "%Y-%m-%d"
            ).date()
            if follow_up_date
            else None,


            notes=request.form.get(
                "notes"
            )

        )


        db.session.add(visit)

        db.session.commit()


        flash(
            "Trade visit saved successfully.",
            "success"
        )


        return redirect(
            url_for(
                "trade_visits.index"
            )
        )


    return render_template(
        "trade_visits/create.html"
    )
@trade_visits_bp.route("/trade-visits/export")
@login_required
@admin_required
def export():

    visits = TradeVisit.query.order_by(
        TradeVisit.created_at.desc()
    ).all()


    output = StringIO()

    writer = csv.writer(output)


    writer.writerow([
        "Date",
        "Sales Officer",
        "Outlet",
        "Location",
        "Contact Person",
        "Phone",
        "Outlet Type",
        "Buying Razco",
        "Products Purchased",
        "Supplier",
        "Restocking Frequency",
        "Average Order Size",
        "Customer Status",
        "Competitor Brand",
        "Competitor Product",
        "Competitor Price",
        "Competitor Promotion",
        "Competitor Equipment",
        "Display Observation",
        "Opportunity Type",
        "Estimated Potential",
        "Next Action",
        "Follow Up Date",
        "Notes"
    ])


    for visit in visits:

        writer.writerow([

            visit.visit_date,
            visit.sales_officer,
            visit.outlet_name,
            visit.location,
            visit.contact_person,
            visit.phone_number,
            visit.outlet_type,
            visit.buying_razco,
            visit.products_purchased,
            visit.current_supplier,
            visit.restocking_frequency,
            visit.average_order_size,
            visit.customer_status,
            visit.competitor_brand,
            visit.competitor_product,
            visit.competitor_price,
            visit.competitor_promotion,
            visit.competitor_equipment,
            visit.display_observation,
            visit.opportunity_type,
            visit.estimated_potential,
            visit.next_action,
            visit.follow_up_date,
            visit.notes

        ])


    output.seek(0)


    return Response(
        output,
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=trade_visits.csv"
        }
    )    