import streamlit as st
import requests
from datetime import datetime, date

BASE_URL = 'http://api:4000'

if 'nuid' in st.session_state:
    nuid = st.session_state['nuid']
    response = requests.get(f'{BASE_URL}/pres/profile/{nuid}')
    response.raise_for_status()

    st.switch_page('Home.py')

st.set_page_config(page_title="Request Maker", layout="centered")
st.title("Submit Request")

tab_create, tab_edit = st.tabs(["Make Funding Request", "Make Support Request"])

# Function to fetch request types
def fetch_request_types():
    try:
        res = requests.get(f"{BASE_URL}/pres/request_types")
        if res.status_code == 200:
            return res.json()
        else:
            st.error("Could not load request types from server.")
            return []
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")
        return []

# TAB 1: Make Funding Request

with tab_create:
    st.subheader("Make Funding Request")
    with st.form("make_request_form"):
        description = st.text_input("Request Description")
        created_time = st.date_input("Created Date", value=date.today())

        request_type_list = fetch_request_types()
        request_type_labels = [t["RequestType"] for t in request_type_list]
        request_type = st.selectbox("Request Type", request_type_labels)

        executive_id = st.text_input("Executive ID")
        executive_club = st.text_input("Executive Club")
        executive_position = st.text_input("Executive Position")

        submit = st.form_submit_button("Submit Request")

        if submit:
            payload = {
                "RequestDescription": description,
                "CreatedTime": created_time.isoformat(),
                "Type": request_type,
                "ExecutiveID": executive_id,
                "ExecutiveClub": executive_club,
                "ExecutivePosition": executive_position
            }

            try:
                res = requests.put(f"{BASE_URL}/club_president/make_request", json=payload)
                if res.status_code == 200:
                    st.success("Request submitted successfully!")
                else:
                    st.error(f"Submission failed: {res.text}")
            except Exception as e:
                st.error(f"Failed to submit request: {e}")

# TAB 2: Make Support Requests

