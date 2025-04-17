import streamlit as st
import requests
from datetime import datetime, date

BASE_URL = 'http://api:4000'

st.set_page_config(page_title="Request Maker", layout="centered")

if 'nuid' in st.session_state:
    nuid = st.session_state['nuid']

    response = requests.get(f'{BASE_URL}/pres/profile/{nuid}')
    response.raise_for_status()
    
    data = response.json()
    
    if data and isinstance(data, list) and len(data) > 0:
        CLUB_ID = data[0].get("ClubId")
        CLUB_NAME = data[0].get("ClubName")
        FIRST_NAME = data[0].get("FirstName")
        POSITIONS = data[0].get("Positions")

else:
    st.switch_page('Home.py')

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

def fetch_support_request_types():
    try:
        res = requests.get(f"{BASE_URL}/pres/support_request_types")
        if res.status_code == 200:
            return res.json()
        else:
            st.error("Could not load support request types from server.")
            return []
    except Exception as e:
        st.error(f"Failed to connect to backend: {e}")
        return []

# TAB 2: Make Support Requests
with tab_edit:
    st.subheader("Make Support Request")
    with st.form("make_support_form"):
        description = st.text_input("Request Description")

        # Fetch support request types
        request_type_list = fetch_support_request_types()

        # Map label to ID
        request_type_map = {t["SupportType"]: t["SupportTypeID"] for t in request_type_list}
        request_type_label = st.selectbox("Request Type", list(request_type_map.keys()))

        submit = st.form_submit_button("Submit Request")

        if submit:
            payload = {
                "RequestDescription": description,
                "SupportTypeID": request_type_map[request_type_label]  # Send the ID to backend
            }
            try:
                res = requests.put(f"{BASE_URL}/club_president/make_support_request", json=payload)
                if res.status_code == 200:
                    st.success("Support request submitted successfully!")
                else:
                    st.error(f"Submission failed: {res.text}")
            except Exception as e:
                st.error(f"Failed to submit request: {e}")
