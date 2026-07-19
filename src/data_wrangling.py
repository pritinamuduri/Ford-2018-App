import pandas as pd
import glob
import os



# Define the path to raw data
raw_data_path = 'data/raw/*.csv'
all_files = glob.glob(raw_data_path)

dfs = []
for file in all_files:
    print(f"Loading {os.path.basename(file)}...")
    df = pd.read_csv(file) # You can add encoding='latin1' here if needed
    dfs.append(df)

# Combine into one master DataFrame
master_df = pd.concat(dfs, ignore_index=True)
print("Successfully loaded all files.")

# 2. Perform your conversion of Data Types
print("Converting data types....")
master_df['start_time'] = pd.to_datetime(master_df['start_time'])
master_df['end_time'] = pd.to_datetime(master_df['end_time'])

master_df['start_station_id'] = master_df['start_station_id'].astype(str)
master_df['end_station_id'] = master_df['end_station_id'].astype(str)
master_df['bike_id'] = master_df['bike_id'].astype(str)

# 3. Handle missing values (without dropping)

# 1. Calculate the median of the existing birth years
median_birth_year = master_df['member_birth_year'].median()
print(f"The median birth year is: {int(median_birth_year)}")

# 2. Fill the missing values with this median
master_df['member_birth_year'] = master_df['member_birth_year'].fillna(median_birth_year)

# 3. Convert to integer (years should be whole numbers, not floats like 1985.0)
master_df['member_birth_year'] = master_df['member_birth_year'].astype(int)

master_df['member_gender'] = master_df['member_gender'].fillna('Unknown')

# --- Further Data Wrangling ----

# 1. Create a 'duration_min' column for easier analysis
master_df['duration_min'] = master_df['duration_sec'] / 60

# 2. Create an 'age' column
# (Assuming the dataset is from 2018, as indicated by your file name)
master_df['age'] = 2018 - master_df['member_birth_year']

# 3. (Optional) Check the data to ensure new columns look correct
print(master_df[['duration_sec', 'duration_min', 'member_birth_year', 'age']].head())

def process_bike_data(df):
    # Perform Conversion
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end _time'] = pd.to_datetime(df['end_time'])
    print(df['end_time'].dtype)

    # NEW DEBUG STEP: Print the first 5 entries of the end_time column
    print("Checking first 5 entries of the end-time:")
    print(df['end_time'].head())


    # Extract the day name correctly
    df['day_of_week'] = df['end_time'].dt.day_name()
    # NEW DEBUG STEP
    print("Checking first 5 entries of day_of_week:")
    print(df['day_of_week'].head())


    return df

# Apply the processing funtion
master_df = process_bike_data(master_df) #  Removed the print() wrapper as discussed
master_df.to_csv('cleaned_bike_data.csv', index=False)
print("Data wrangling complete.")

# Final Check
master_df.info()

# Print a count of the days to see if irt is ONLY Wednesday
print(master_df['day_of_week'].value_count())

# Final Check
print(master_df.info())
print("Data wrangling complete.")

# Save the cleaned data to a new file
master_df.to_csv('data/processed/cleaned_fordgobike_2018.csv', index=False)
print("Cleaned data saved to data/processedcleaned_fordgobike_2018.csv")

# At the end of data_wrangling .py
# Make sure you are saving the DataFrame thast has the new column
master_df.to_csv('data/processed/cleaned_fordgobike_2018.csv', index=False)
print("Saved! Now the file includes day_of_week'.")

# 1. First, make sure your function is defined(as you have it)

# 2. Add these lines at the VERY BOTTOM of your file:
if __name__ == "__main__":
    # This block only runs if you execute the file directly

    # Run the processing function
    master_df = process_bike_data(master_df)

    # SAve the updated DataFrame
    master_df.to_csv('data/processed/cleaned_fordgobike_2018.csv', index=False)
    print("Processing complete and file saved with 'day_of_Week' column!")