import pandas as pd

# Read all three files
risk_data = pd.read_excel(r'C:\Users\AndrewSmart\DecideWright Ltd\Clients - General\TT\ARTT Risk Tool\TT Risk Data Import.xlsx')
categories_df = pd.read_csv(r'C:\Users\AndrewSmart\DecideWright Ltd\Clients - General\TT\ARTT Risk Tool\Risk Categories.csv')
classifications_df = pd.read_csv(r'C:\Users\AndrewSmart\DecideWright Ltd\Clients - General\TT\ARTT Risk Tool\Risk Classification.csv')

print("="*80)
print("ORIGINAL DATA")
print("="*80)
print(f"Total rows: {len(risk_data)}")
print(f"\nOriginal Risk Categories:")
print(risk_data['Risk Category'].value_counts())

# Create intelligent mapping based on risk names and descriptions
# Risk Name -> (New Risk Category, Risk Classification or None)
risk_mappings = {
    'Unauthorized Access': ('Technology & Cyber Risk', 'ISO27001'),
    'Privilege Escalation': ('Technology & Cyber Risk', 'ISO27001'),
    'Cryptographic Failure': ('Technology & Cyber Risk', 'ISO27001'),
    'Key Compromise': ('Technology & Cyber Risk', 'ISO27001'),
    'Physical Breach': ('Technology & Cyber Risk', 'ISO27001'),
    'Environmental Damage': ('Process Risk', 'ISO27001'),
    'Configuration Error': ('Process Risk', 'ISO27001'),
    'Malware Infection': ('Technology & Cyber Risk', 'ISO27001'),
    'Network Intrusion': ('Technology & Cyber Risk', 'ISO27001'),
    'Man-in-the-Middle Attack': ('Technology & Cyber Risk', 'ISO27001'),
    'Application Vulnerability': ('Technology & Cyber Risk', 'ISO27001'),
    'Input Validation Failure': ('Technology & Cyber Risk', 'ISO27001'),
    'Data Leakage': ('Reputation Risk', 'Corporate Reputation'),
    'Data Loss': ('Technology & Cyber Risk', 'ISO27001'),
    'Vendor Compromise': ('Third Party Risk', 'Third Party Reputation'),
    'Cloud Service Failure': ('Third Party Risk', 'ISO27001'),
    'Insider Threat': ('People Risk', 'Employee Reputation'),
    'Social Engineering': ('People Risk', 'Employee Reputation'),
    'Regulatory Non-Compliance': ('Governance Risk', 'ISO27001'),
    'Privacy Violation': ('Reputation Risk', 'Customer Reputation')
}

# Apply mappings
def apply_mapping(row):
    risk_name = row['Risk Name']
    if risk_name in risk_mappings:
        category, classification = risk_mappings[risk_name]
        return pd.Series({
            'Risk Category': category,
            'Risk Classification': classification
        })
    else:
        # Keep original if not in mapping
        return pd.Series({
            'Risk Category': row['Risk Category'],
            'Risk Classification': None
        })

# Apply the mapping
risk_data[['Risk Category', 'Risk Classification']] = risk_data.apply(apply_mapping, axis=1)

print("\n" + "="*80)
print("UPDATED DATA")
print("="*80)
print(f"\nNew Risk Categories:")
print(risk_data['Risk Category'].value_counts())
print(f"\nRisk Classifications:")
print(risk_data['Risk Classification'].value_counts(dropna=False))

# Show detailed mapping for unique risks
print("\n" + "="*80)
print("DETAILED MAPPING (Unique Risks)")
print("="*80)
unique_risks = risk_data[['Risk Name', 'Risk Category', 'Risk Classification']].drop_duplicates('Risk Name')
print(unique_risks.to_string(index=False))

# Save the updated file
output_path = r'C:\Users\AndrewSmart\DecideWright Ltd\Clients - General\TT\ARTT Risk Tool\TT Risk Data Import - Updated.xlsx'
risk_data.to_excel(output_path, index=False, engine='openpyxl')

print(f"\n{'='*80}")
print(f"Updated file saved to:")
print(f"{output_path}")
print(f"{'='*80}")
