import pandas as pd
import glob
import os

# Define the path to raw data
raw_data_path = 'data/raw/*.csv'
all_files = glob.glob(raw_data_path)

def load_and_clean_data(file_path):
    # skipfoter=0, header=1 skips the first "garbage" row
    # encoding='latin1' handles the special characters
    df = pd.read_csv(file_path, header=0, encoding='latin1')
    return df

# Create a list to hold the dataframes
dfs = []

# Loop through all files  and load them
for file in all_files:
    print(f"Loading {os.path.basename(file)}...")
    df = load_and_clean_data(file)
    dfs.append(df)

# Combine all into one master DataFrame
master_df = pd.concat(dfs, ignore_index=True)      

print(f"Successfuly loaded {len(all_files)} files.")
print(f"Total rows: {len(master_df)}")
print(master_df.head())
print(master_df.info())
print(master_df.dtypes)

# Check for missing values in every column
print("Missing values per column:")
print(master_df.isnull().sum())

print(f"Total missing values in dataset: {master_df.isnull().sum().sum()}")