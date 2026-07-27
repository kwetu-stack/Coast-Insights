import os
import sqlite3
from pathlib import Path

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert


BASE_DIR = Path(__file__).resolve().parent
SQLITE_PATH = BASE_DIR / "instance" / "coast_insights.db"
TABLE_NAME = "trade_visits"


def railway_database_url():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is missing. Run this with: railway run python copy_trade_visits_to_railway.py"
        )
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    return database_url


def local_trade_visits():
    with sqlite3.connect(SQLITE_PATH) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            f'SELECT * FROM "{TABLE_NAME}" ORDER BY id'
        ).fetchall()
        return [dict(row) for row in rows]


def main():
    rows = local_trade_visits()
    if not rows:
        print("No local trade visits found.")
        return

    engine = sa.create_engine(railway_database_url())
    metadata = sa.MetaData()

    with engine.begin() as connection:
        before = connection.execute(
            sa.text(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        ).scalar_one()

        table = sa.Table(TABLE_NAME, metadata, autoload_with=connection)
        result = connection.execute(
            insert(table)
            .values(rows)
            .on_conflict_do_nothing(index_elements=["id"])
        )

        max_id = max(row["id"] for row in rows)
        connection.execute(
            sa.text(
                "SELECT setval(pg_get_serial_sequence(:table_name, 'id'), "
                f"GREATEST(:max_id, COALESCE((SELECT MAX(id) FROM {TABLE_NAME}), 1)))"
            ),
            {"table_name": TABLE_NAME, "max_id": max_id},
        )

        after = connection.execute(
            sa.text(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        ).scalar_one()

    print(f"Local trade visits: {len(rows)}")
    print(f"Railway trade visits before: {before}")
    print(f"Inserted into Railway: {result.rowcount}")
    print(f"Railway trade visits after: {after}")


if __name__ == "__main__":
    main()
