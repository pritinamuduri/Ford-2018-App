import streamlit as st
import pandas as pd
import io
import gdown
import gdown



# 2. Cache the download function so it only downloads once
@st.cache_data
def load_data():
    file_id ='1gqU4G-UcC1UM185WxAbidXaT5XYFaLVx'
    output_path = 'cleaned_firdgobike_2018.csv'


   # gdown handles the security/virus warning automatically
    gdown.download(id=file_id, output=output_path, quiet=False)

  

    df = pd.read_csv(output_path)
    return df



st.title("📊 Data cleaning & Preparation")


with st.expander("View Full Data Cleaning Pipeline"):
    st.markdown("""
    ### 1. Data Type Conversions
    * **Timestamp Conversion**: `start_time` and `end_time` were converted to datetime objects for accurate time-series analysis.
    * **Identifier Conversion**: `start_station_id`, `end_station_id` and `bike_id`were converted to string format. Reason for converting start_station_id, end_station_id and bike_id into string format is that, in data science, IDs like (Station IDs, Bike IDs, Zip Codes, or Phine Numbers are stored as strings even if they llok like numbers. Because , there wil never be a need to add, subtract or find the mathematical average of two station IDs. Keeping them as integers can accidentally strip away leading zeros(e.g. 0123 becomes 123) or cause issues if a new bike ID is introdeced later that contains letters(like B102). So keeping them astype(str) is exactly what we have done here.

    ### 2. Missing Value Management
    * **Birth Year**: Missing values were filled with the median birth yearand converted to integers.
    * **Member Gender**: Missing values were labeled as 'Unknown' to maintain dataset completeness.

    ### 3. Feature Engineering
    * **Duration(Minutes)**: Created `duration_min` by dividing `duration_sec` by 60.
    * **Age Calculation**: Calculated missing `age` by subtracting `member_birth_year` from 2018.
    * **Temporal Extraction**: Extracted `day_of_week` from the `start_time` to enable weekend vs. weekday analysis.
    """)                                                                                  
                                    
    # Load the cleaned dataset
    df = load_data()

    

# ... code to get url

st.subheader("Cleaned Dataset Preview")
st.write("Below is a preview of the cleaned dataset of first 100 Rows.")
st.dataframe(df.head(100)) # Shows the first 100 rows for performance[span_5](start_span)[span_5](end_span)

csv_buffer = io.BytesIO()
df.to_csv(csv_buffer, index=False)
csv_data = csv_buffer.getvalue()

st.download_button(
    label="Download Cleaned CSV Data",
    data=csv_data,
    file_name="cleaned_fordgobike_2018.csv",
    mime='text/csv',
)    




        