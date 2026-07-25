from app import app

from services.sales_import_service import import_sales_workbook


WORKBOOK = "July sales/JULY SALES TRACKER.xlsx"


with app.app_context():

    result = import_sales_workbook(WORKBOOK)

    print("\n========== IMPORT COMPLETE ==========")
    print(f"Worksheets Processed : {result['worksheets_processed']}")
    print(f"Records Imported     : {result['records_imported']}")
    print(f"Records Skipped      : {result['records_skipped']}")