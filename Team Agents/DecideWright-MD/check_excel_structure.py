import pandas as pd

# Read the Excel file to check all sheets
xl_file = pd.ExcelFile(r'C:\Users\AndrewSmart\DecideWright Ltd\Clients - General\TT\ARTT Risk Tool\TT Risk Data Import.xlsx')

print('='*80)
print('EXCEL FILE STRUCTURE')
print('='*80)
print(f'Sheet names: {xl_file.sheet_names}')

total_rows = 0
for sheet in xl_file.sheet_names:
    df = pd.read_excel(xl_file, sheet_name=sheet)
    print(f'\nSheet: {sheet}')
    print(f'  Rows: {len(df)}')
    print(f'  Columns: {df.columns.tolist()}')
    total_rows += len(df)

    if len(df) > 0:
        print(f'  First few rows:')
        print(df.head(3).to_string())

print(f'\n{'='*80}')
print(f'TOTAL ROWS ACROSS ALL SHEETS: {total_rows}')
print('='*80)
