import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.express as px
from pyvis.network import Network
import streamlit.components.v1 as components
import os


st.set_page_config(layout='wide')

if 'role' in st.session_state:
    if st.session_state['role'] == 'coordinator' :
        NAME = st.session_state['first_name']
    else:
        st.switch_page('Home.py')
else:
    st.switch_page('Home.py')

st.title(f"Act as {NAME}, the Systems Coordinator")


BASE_URL = "http://api:4000/ad"

st.sidebar.title("Dashboard Navigation")
page = st.sidebar.radio("Go to...", ["System Health Dashboard", "API Health", "Issue Tracker"])

# SYSTEM HEALTH DASHBOARD PAGE
if page == "System Health Dashboard":
    st.title("📊 System Health Dashboard")
    st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("---")

    # 🧠 Section 1: Key Metrics
    st.subheader("📌 Platform Summary Metrics")
    col1, col2, col3, col4 = st.columns(4)

    try:
        students_response = requests.get(f"{BASE_URL}/totalstudents")
        total_students = students_response.json()[0]["TotalStudents"] if students_response.status_code == 200 else "N/A"
    except Exception:
        total_students = "N/A"

    try:
        clubs_response = requests.get(f"{BASE_URL}/totalclubs")
        total_clubs = clubs_response.json()[0]["TotalClubs"] if clubs_response.status_code == 200 else "N/A"
    except Exception:
        total_clubs = "N/A"

    try:
        events_response = requests.get(f"{BASE_URL}/totalevents")
        total_events = events_response.json()[0]["TotalEvents"] if events_response.status_code == 200 else "N/A"
    except Exception:
        total_events = "N/A"

    try:
        past_month_response = requests.get(f"{BASE_URL}/pastmonth")
        events_past_month = past_month_response.json()[0]["RecentEvents"] if past_month_response.status_code == 200 else "N/A"
    except Exception:
        events_past_month = "N/A"

    col1.metric("👥 Total Students", total_students)
    col2.metric("📚 Total Clubs", total_clubs)
    col3.metric("📅 Total Events", total_events)
    col4.metric("🗓️ Events This Month", events_past_month)

    st.markdown("---")

    # 🏆 Section 2: Top Event Engagement
    st.subheader("🏆 Most Attended Events")
    try:
        most_attended_response = requests.get(f"{BASE_URL}/mostattended")
        if most_attended_response.status_code == 200:
            most_attended = most_attended_response.json()
            if most_attended:
                for idx, event in enumerate(most_attended, start=1):
                    st.markdown(f"**{idx}. {event['EventName']}** — {event['AttendanceCount']} attendees")
            else:
                st.info("No attendance data available.")
        else:
            st.error("Failed to fetch most attended events.")
    except Exception:
        st.error("Error loading event attendance data.")

    st.markdown("---")

    # 📈 Section 3: Monthly Sign-Ups
    st.subheader("📈 Monthly Student Sign-Ups")
    try:
        res = requests.get(f"{BASE_URL}/signupsbydate")
        if res.status_code == 200:
            signup_data = res.json()
            df_signups = pd.DataFrame(signup_data)

            if not df_signups.empty:
                df_signups["JoinDate"] = pd.to_datetime(df_signups["JoinDate"])
                df_signups["Month"] = df_signups["JoinDate"].dt.to_period("M").dt.to_timestamp()
                monthly_signups = df_signups.groupby("Month")["StudentCount"].sum().reset_index()

                fig = px.line(
                    monthly_signups,
                    x="Month",
                    y="StudentCount",
                    markers=True,
                    labels={"Month": "Month", "StudentCount": "Sign-Ups"},
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No sign-up data available.")
        else:
            st.error(f"Failed to fetch sign-up history: {res.status_code}")
    except Exception as e:
        st.error(f"Error rendering monthly sign-up chart: {e}")

    st.markdown("---")

    # 🌐 Section 4: Network Graph
    st.subheader("🌐 Student–Club Engagement Network")
    try:
        response = requests.get(f"{BASE_URL}/engagementnetwork")
        if response.status_code == 200:
            data = response.json()
            nodes = data["nodes"]
            edges = data["edges"]

            net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
            net.force_atlas_2based()

            for node in nodes:
                color = "#6EC1E4" if "(" in node else "#F4A261"
                net.add_node(node, label=node, color=color)

            for edge in edges:
                edge_type = edge.get("type", "member")
                edge_color = "#DC143C" if edge_type == "executive" else "#D3D3D3"
                edge_label = "Executive" if edge_type == "executive" else "Member"
                net.add_edge(edge["source"], edge["target"], color=edge_color, title=edge_label)

            html_path = "/tmp/engagement_network.html"
            net.save_graph(html_path)
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            components.html(html_content, height=650)
        else:
            st.error(f"Failed to fetch engagement data: {response.status_code}")
    except Exception as e:
        st.error(f"Error rendering engagement graph: {e}")

# API HEALTH PAGE
elif page == "API Health":
    st.switch_page('pages/12_API_Test.py')

# ISSUE TRACKER PAGE
elif page == "Issue Tracker":
    st.title("🛠️ Issue Tracker Dashboard")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("---")

    # 🔎 Section 1: Student Registration Issues
    st.subheader("👤 Incomplete Student Data")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Students with Incomplete Profiles**")
        try:
            profiles_response = requests.get(f"{BASE_URL}/studentsincomplete")
            if profiles_response.status_code == 200:
                data = profiles_response.json()
                if isinstance(data, dict):
                    data = [data]
                if data:
                    st.dataframe(pd.DataFrame(data))
                else:
                    st.info("No students with incomplete profiles.")
            else:
                st.error(f"Failed to fetch: {profiles_response.status_code}")
        except Exception:
            st.error("Error loading profile data.")

    with col2:
        st.markdown("**Clubs with Incomplete Registrations (Last 7 Days)**")
        try:
            reg_response = requests.get(f"{BASE_URL}/incompleteregistrations")
            if reg_response.status_code == 200:
                data = reg_response.json()
                if isinstance(data, dict):
                    data = [data]
                if data:
                    st.dataframe(pd.DataFrame(data))
                else:
                    st.info("No recent incomplete registrations.")
            else:
                st.error(f"Failed to fetch: {reg_response.status_code}")
        except Exception:
            st.error("Error loading registration data.")

    st.markdown("---")

    # 🧩 Section 2: Support Insights
    st.subheader("📩 Support Requests Overview")

    try:
        support_response = requests.get(f"{BASE_URL}/supportrequests")
        if support_response.status_code == 200:
            support_data = support_response.json()
            if isinstance(support_data, dict):
                support_data = [support_data]
            if support_data:
                df_support = pd.DataFrame(support_data)

                st.markdown("**Raw Support Request Table**")
                st.dataframe(df_support)

                st.markdown("**🧁 Distribution by Type (Pie Chart)**")
                type_counts = df_support["SupportType"].value_counts().reset_index()
                type_counts.columns = ["Support Type", "Requests"]
                fig_pie = px.pie(type_counts, names="Support Type", values="Requests", hole=0.3)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.info("No support requests found.")
        else:
            st.error(f"Support API error: {support_response.status_code}")
    except Exception as e:
        st.error(f"Support data error: {e}")

    st.markdown("---")
