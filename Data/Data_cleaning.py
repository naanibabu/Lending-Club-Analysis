 ##Import Liabraries
import pandas as pd
import numpy as np
import warnings

##To ignore warnings
warnings.filterwarnings('ignore')

file_name = 'Data/accepted_2007_to_2018Q4.csv'

features = ['id', 'loan_amnt', 'term', 'int_rate', 'installment', 
            'grade', 'sub_grade', 'emp_length', 'home_ownership', 'annual_inc',
            'verification_status', 'issue_d', 'loan_status', 'purpose',
            'fico_range_high', 'fico_range_low', 'dti', 
            'earliest_cr_line',  'open_acc', 'pub_rec', 'revol_bal', 'revol_util', 'total_acc',
            'application_type', 'mort_acc', 'pub_rec_bankruptcies' ]

###Load Data

if file_name:
    print(f"System mapped file successfully at: {file_name}")
    print("Loading dataset into memory... This may take a minute.")
    
    # Load the dataset efficiently by reading only the specified columns
    df = pd.read_csv(file_name, usecols=features, low_memory=True)
    
    print("\n Dataset loaded successfully!")
    print("-" * 50)
    
    # Display the shape of the dataframe and memory usage
    print(f"Total Rows: {df.shape[0]:,}")
    print(f"Total Columns: {df.shape[1]}")
    print("-" * 50)
    df.info()
else:
    print("ERROR: Could not locate the 'accepted' dataset in the Kaggle /input/ folder.")
    print("Please ensure the dataset is properly added to your notebook environment.")



# 1. Filter for completed loans only (Definitive outcomes)
print("Filtering for loans with a defined outcome...")
target_statuses = ['Fully Paid', 'Charged Off']
df = df[df['loan_status'].isin(target_statuses)]

# 2. Handle missing values in critical columns
# Only drop rows where CRITICAL columns are null
critical_cols = ['emp_length', 'dti', 'revol_util', 'annual_inc']

df.dropna(subset=critical_cols, inplace=True)

# 3. Data Type Conversions
print("Standardizing date formats...")
df['issue_d'] = pd.to_datetime(df['issue_d'])
df['earliest_cr_line'] = pd.to_datetime(df['earliest_cr_line'])

##Feature Engineering
df['avg_fico'] = (df['fico_range_high'] + df['fico_range_low'])/2
df.drop(columns=['fico_range_high', 'fico_range_low'], inplace=True)

# 4. Create a binary target column
# 0 = Fully Paid, 1 = Charged Off
df['default_flag'] = np.where(df['loan_status'] == 'Charged Off', 1, 0)

print("\nData Cleaning Completed Successfully.")
print("-" * 50)

# Display the final clean dataset size
print(f"Clean Dataset Total Rows: {df.shape[0]:,}")
print(f"Clean Dataset Total Columns: {df.shape[1]}")
print("-" * 50)

df.to_csv('cleaned_data.csv', index=False)

print("CSV file saved successfully!")





