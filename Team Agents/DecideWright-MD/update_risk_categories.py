import pandas as pd

# Read all three files
risk_data = pd.read_excel(r'C:\Users\AndrewSmart\DecideWright Ltd\Clients - General\TT\ARTT Risk Tool\TT Risk Data Import.xlsx')
categories_df = pd.read_csv(r'C:\Users\AndrewSmart\DecideWright Ltd\Clients - General\TT\ARTT Risk Tool\Risk Categories.csv')
classifications_df = pd.read_csv(r'C:\Users\AndrewSmart\DecideWright Ltd\Clients - General\TT\ARTT Risk Tool\Risk Classification.csv')

print("Original Data:")
print(f"Rows: {len(risk_data)}")
print(f"\nCurrent Risk Categories:")
print(risk_data['Risk Category'].value_counts())

# Create mapping from old categories to new categories
category_mapping = {
    'Access Control': 'Technology & Cyber Risk',
    'Application Security': 'Technology & Cyber Risk',
    'Compliance': 'Governance Risk',
    'Cryptography': 'Technology & Cyber Risk',
    'Data Protection': 'Technology & Cyber Risk',
    'Human Resource': 'People Risk',
    'Network Security': 'Technology & Cyber Risk',
    'Operational Security': 'Process Risk',
    'Physical Security': 'Technology & Cyber Risk',
    'Third-Party': 'Third Party Risk'
}

# Update Risk Category based on mapping
risk_data['Risk Category'] = risk_data['Risk Category'].map(category_mapping)

# Add Risk Classification column if it doesn't exist, otherwise update it
# Since all risks reference ISO/IEC 27002:2022, classify them as ISO27001
if 'Risk Classification' not in risk_data.columns:
    risk_data['Risk Classification'] = 'ISO27001'
else:
    risk_data['Risk Classification'] = 'ISO27001'

print("\n" + "="*80)
print("Updated Data:")
print(f"\nNew Risk Categories:")
print(risk_data['Risk Category'].value_counts())
print(f"\nRisk Classifications:")
print(risk_data['Risk Classification'].value_counts())

# Save the updated file
output_path = r'C:\Users\AndrewSmart\DecideWright Ltd\Clients - General\TT\ARTT Risk Tool\TT Risk Data Import - Updated.xlsx'
risk_data.to_excel(output_path, index=False, engine='openpyxl')

print(f"\n✓ Updated file saved to: {output_path}")

# Show sample of updated data
print("\nSample of updated data (first 5 rows):")
print(risk_data[['Risk ID', 'Risk Category', 'Risk Classification', 'Risk Name']].head())
