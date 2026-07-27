from app import app

from extensions import db
from services.sales_import_service import import_sales_workbook
from models import Sale


WORKBOOK = "July sales/JULY SALES TRACKER.xlsx"


with app.app_context():

    existing_sales = Sale.query.count()

    print(f"Existing sales records: {existing_sales}")

    if existing_sales:

        print("Refreshing sales data from master workbook...")

        Sale.query.delete()

        db.session.commit()

        print("Existing sales deleted.")

    result = import_sales_workbook(WORKBOOK)

    print("\n========== IMPORT COMPLETE ==========")
    print(f"Worksheets Processed : {result['worksheets_processed']}")
    print(f"Records Imported     : {result['records_imported']}")
    print(f"Records Skipped      : {result['records_skipped']}")

    print(f"Database Total Sales : {Sale.query.count()}")