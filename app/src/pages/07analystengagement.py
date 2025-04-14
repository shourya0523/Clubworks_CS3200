import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

# Configure the page
st.set_page_config(
    page_title="Engagement Tracker",
    page_icon="🔍",
    layout="wide"
)

st.title("Engagement Tracker")
st.write("View the percentage breakdown of events attended by category (Major or Graduation Year).")

# Fetch demographics data from the API endpoint
try:
    response = requests.get("http://api:4000/a/demographics_insights")
    response.raise_for_status()  # Raise an error if the response status isn't 200
    demo_data = response.json()
    st.write("**Raw API Data:**", demo_data)  # Debug: show raw API response
except Exception as e:
    st.error(f"Error fetching data: {e}")
    demo_data = []

if demo_data:
    # Convert the fetched data into a DataFrame.
    # The API is expected to return a list of dictionaries with keys:
    # 'EventsAttended', 'GraduationYear', and 'Major'.
    df = pd.DataFrame(demo_data)
    st.write("**DataFrame Preview:**", df.head())  # Debug: preview DataFrame

    # Check if the DataFrame has the expected columns.
    expected_columns = {"Major", "GraduationYear", "EventsAttended"}
    if expected_columns.issubset(df.columns):
        # If the DataFrame already has the proper keys, we can use it directly.
        df = df[list(expected_columns)]
    elif len(df.columns) == 3:
        # If only three columns exist, assume they are in the correct order.
        df.columns = ["Major", "GraduationYear", "EventsAttended"]
    else:
        st.error("Data format from API is not as expected:")
        st.write(df)
    
    # Convert the 'EventsAttended' column to numeric values.
    df["EventsAttended"] = pd.to_numeric(df["EventsAttended"], errors="coerce")
    st.write("**DataFrame After Numeric Conversion:**", df)  # Debug: show DataFrame after conversion

    # Let the user select the grouping category.
    category = st.selectbox("Select Category to View Engagement", ["Major", "GraduationYear"])

    # Group the data by the selected category and sum the events attended.
    chart_data = df.groupby(category)["EventsAttended"].sum().reset_index()
    st.write("**Aggregated Data:**", chart_data)  # Debug: display aggregated/grouped data

    # Filter out groups with 0 events attended
    chart_data = chart_data[chart_data["EventsAttended"] > 0]

    if not chart_data.empty:
        total_events = chart_data["EventsAttended"].sum()
        # Create a pie chart showing both the percentage share and the absolute count.
        fig, ax = plt.subplots()
        ax.pie(
            chart_data["EventsAttended"],
            labels=chart_data[category],
            autopct=lambda p: f'{p:.1f}%\n({int(p * total_events / 100)})',
            startangle=90
        )
        ax.axis("equal")  # Ensures the pie chart is drawn as a circle
        st.pyplot(fig)
    else:
        st.warning("⚠️ No valid data to display in pie chart after filtering.")
else:
    st.info("ℹ️ No engagement data found to generate the pie chart.")
