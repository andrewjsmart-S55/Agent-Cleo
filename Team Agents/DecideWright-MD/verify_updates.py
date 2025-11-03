import pandas as pd

# Read the updated file
df = pd.read_excel(
    r'C:\Users\AndrewSmart\DecideWright Ltd\Clients - General\TT\ARTT Risk Tool\TT Risk Data Import - Updated_All_v20251029.xlsx',
    sheet_name='Standard Risks'
)

print('='*80)
print('VERIFICATION OF UPDATED FILE')
print('='*80)
print(f'Total risks: {len(df)}')
print(f'\nColumn names: {df.columns.tolist()}')

print(f'\n{"="*80}')
print('RISK CATEGORIES DISTRIBUTION')
print('='*80)
print(df['Risk Category'].value_counts())

print(f'\n{"="*80}')
print('RISK CLASSIFICATIONS DISTRIBUTION')
print('='*80)
print(df['Risk Classification'].value_counts(dropna=False))

print(f'\n{"="*80}')
print('SAMPLE RISKS BY CATEGORY')
print('='*80)

# Show samples for each category
for cat in df['Risk Category'].unique():
    print(f'\n{cat}:')
    sample = df[df['Risk Category']==cat][['Risk Name', 'Risk Classification']].head(3)
    for idx, row in sample.iterrows():
        classification = row['Risk Classification'] if pd.notna(row['Risk Classification']) else 'None'
        print(f'  - {row["Risk Name"][:80]}... | {classification}')

print(f'\n{"="*80}')
print('DETAILED BREAKDOWN BY CATEGORY AND CLASSIFICATION')
print('='*80)
breakdown = df.groupby(['Risk Category', 'Risk Classification']).size().reset_index(name='Count')
breakdown = breakdown.sort_values(['Risk Category', 'Count'], ascending=[True, False])
print(breakdown.to_string(index=False))
