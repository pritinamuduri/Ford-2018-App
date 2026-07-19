import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

st.title("Data Exploration & Visualisation")

@st.cache_data
def load_data():
    file_id ='1gqU4G-UcC1UM185WxAbidXaT5XYFaLVx'
    output_path = 'cleaned_firdgobike_2018.csv'


   # gdown handles the security/virus warning automatically
    gdown.download(id=file_id, output=output_path, quiet=False)

    return pd.read_csv(output_path)

# Load the data
df = load_data()





# 2. Add Sidebars Filters
st.sidebar.header("Global Filters")

# Filter by User Type
user_type_filter = st.sidebar.multiselect(
    "Select User Type:",
    options=df['user_type'].unique(),
    default=df['user_type'].unique()
)

# Filter by Age Range
min_age = int(df['age'].min())
max_age = int(df['age'].max())
age_range = st.sidebar.slider(
    "Select Age Range:",
    min_age, max_age, (min_age, max_age)

)

# 3. Apply the filters to the dataframe
df = df[df['user_type'].isin(user_type_filter)]
df = df[(df['age'] >= age_range[0]) & (df['age'] <= age_range[1])]

# 4. Header Section
st.title ("Ford GoBike Data Dashboard")
st.markdown("""
This dashboard provides an interactive analysis of the Ford GoBike Trip data.
Use the sidebar to filter the datasetby user type and age, and explore
different paterns in the tabs below
""")  

# 5. Key Metrics Section
col1, col2, col3 = st.columns(3)
col1.metric("Total Trips", f"{len(df):,}")
col2.metric("Avg Duration (Min)", f"{round(df['duration_min'].mean(), 2)}")
col3.metric("Most Active Day", df['day_of_week'].mode()[0])
        





# Create the tabs
tab1, tab2, tab3 = st.tabs(["Univariable", "Bivariate", "Multivariate"])

with tab1:
    st.header("Univariable Exploration")
    st.write("This section examines indivdual variables to understand their distribution and central tendencies.")
    st.write("We will look at how metrics like user age, tripduration, and usage patterns appear on their own.")
    # ... your existing Univariate code ...

    st.markdown("---")

    # Dropdown to let the user select which variable to explore
    univariate_var = st.selectbox(
        "Select a variable to explore:",
        ["Trip Duration (Minutes)", "User Age", "Day of the Week"]
    )    

    if univariate_var == "Trip Duration (Minutes)":
        # Filter to <= 60 mins to avoid a heavily skewed chart caused by extreme outliers
        filtered_df = df[df['duration_min'] <= 60]
        fig = px.histogram(
            filtered_df,
            x="duration_min",
            nbins=30,
            title="Distribution of Trip Durations (Up to 60 Minutes)",
            labels={"duration_min": "Duration (Minutes)"},
            color_discrete_sequence=['#1f77b4']
        )
        st.plotly_chart(fig, use_container_width = True)

        st.markdown("** Observation:** The trip duration distribution is heavily right skewed, with most trips lasting under 20 minutes. A very small fraction of users take trips longer than one hour.")
        st.markdown("**Insight:** The service is primarily used for short, quick commutes rather than long-distance travel, suggesting it functions as a 'last-mile' solution.")
        st.markdown("**Recommendation:** Introduce weekend-exclusive 'Leisure Passes' to capture higher revenue from the longer-duration trips during peak weekend hours.")

    elif univariate_var == "User Age":
        # Plotting the age distribution
        fig = px.histogram(
            df,
            x="age",
        nbins=40,
        title="Distribution of User Ages",
        labels={"age": "Age (Years)"},
        color_discrete_sequence=['#ff7f0e'] 
        )   

        st.plotly_chart(fig, use_container_width=True)  

        st.markdown("**Observation:** The rider age distribution shows a high density of users between the ages of 25 and 40. There is a noticeable drop-off in ridership for users aged 50 and above.")
        st.markdown("**Insight:** The service heavily attracts younger professionals and urban workers, suggesting the marketing and bike design are best suited for this demographic.")
        st.markdown("**Recommendation:** Consider targeted campaigns or adjusted pricing for the older demographic to broaden the user base and increase total ridership numbers.")

    elif univariate_var == "Day of the Week":
        # Ensure days are in logical order , not alphabetical
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        # Count trips per day and reindex to the correct order
        day_counts = df['day_of_week'].value_counts().reindex(day_order).reset_index()
        day_counts.columns = ['Day of Week', 'Number of Trips']

        fig = px.bar(
            day_counts,
            x='Day of Week',
            y='Number of Trips',
            title="Total Trips by Day of the Week",
            color_discrete_sequence=['#2ca02c']
        )
        st.plotly_chart(fig, use_container_width=True)    

        st.markdown("**Observation:** Ridership is consistently higher on weekdays(Monday through Friday) compared to weekends, with a noticeable peak in the middle of the week. There is a distinct decline in activity on Saturdays and Sundays.")
        st.markdown("**Insight:** The usage pattern is strongly driven by work-week commuters, indicating that the bike-sharing service is primarily integrated into daily professional routines.")
        st.markdown("**Recommendation:** Shift promotional efforts for subscription renewals to the mid-week peak to capitalize on when the service is most central to the users' daily lives.")
         
        





        


    

