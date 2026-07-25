from flask import Flask, redirect, url_for

from config import Config
from extensions import db, login_manager, migrate
from models import User
from blueprints.auth import auth_bp
from blueprints.dashboard import dashboard_bp
from blueprints.sales import sales_bp
from blueprints.trade_visits import trade_visits_bp


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(trade_visits_bp)

    # Home Route
    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)