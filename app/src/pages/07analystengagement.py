import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd
from email.utils import parsedate_to_datetime

# Configure the page
st.set_page_config(
    page_title="Engagement Tracker",
    page_icon="🔍",
    layout="wide"
)

# Create two columns: left for the engagement chart, right for the Inbox
left_column, right_column = st.columns([2, 1])

### LEFT COLUMN: Engagement Pie Chart ###
with left_column:
    st.subheader("Engagement Breakdown by Category")
    try:
        response = requests.get("http://api:4000/a/demographics_insights")
        response.raise_for_status()
        demo_data = response.json()
    except Exception as e:
        st.error(f"Error fetching demographics data: {e}")
        demo_data = []

    if demo_data:
        # Convert the fetched data into a DataFrame.
        df = pd.DataFrame(demo_data)
        expected_columns = {"Major", "GraduationYear", "EventsAttended"}
        if expected_columns.issubset(df.columns):
            df = df[list(expected_columns)]
        elif len(df.columns) == 3:
            df.columns = ["Major", "GraduationYear", "EventsAttended"]
        else:
            st.error("Data format from demographics API is not as expected.")
            st.stop()

        df["EventsAttended"] = pd.to_numeric(df["EventsAttended"], errors="coerce")
        category = st.selectbox("Select Category to View Engagement", ["Major", "GraduationYear"])
        chart_data = df.groupby(category)["EventsAttended"].sum().reset_index()
        chart_data = chart_data[chart_data["EventsAttended"] > 0]

        if not chart_data.empty:
            total_events = chart_data["EventsAttended"].sum()

            # Helper function to format the pie chart labels.
            def make_autopct(total):
                def my_autopct(pct):
                    absolute = int(pct * total / 100)
                    return f"{pct:.1f}%\n({absolute})"
                return my_autopct

            # Reduce the size of the pie chart by specifying a smaller figsize.
            fig, ax = plt.subplots(figsize=(4, 4))
            ax.pie(
                chart_data["EventsAttended"],
                labels=chart_data[category],
                autopct=make_autopct(total_events),
                startangle=90
            )
            ax.axis("equal")  # Ensure the pie chart is drawn as a circle
            st.pyplot(fig)
        else:
            st.warning("⚠️ No valid data to display in the pie chart.")
    else:
        st.info("ℹ️ No engagement data found to generate the pie chart.")

### RIGHT COLUMN: Funding Requests Inbox ###
with right_column:
    st.title("Inbox")
    
    try:
        all_requests = requests.get("http://api:4000/a/funding_requests").json()
    except Exception as e:
        st.error(f"Error fetching funding requests: {e}")
        all_requests = []

    if all_requests:
        with st.expander("💰 Funding Requests", expanded=True):
            for req in all_requests:
                created_time = req.get("CreatedTime", "")
                try:
                    date = parsedate_to_datetime(created_time).strftime("%b %d, %Y")
                except Exception:
                    date = "Unknown date"
                
                st.write(f"**Request #{req['RequestID']} - {req['RequestType']}**")
                st.write(f"Club: **{req['ClubName']}**")
                st.write(f"Status: **{req['Status']}** | Created: {date}")
                st.divider()
    else:
        st.info("ℹ️ No funding requests found.")

### MIDDLE: Top 3 Clubs by Engagement ###
st.markdown("---")
st.subheader("Top 3 Clubs by Engagement 📊", anchor=False)

try:
    top_clubs = requests.get("http://api:4000/a/top_club").json()
except Exception as e:
    st.error(f"Error fetching top clubs: {e}")
    top_clubs = []

if top_clubs:
    top_df = pd.DataFrame(top_clubs)
    if {"ClubName", "TotalAttendance", "FeedbackCount"}.issubset(top_df.columns):
        st.dataframe(
            top_df.rename(columns={
                "ClubName": "Club",
                "TotalAttendance": "Total Attendees",
                "FeedbackCount": "Feedback Submitted"
            }),
            use_container_width=True
        )
    else:
        st.warning("⚠️ Unexpected data format from /a/top_club.")
else:
    st.info("ℹ️ No club engagement data found.")
