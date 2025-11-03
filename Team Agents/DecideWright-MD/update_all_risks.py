import pandas as pd

# Read the Standard Risks sheet
risk_data = pd.read_excel(
    r'C:\Users\AndrewSmart\DecideWright Ltd\Clients - General\TT\ARTT Risk Tool\TT Risk Data Import.xlsx',
    sheet_name='Standard Risks'
)

print('='*80)
print('ORIGINAL DATA - Standard Risks Sheet')
print('='*80)
print(f'Total risks: {len(risk_data)}')
print(f'\nOriginal Risk Categories:')
print(risk_data['Risk Categoy'].value_counts())
print(f'\nOriginal Risk Classifications:')
print(risk_data['Risk Classification'].value_counts(dropna=False))

# Category mapping: Old Category -> New Risk Category
category_mapping = {
    'Customer Value Proposition (CVP) Risks': 'Brand Risk',
    'Employee Value Proposition (EVP) Risk': 'Brand Risk',
    'Investor Value Proposition (IVP) Risk': 'Brand Risk',
    'Social Value Proposition (SVP) Risk': 'Brand Risk',
    'People Risk': 'People Risk',
    'Technology Risks': 'Technology & Cyber Risk',
    'Service Risks': 'Service Risk',
    'Initiative Management Risks': 'Change Management Risk',
    'Third-Party Risks': 'Third Party Risk',
    'Process Risks': 'Process Risk',
    'Values & Culture Risks': 'Culture Risk',
    'Results Risks': 'Annual Results Risk',
    'Product Risks': 'Innovation Risk',
    'Financial Risks - Cost': 'Financials Risk',
    'Financial Risks - Capital': 'Financials Risk',
    'Strategic Goal Risks': 'Strategic Goals Risk',
    'Stakeholders': 'Reputation Risk'
}

# Function to determine Risk Classification based on old category and risk name
def get_classification(row):
    old_category = row['Risk Categoy']
    risk_name = str(row['Risk Name']).lower()

    # CVP risks -> Customer Brand
    if old_category == 'Customer Value Proposition (CVP) Risks':
        if 'reputation' in risk_name or 'brand' in risk_name:
            return 'Customer Reputation'
        return 'Customer Brand'

    # EVP risks -> Employee Brand
    elif old_category == 'Employee Value Proposition (EVP) Risk':
        if 'reputation' in risk_name or 'brand' in risk_name:
            return 'Employee Reputation'
        return 'Employee Brand'

    # IVP risks -> Investor Brand
    elif old_category == 'Investor Value Proposition (IVP) Risk':
        if 'reputation' in risk_name or 'brand' in risk_name:
            return 'Investor Reputation'
        return 'Investor Brand'

    # SVP risks -> ESG Brand
    elif old_category == 'Social Value Proposition (SVP) Risk':
        if 'reputation' in risk_name or 'brand' in risk_name:
            return 'ESG Reputation'
        return 'ESG Brand'

    # People risks
    elif old_category == 'People Risk':
        if 'reputation' in risk_name or 'brand' in risk_name or 'culture' in risk_name:
            return 'Employee Reputation'
        return None

    # Third-Party risks
    elif old_category == 'Third-Party Risks':
        if 'reputation' in risk_name or 'brand' in risk_name:
            return 'Third Party Reputation'
        return None

    # Service risks
    elif old_category == 'Service Risks':
        if 'customer' in risk_name or 'reputation' in risk_name:
            return 'Customer Reputation'
        return None

    # Product risks
    elif old_category == 'Product Risks':
        if 'reputation' in risk_name or 'brand' in risk_name:
            return 'Customer Reputation'
        return 'Customer Brand'

    # Stakeholders
    elif old_category == 'Stakeholders':
        if 'customer' in risk_name:
            return 'Customer Reputation'
        elif 'employee' in risk_name:
            return 'Employee Reputation'
        elif 'investor' in risk_name:
            return 'Investor Reputation'
        elif 'third party' in risk_name or 'vendor' in risk_name or 'supplier' in risk_name:
            return 'Third Party Reputation'
        else:
            return 'Corporate Reputation'

    # Culture risks
    elif old_category == 'Values & Culture Risks':
        if 'reputation' in risk_name or 'brand' in risk_name:
            return 'Employee Reputation'
        return None

    # Default: no classification
    else:
        return None

# Apply mappings
risk_data['New Risk Category'] = risk_data['Risk Categoy'].map(category_mapping)
risk_data['New Risk Classification'] = risk_data.apply(get_classification, axis=1)

# Replace old columns with new ones
risk_data['Risk Category'] = risk_data['New Risk Category']
risk_data['Risk Classification'] = risk_data['New Risk Classification']

# Drop the temporary columns and the old misspelled column
risk_data = risk_data.drop(columns=['Risk Categoy', 'New Risk Category', 'New Risk Classification'])

print('\n' + '='*80)
print('UPDATED DATA')
print('='*80)
print(f'\nNew Risk Categories:')
print(risk_data['Risk Category'].value_counts())
print(f'\nNew Risk Classifications:')
print(risk_data['Risk Classification'].value_counts(dropna=False))

# Show detailed breakdown
print('\n' + '='*80)
print('CATEGORY & CLASSIFICATION BREAKDOWN')
print('='*80)
breakdown = risk_data.groupby(['Risk Category', 'Risk Classification']).size().reset_index(name='Count')
print(breakdown.to_string(index=False))

# Save the updated file
output_path = r'C:\Users\AndrewSmart\DecideWright Ltd\Clients - General\TT\ARTT Risk Tool\TT Risk Data Import - Updated_All_v20251029.xlsx'

# Read original file to preserve other sheets
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    # Write updated Standard Risks sheet
    risk_data.to_excel(writer, sheet_name='Standard Risks', index=False)

    # Copy other sheets from original file
    original_file = pd.ExcelFile(r'C:\Users\AndrewSmart\DecideWright Ltd\Clients - General\TT\ARTT Risk Tool\TT Risk Data Import.xlsx')
    for sheet in original_file.sheet_names:
        if sheet != 'Standard Risks':
            df = pd.read_excel(original_file, sheet_name=sheet)
            if len(df) > 0:  # Only write non-empty sheets
                df.to_excel(writer, sheet_name=sheet, index=False)

print(f'\n{'='*80}')
print(f'Updated file saved to:')
print(f'{output_path}')
print(f'{'='*80}')

# Show sample of updated data
print('\nSample of updated data (first 20 risks):')
print(risk_data[['Risk Name', 'Risk Category', 'Risk Classification']].head(20).to_string(index=False))
