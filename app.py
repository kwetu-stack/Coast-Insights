from flask import Flask

from config import Config
from extensions import db, login_manager, migrate


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Temporary Home Route
    @app.route("/")
    def home():
        return """
        <h1>Coast Insights™</h1>
        <h3>Executive Sales Intelligence & Decision Support System</h3>
        <p>Checkpoint 3: Flask Foundation Running ✅</p>
        """

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)