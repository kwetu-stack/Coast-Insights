from app import app

from services.sales_import_service import import_sales_workbook
from models import Sale


WORKBOOK = "July sales/JULY SALES TRACKER.xlsx"


with app.app_context():
    existing_sales = Sale.query.count()

    if existing_sales:
        print(
            f"Sales import skipped. Database already has {existing_sales} sales records."
        )
        raise SystemExit(0)

    result = import_sales_workbook(WORKBOOK)

    print("\n========== IMPORT COMPLETE ==========")
    print(f"Worksheets Processed : {result['worksheets_processed']}")
    print(f"Records Imported     : {result['records_imported']}")
    print(f"Records Skipped      : {result['records_skipped']}")
