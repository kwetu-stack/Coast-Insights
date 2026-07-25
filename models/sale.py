from datetime import datetime

from extensions import db


class Sale(db.Model):

    __tablename__ = "sales"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    sale_date = db.Column(
        db.Date,
        nullable=False
    )

    customer_name = db.Column(
        db.String(150),
        nullable=False
    )

    channel = db.Column(
        db.String(100),
        nullable=False
    )

    location = db.Column(
        db.String(100),
        nullable=False
    )

    value = db.Column(
        db.Float,
        nullable=False,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"<Sale {self.customer_name} | "
            f"{self.channel} | "
            f"{self.value}>"
        )