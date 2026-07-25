import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE_DIR, exist_ok=True)


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "coast-insights-dev-key")

    database_url = os.environ.get("DATABASE_URL")
    if os.environ.get("RAILWAY_ENVIRONMENT") and not database_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Add a Railway PostgreSQL database and "
            "connect its DATABASE_URL variable to this service."
        )

    SQLALCHEMY_DATABASE_URI = database_url or (
        "sqlite:///" + os.path.join(INSTANCE_DIR, "coast_insights.db")
    )
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://", 1
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
