import json
from datetime import date, datetime
from pathlib import Path

from app import app
from extensions import db
from models import TradeVisit


FIXTURE_PATH = Path(__file__).resolve().parent / "data" / "trade_visits.json"
DATE_FIELDS = ("visit_date", "follow_up_date")
DATETIME_FIELDS = ("created_at", "updated_at")


def parse_date(value):
    if not value:
        return None
    return date.fromisoformat(value)


def parse_datetime(value):
    if not value:
        return None
    return datetime.fromisoformat(value)


def load_trade_visits():
    if not FIXTURE_PATH.exists():
        raise FileNotFoundError(f"Trade visits fixture not found: {FIXTURE_PATH}")

    rows = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    existing_visits = TradeVisit.query.count()
    if existing_visits:
        print(
            f"Trade visit import skipped. Database already has {existing_visits} records."
        )
        return

    for row in rows:
        for field in DATE_FIELDS:
            row[field] = parse_date(row.get(field))
        for field in DATETIME_FIELDS:
            row[field] = parse_datetime(row.get(field))

        db.session.add(TradeVisit(**row))

    db.session.commit()
    print(f"Trade visits imported: {len(rows)}")


with app.app_context():
    load_trade_visits()
