from app import app
from extensions import db
from models.sale import Sale


with app.app_context():

    total = Sale.query.count()

    print(f"Sales records before delete: {total}")

    Sale.query.delete()

    db.session.commit()

    print("Sales table cleared successfully.")

    print(f"Sales records after delete: {Sale.query.count()}")