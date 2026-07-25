import os
import sqlite3
from pathlib import Path

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert


BASE_DIR = Path(__file__).resolve().parent
SQLITE_PATH = BASE_DIR / "instance" / "coast_insights.db"
TABLES = ("users", "sales", "trade_visits")


def get_database_url():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not set.")
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    return database_url


def read_sqlite_rows(table_name):
    with sqlite3.connect(SQLITE_PATH) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(f'SELECT * FROM "{table_name}"').fetchall()
        return [dict(row) for row in rows]


def copy_table(connection, metadata, table_name):
    rows = read_sqlite_rows(table_name)
    if not rows:
        print(f"{table_name}: no rows to copy")
        return

    table = sa.Table(table_name, metadata, autoload_with=connection)
    statement = insert(table).values(rows).on_conflict_do_nothing(index_elements=["id"])
    result = connection.execute(statement)

    max_id = max(row["id"] for row in rows)
    connection.execute(
        sa.text(
            "SELECT setval(pg_get_serial_sequence(:table_name, 'id'), "
            "GREATEST(:max_id, COALESCE((SELECT MAX(id) FROM "
            f"{table_name}), 1)))"
        ),
        {"table_name": table_name, "max_id": max_id},
    )

    print(f"{table_name}: copied {result.rowcount} of {len(rows)} rows")


def main():
    if not SQLITE_PATH.exists():
        raise FileNotFoundError(f"SQLite database not found: {SQLITE_PATH}")

    engine = sa.create_engine(get_database_url())
    metadata = sa.MetaData()

    with engine.begin() as connection:
        for table_name in TABLES:
            copy_table(connection, metadata, table_name)


if __name__ == "__main__":
    main()
