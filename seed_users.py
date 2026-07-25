from app import create_app
from extensions import db
from models import User


app = create_app()


def seed_users():

    with app.app_context():

        # Prevent duplicates
        existing_admin = User.query.filter_by(username="admin").first()

        if existing_admin:
            print("Users already exist.")
            return

        admin = User(
            username="admin",
            display_name="System Administrator",
            role="admin",
            is_active=True
        )

        admin.set_password("admin123")

        executive = User(
            username="executive",
            display_name="Executive User",
            role="executive",
            is_active=True
        )

        executive.set_password("executive123")

        db.session.add(admin)
        db.session.add(executive)

        db.session.commit()

        print("Users created successfully.")
        print("Admin login: admin / admin123")
        print("Executive login: executive / executive123")


if __name__ == "__main__":
    seed_users()