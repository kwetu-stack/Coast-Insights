from flask import Flask, redirect, url_for

from config import Config
from extensions import db, login_manager, migrate
from models import User
from blueprints.auth import auth_bp


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

    # Home Route
    @app.route("/")
    def home():
        return redirect(url_for("auth.login"))

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)