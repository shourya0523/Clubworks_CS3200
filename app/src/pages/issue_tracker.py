import streamlit as st
import pandas as pd
import requests
from datetime import datetime
import plotly.express as px
from modules.nav import SideBarLinks

st.set_page_config(layout='wide')

SideBarLinks('admin')

# Authentication check
if 'authenticated' not in st.session_state:
    st.switch_page('Home.py')
if 'authenticated' in st.session_state:
    if st.session_state['authenticated'] == False:
        st.switch_page('Home.py')
if 'role' in st.session_state:
    if st.session_state['role'] == 'Coordinator':
        NAME = st.session_state['first_name']
    else:
        st.switch_page('Home.py')
else:
    st.switch_page('Home.py')

BASE_URL = "http://api:4000/ad"

# Navigation
st.sidebar.title("Dashboard Navigation")
page = st.sidebar.radio("Go to...", ["System Health Dashboard", "API Health", "Issue Tracker"])

# Route to appropriate page based on selection
if page == "System Health Dashboard":
    st.switch_page('pages/admin/system_health.py')
elif page == "API Health":
    st.switch_page('pages/12_API_Test.py')
elif page == "Issue Tracker":
    pass 

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