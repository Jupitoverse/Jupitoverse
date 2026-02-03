import pandas as pd
import glob

# Define file paths
master_file = r'C:\Users\abhisha3\Desktop\Projects\Excel\Master.xlsx'
child_files = glob.glob(r'C:\Users\abhisha3\Desktop\Projects\Excel\*.xlsx')

# Read child sheets
child_data = []
for file in child_files:
    if 'Master' not in file:
        df = pd.read_excel(file)
        df['Source'] = file.split('\\')[-1].split('.')[0]  # Add sheet holder name
        
        child_data.append(df)

# Combine child sheets into master sheet
master_df = pd.concat(child_data, ignore_index=True)

# Create primary key column
master_df['Primary Key'] = master_df['Date'] + '-' + master_df['Source']

# Save to master file
master_df.to_excel(master_file, index=False)

# Function to update child sheets from master
def update_child_sheets():
    master_df = pd.read_excel(master_file)
    for file in child_files:
        if 'Master' not in file:
            holder_name = file.split('\\')[-1].split('.')[0]
            child_df = master_df[master_df['Source'] == holder_name]
            child_df.to_excel(file, index=False)

# Call the function to update child sheets
update_child_sheets()