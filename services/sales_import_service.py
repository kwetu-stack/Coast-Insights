import pandas as pd

from extensions import db
from models import Sale


def import_sales_workbook(workbook_path):
    """
    Import all worksheets from the sales workbook.

    Expected columns:
        DATE
        CUSTOMER / CUSTOMERS
        CHANNEL
        LOCATION
        AMOUNT
    """

    workbook = pd.ExcelFile(workbook_path)

    worksheets_processed = 0
    records_imported = 0
    records_skipped = 0

    required_columns = [
        "DATE",
        "CUSTOMERS",
        "CHANNEL",
        "LOCATION",
        "AMOUNT",
    ]

    for sheet_name in workbook.sheet_names:

        print(f"\nProcessing worksheet: {sheet_name}")

        df = pd.read_excel(
            workbook,
            sheet_name=sheet_name
        )

        worksheets_processed += 1

        # ---------------------------------
        # Standardize column names
        # ---------------------------------

        df.columns = [
            str(col).strip().upper()
            for col in df.columns
        ]

        # Some worksheets use CUSTOMER instead of CUSTOMERS
        if "CUSTOMER" in df.columns and "CUSTOMERS" not in df.columns:
            df.rename(
                columns={
                    "CUSTOMER": "CUSTOMERS"
                },
                inplace=True
            )

        # ---------------------------------
        # Check required columns
        # ---------------------------------

        if not all(col in df.columns for col in required_columns):
            print(
                f"Skipping worksheet '{sheet_name}' (missing required columns)"
            )
            continue

        # ---------------------------------
        # Import rows
        # ---------------------------------

        for _, row in df.iterrows():

            try:

                # Customer
                if pd.isna(row["CUSTOMERS"]):
                    records_skipped += 1
                    continue

                customer_name = str(row["CUSTOMERS"]).strip()

                if customer_name == "":
                    records_skipped += 1
                    continue

                # Date
                if pd.isna(row["DATE"]):
                    records_skipped += 1
                    continue

                sale_date = pd.to_datetime(
                    row["DATE"],
                    errors="coerce"
                )

                if pd.isna(sale_date):
                    records_skipped += 1
                    continue

                # Amount
                if pd.isna(row["AMOUNT"]):
                    records_skipped += 1
                    continue

                amount = (
                    str(row["AMOUNT"])
                    .upper()
                    .replace(",", "")
                    .replace("/=", "")
                    .replace("/", "")
                    .replace("KSH", "")
                    .replace("KES", "")
                    .replace(" ", "")
                    .strip()
                )

                if amount == "":
                    records_skipped += 1
                    continue

                value = float(amount)

                # Channel
                channel = ""

                if not pd.isna(row["CHANNEL"]):
                    channel = str(row["CHANNEL"]).strip()

                # Location
                location = ""

                if not pd.isna(row["LOCATION"]):
                    location = str(row["LOCATION"]).strip()

                sale = Sale(
                    sale_date=sale_date.date(),
                    customer_name=customer_name,
                    channel=channel,
                    location=location,
                    value=value,
                )

                db.session.add(sale)

                records_imported += 1

            except Exception as e:

                print(
                    f"Skipped row in '{sheet_name}': {e}"
                )

                records_skipped += 1

    try:
        db.session.commit()

    except Exception as e:

        db.session.rollback()

        raise Exception(
            f"Database commit failed: {e}"
        )

    return {
        "worksheets_processed": worksheets_processed,
        "records_imported": records_imported,
        "records_skipped": records_skipped,
    }