with tab2:
    st.header("Bivariate Exploration")    
    st.write("This section explores the relationships between two different variables to uncover correlations.")
    st.write("We will investigate how factors like age and gender influence the duration of bike trips.")
    # ... paceholder for your Bivariate code ...
    st.markdown("---")

    # Selectbox for bivariate analysis
    bivariate_var = st.selectbox(
        "Select a relationship to explore:",
        ["Age vs. Trip Duration", "Day of the Week vs. Trip Duration", "Gender vs. Trip Duration"]
    )

    if bivariate_var == "Age vs. Trip Duration":
        # Using a sample because scatter plots with 1.8M points are too slow
        sampled_df = df.sample(1000)   
        fig = px.scatter(
            sampled_df,
            x="age",
            y="duration_min",
            title= "Age vs Trip Duration (Sampled 1,000 trips)",
            labels={"age": "Age (Years)", "duration_min": "Duration (Minutes)"},
            trendline="ols" # Adds a trendline to see the relationship clearly
        )        

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("** observation:** There is no strong linear correlation between age and trip duration, though the longesr trips are clustered among users in the 25-40 age bracket.")
        st.markdown("**Insight:** Trip duration is driven more by the purpose of the trip-such as commuting or recreation-rather than the physical endurance associated with  age.")
        st.markdown("**Recommendation:** Market bike-share features like e-bike assistance more hevily to older demographics to encourage longer, more comfortable trips.")


    elif bivariate_var == "Day of the Week vs. Trip Duration":
        fig = px.box(
            df[df['duration_min'] < 60],
            x="day_of_week",
            y="duration_min",
            category_orders={"day_of_week": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
            title="Trip Duration by Day of the Week (Under 60 Min)",
            labels={"day_of_week": "Day of the Week", "duration_min": "Duration (Minutes)"}
        )   
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("**Observation:** Subscriber activity remains remarkably stable across the work week but dips on weekends, whereas Customer activity shows a  relative increase on Saturdays and Sundays.")
        st.markdown("**Insight:** The service experiences a 'business-to-leisure' shift on weekends, indicating that the value proposition of the bike-share changes depending on the day.")
        st.markdown("**Recommendation:** Schedule station maintainance for weekends to minimize imopact on weekday commuters and ensure maximum bike availability during peak leisure times.")

    elif bivariate_var == "Gender vs. Trip Duration":
        fig = px.violin(
            df[df['duration_min'] < 60],
            x="member_gender",
            y="duration_min",
            box=True, # Shows quartiles

            points=False, # Hides individual points for cleaner look
            title="Trip Duration Distribution by Gender (Under 60 Min)",
            labels={"member_gender": "Gender", "duration_min": "Duration (Minutes)"}
        )

        st.plotly_chart(fig, use_container_width=True)  

        st.markdown("**Obseravtion:** While 'Customers' have a significantly higher median trip duration than 'Subscribers,' the 'Subscriber' group shows a much higher volume of short, consistent trips.")
        st.markdown("**Insight:** This confirms that Subscribers use the service as a habitual utility for quick transit, whereas Customers treat it as an ocassional, flexible service for longer rides.")
        st.markdown("**Recommendation:**Develop an 'Annual Commuter Pass' to reward the high-frequency, short-trip behavior of Subscribers, while keeping single-trip pricing competitive for Customers.")






        






        





          




with tab3:
    st.header("Multivariate Exploration")    
    st.write("This section analyzes interactions between three or more variables to reveal complex patterns.")
    st.write("We will see how uasge habits differ across demographics, days of the week, and trip types.")
    # ... placeholder for Multivariate code 

    st.markdown("---")

    # Selectbox for multivariate analysis
    multi_var = st.selectbox(
        "Select a multivariate view:",
        ["User Type, Day of Week & Trip Duration", "Gender, Day of Week & Trip Duration"]


    )

    if multi_var == "User Type, Day of Week & Trip Duration":
        fig = px.box(
            df[df['duration_min'] < 60],
            x="day_of_week",
            y="duration_min",
            color="user_type",
            category_orders={"day_of_week": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
            title="Trip Duration by Day and User Type (Under 60 Min)",
            labels={"day_of_week": "Day", "duration_min": "Duration (Min)", "user_type": "User Type"}
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("**Obseravtion:** The duration gap between 'Customers' and 'Subscribers' is most pronounced on weekends, where Customer trip lengths spike significantly compared to their weekday usage.")
        st.markdown("**Insight:** Weekends reveal a fundamental different use-case, where the service shifts from a logistical tool for commuters to a leisure-oriented activity for casual riders.")
        st.markdown("** Recommendation:** Design targeted weekend marketing campaignfor 'Customers' that promote specific leisure routes or sightseeing tours to maximize the value of these longer trips.")

    elif multi_var == "Gender, Day of Week & Trip Duration":
        fig = px.box(
            df[df['duration_min'] < 60],
            x="day_of_week",
            y="duration_min",
            color="member_gender",
            category_orders={"day_of_week": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]},
            title="Trip Duration by Day and Gender (Under 60 Min)",
            labels={"day_of_week": "Day", "duration_min": "Duration (Min)", "memver_gender": "Gender"}
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("** Observation:** While both genders show similar trends in trip frequency throughout the week, specific differences emerge in duration on weekends, where one group maintains higher consistency than the other.")
        st.markdown("**Insight:** These subtle variations indicate that external factors like weekend social planning or specific destination preferences may influence ride duration more than gender alone.")
        st.markdown("**Recommendation:** Conduct a survey focused on weekend destination preferences to understand the'why' behind these duration spikes and optimize station placement near high-leisure zones.")

        # Temporary debugging of the l;ines
        st.write("First few rows of data:")


print(df.columns.tolist())
        



        