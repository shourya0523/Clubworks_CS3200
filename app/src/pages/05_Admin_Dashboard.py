import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import altair as alt
from pyvis.network import Network
import streamlit.components.v1 as components

st.set_page_config(layout='wide')

BASE_URL = "http://api:4000/ad"

st.sidebar.title("Dashboard Navigation")
page = st.sidebar.radio("Go to...", ["System Health Dashboard", "API Health", "Issue Tracker"])

# SYSTEM HEALTH DASHBOARD PAGE
if page == "System Health Dashboard":
    st.title("Welcome to the Admin Dashboard, Connor!")
    st.subheader("System Health Dashboard 🩺 ")
    st.caption(f"Data last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        students_response = requests.get(f"{BASE_URL}/totalstudents")
        if students_response.status_code == 200:
            total_students = students_response.json()[0]["TotalStudents"]
        else:
            st.error(f"Failed to fetch total students: {students_response.status_code}")
    except Exception:
        st.error("Error fetching total students.")

    try:
        clubs_response = requests.get(f"{BASE_URL}/totalclubs")
        if clubs_response.status_code == 200:
            total_clubs = clubs_response.json()[0]["TotalClubs"]
        else:
            st.error(f"Failed to fetch total clubs: {clubs_response.status_code}")
    except Exception:
        st.error("Error fetching total clubs.")

    try:
        events_response = requests.get(f"{BASE_URL}/totalevents")
        if events_response.status_code == 200:
            total_events = events_response.json()[0]["TotalEvents"]
        else:
            st.error(f"Failed to fetch total events: {events_response.status_code}")
    except Exception:
        st.error("Error fetching total events.")

    try:
        past_month_response = requests.get(f"{BASE_URL}/pastmonth")
        if past_month_response.status_code == 200:
            events_past_month = past_month_response.json()[0]["RecentEvents"]
        else:
            st.error(f"Failed to fetch events past month: {past_month_response.status_code}")
    except Exception:
        st.error("Error fetching events past month.")

    st.markdown("### 🌐 Student–Club Engagement Network")

    try:
        res = requests.get(f"{BASE_URL}/engagementnetwork")
        if res.status_code == 200:
            data = res.json()
            nodes = data["nodes"]
            edges = data["edges"]

            net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
            net.force_atlas_2based()

            for node in nodes:
                color = "#FF7F50" if "@" not in node else "#87CEEB"
                net.add_node(node, label=node, color=color)

            for edge in edges:
                net.add_edge(edge["source"], edge["target"])

            net.save_graph("engagement_network.html")
            components.html(open("engagement_network.html", "r", encoding="utf-8").read(), height=620)

        else:
            st.error(f"Failed to fetch network data: {res.status_code}")
    except Exception as e:
        st.error(f"Error rendering network graph: {e}")


        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Total Students", value=total_students)
        col2.metric(label="Total Clubs", value=total_clubs)
        col3.metric(label="Total Events", value=total_events)
        col4.metric(label="Events This Month", value=events_past_month)

        st.markdown("### 🏆 Top 5 Most Attended Events")
        try:
            most_attended_response = requests.get(f"{BASE_URL}/mostattended")
            if most_attended_response.status_code == 200:
                most_attended = most_attended_response.json()
                if most_attended:
                    for idx, event in enumerate(most_attended, start=1):
                        st.write(f"{idx}. **{event['EventName']}** — {event['AttendanceCount']} attendees")
                else:
                    st.write("No data available for most attended events.")
            else:
                st.error(f"Failed to fetch most attended events: {most_attended_response.status_code}")
        except Exception:
            st.error("Error fetching most attended events.")

# API HEALTH PAGE
elif page == "API Health":
    st.switch_page('pages/12_API_Test.py')

# ISSUE TRACKER PAGE
elif page == "Issue Tracker":
    st.title("🛠️ Issue Tracker")
    st.caption(f"Data last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    st.markdown("### 👤 Students with Incomplete Profiles")
    try:
        profiles_response = requests.get(f"{BASE_URL}/studentsincomplete")
        if profiles_response.status_code == 200:
            incomplete_profiles = profiles_response.json()
            if isinstance(incomplete_profiles, dict):
                incomplete_profiles = [incomplete_profiles]
            if incomplete_profiles:
                df_profiles = pd.DataFrame(incomplete_profiles)
                st.dataframe(df_profiles)
            else:
                st.write("No students with incomplete profiles.")
        else:
            st.error(f"Failed to fetch incomplete profiles: {profiles_response.status_code}")
    except Exception:
        st.error("Error fetching incomplete profiles.")

    st.markdown("### 📋 Students with Incomplete Registrations (Last 7 Days)")
    try:
        registrations_response = requests.get(f"{BASE_URL}/incompleteregistrations")
        if registrations_response.status_code == 200:
            incomplete_registrations = registrations_response.json()
            if isinstance(incomplete_registrations, dict):
                incomplete_registrations = [incomplete_registrations]
            if incomplete_registrations:
                df_registrations = pd.DataFrame(incomplete_registrations)
                st.dataframe(df_registrations)
            else:
                st.write("No incomplete registrations in the last 7 days.")
        else:
            st.error(f"Failed to fetch incomplete registrations: {registrations_response.status_code}")
    except Exception:
        st.error("Error fetching incomplete registrations.")

    st.markdown("### 🏛️ Clubs with Incomplete Profiles")
    try:
        clubs_response = requests.get(f"{BASE_URL}/clubs")
        if clubs_response.status_code == 200:
            incomplete_clubs = clubs_response.json()
            if isinstance(incomplete_clubs, dict):
                incomplete_clubs = [incomplete_clubs]
            if incomplete_clubs and "Status" not in incomplete_clubs[0]:
                df_clubs = pd.DataFrame(incomplete_clubs)
                st.dataframe(df_clubs)
            else:
                st.write("No clubs with incomplete profiles.")
        else:
            st.error(f"Failed to fetch incomplete clubs: {clubs_response.status_code}")
    except Exception:
        st.error("Error fetching incomplete clubs.")

    st.markdown("### 📩 Support Requests")
    try:
        support_response = requests.get(f"{BASE_URL}/supportrequests")
        if support_response.status_code == 200:
            support_requests = support_response.json()
            if isinstance(support_requests, dict):
                support_requests = [support_requests]
            if support_requests:
                df_support = pd.DataFrame(support_requests)
                st.dataframe(df_support)
            else:
                st.write("No active support requests.")
        else:
            st.error(f"Failed to fetch support requests: {support_response.status_code}")
    except Exception:
        st.error("Error fetching support requests.")

    st.markdown("### 📈 User Sign-Ups Over Time")

    try:
        res = requests.get(f"{BASE_URL}/signupsbydate")
        if res.status_code == 200:
            signup_data = res.json()
            df_signups = pd.DataFrame(signup_data)

            if not df_signups.empty:
                df_signups["JoinDate"] = pd.to_datetime(df_signups["JoinDate"])

                line_chart = alt.Chart(df_signups).mark_line(point=True).encode(
                    x=alt.X("JoinDate:T", title="Join Date"),
                    y=alt.Y("StudentCount:Q", title="Sign-Ups"),
                    tooltip=["JoinDate", "StudentCount"]
                ).properties(
                    width=700,
                    height=400,
                    title="Daily Student Sign-Ups"
                )

                st.altair_chart(line_chart, use_container_width=True)
            else:
                st.info("No sign-up data available to display.")
        else:
            st.error(f"Failed to fetch sign-up history: {res.status_code}")
    except Exception:
        st.error("Error fetching user sign-up data.")