from datetime import datetime, timezone, timedelta

from extensions import db


# ---------------------------------------------------------
# East Africa Time (UTC+3)
# Kenya does not observe daylight saving time.
# ---------------------------------------------------------

EAT = timezone(timedelta(hours=3))


def nairobi_now():
    return datetime.now(EAT)


class TradeVisit(db.Model):
    __tablename__ = "trade_visits"

    id = db.Column(db.Integer, primary_key=True)

    # ---------------------------------------------------------
    # Visit Information
    # ---------------------------------------------------------

    visit_date = db.Column(
        db.Date,
        nullable=False,
        default=lambda: nairobi_now().date()
    )

    sales_officer = db.Column(
        db.String(100),
        nullable=True
    )

    # ---------------------------------------------------------
    # Outlet Information
    # ---------------------------------------------------------

    outlet_name = db.Column(
        db.String(150),
        nullable=False
    )

    location = db.Column(
        db.String(100),
        nullable=False
    )

    contact_person = db.Column(
        db.String(100),
        nullable=True
    )

    phone_number = db.Column(
        db.String(30),
        nullable=True
    )

    outlet_type = db.Column(
        db.String(50),
        nullable=True
    )

    # ---------------------------------------------------------
    # Current Business Status
    # ---------------------------------------------------------

    buying_razco = db.Column(
        db.String(10),
        nullable=True
    )

    products_purchased = db.Column(
        db.Text,
        nullable=True
    )

    current_supplier = db.Column(
        db.String(150),
        nullable=True
    )

    restocking_frequency = db.Column(
        db.String(100),
        nullable=True
    )

    average_order_size = db.Column(
        db.String(100),
        nullable=True
    )

    # ---------------------------------------------------------
    # Customer Classification
    # ---------------------------------------------------------

    customer_status = db.Column(
        db.String(50),
        nullable=True
    )

    # ---------------------------------------------------------
    # Competitor Intelligence
    # ---------------------------------------------------------

    competitor_brand = db.Column(
        db.String(100),
        nullable=True
    )

    competitor_product = db.Column(
        db.String(100),
        nullable=True
    )

    competitor_price = db.Column(
        db.String(50),
        nullable=True
    )

    competitor_promotion = db.Column(
        db.String(200),
        nullable=True
    )

    competitor_equipment = db.Column(
        db.String(200),
        nullable=True
    )

    display_observation = db.Column(
        db.Text,
        nullable=True
    )

    # ---------------------------------------------------------
    # Opportunity
    # ---------------------------------------------------------

    opportunity_type = db.Column(
        db.String(100),
        nullable=True
    )

    estimated_potential = db.Column(
        db.String(100),
        nullable=True
    )

    next_action = db.Column(
        db.String(200),
        nullable=True
    )

    follow_up_date = db.Column(
        db.Date,
        nullable=True
    )

    notes = db.Column(
        db.Text,
        nullable=True
    )

    # ---------------------------------------------------------
    # Audit Fields
    # ---------------------------------------------------------

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=nairobi_now
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=nairobi_now,
        onupdate=nairobi_now
    )

    # ---------------------------------------------------------

    def __repr__(self):
        return f"<TradeVisit {self.outlet_name}>"