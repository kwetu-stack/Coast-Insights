import pandas as pd

workbook = pd.ExcelFile("July sales/JULY SALES TRACKER.xlsx")

for sheet in workbook.sheet_names:

    print(f"\n{'='*60}")
    print(sheet)
    print("="*60)

    df = pd.read_excel(workbook, sheet_name=sheet, nrows=5)

    print(df.columns.tolist())