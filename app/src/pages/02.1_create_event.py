import streamlit as st
import requests
from datetime import datetime

BASE_URL = 'http://api:4000'


st.set_page_config(page_title="Create or Update Events", layout="centered")
st.title("📅 Manage Events")
tab_create, tab_edit = st.tabs(["Create Event", "Edit Event"])

if 'nuid' in st.session_state:
    nuid = st.session_state['nuid']
    # Make the GET request
    response = requests.get(f'{BASE_URL}/pres/profile/{nuid}')
    response.raise_for_status()
    
    # Parse the JSON response
    data = response.json()
    
    if data and isinstance(data, list) and len(data) > 0:
        CLUB_ID = data[0].get("ClubId")
        CLUB_NAME = data[0].get("ClubName")
        FIRST_NAME = data[0].get("FirstName")
        POSITIONS = data[0].get("Positions")
        
        # Display the extracted variables
        st.write("**Extracted Variables:**")
        st.write("Club ID:", CLUB_ID)
else:
    st.switch_page('Home.py')

def fetch_event_types():
    try:
        res = requests.get(f"{BASE_URL}/pres/event_types")
        if res.status_code == 200:
            return res.json()
        else:
            st.error("❌ Could not load event types from server.")
            return []
    except Exception as e:
        st.error(f"🚫 Failed to connect to backend: {e}")
        return []

# -------------------------
# TAB 1: Create Event
# -------------------------
with tab_create:
    st.subheader("Create a New Event")
    with st.form("create_event_form"):
        name = st.text_input("Event Name")
        location = st.text_input("Location")
        event_date = st.date_input("Event Date")
        start_time_input = st.time_input("Start Time")
        end_time_input = st.time_input("End Time")
        start_time = datetime.combine(event_date, start_time_input).isoformat()
        end_time = datetime.combine(event_date, end_time_input).isoformat()
        poster_img = st.text_input("Poster Image URL")
        event_type_list = fetch_event_types()
        event_type_labels = [t["EventType"] for t in event_type_list]
        event_type = st.selectbox("Event Type", event_type_labels)
        create_submit = st.form_submit_button("Create Event")
        if create_submit:
            payload = {
                "Name": name,
                "Location": location,
                "StartTime": str(start_time),
                "EndTime": str(end_time),
                "ClubID": CLUB_ID,
                "Type": event_type,
                "PosterImg": poster_img
            }

            try:
                response = requests.post(f"{BASE_URL}/pres/create_event", json=payload)
                if response.status_code == 200:
                    st.success("✅ Event created successfully!")
                else:
                    st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Failed to reach server: {e}")

# -------------------------
# TAB 2: Edit Event
# -------------------------



