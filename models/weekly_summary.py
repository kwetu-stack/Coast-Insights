from datetime import date

from extensions import db


class WeeklySummary(db.Model):

    __tablename__ = "weekly_summaries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    week_commencing = db.Column(
        db.Date,
        nullable=False,
        default=date.today
    )

    route_plan = db.Column(
        db.Text,
        nullable=False
    )

    accounts_opened = db.Column(
        db.Text,
        nullable=False
    )

    prospects = db.Column(
        db.Text,
        nullable=False
    )

    trade_visits = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    def __repr__(self):

        return (
            f"<WeeklySummary {self.week_commencing}>"
        )