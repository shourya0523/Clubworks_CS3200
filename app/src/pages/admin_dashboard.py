import streamlit as st
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

st.title(f"Act as {NAME}, the Systems Coordinator")

# Navigation
st.sidebar.title("Dashboard Navigation")
page = st.sidebar.radio("Go to...", ["System Health Dashboard", "API Health", "Issue Tracker"])

# Route to appropriate page based on selection
if page == "System Health Dashboard":
    st.switch_page('pages/system_health.py')
elif page == "API Health":
    st.switch_page('pages/12_API_Test.py')
elif page == "Issue Tracker":
    st.switch_page('pages/issue_tracker.py')
