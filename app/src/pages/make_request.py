import streamlit as st
import requests
from datetime import datetime

BASE_URL = 'http://api:4000'

if 'ClubID' in st.session_state:
    club_id = st.session_state['ClubID']
else:
    st.switch_page('Home.py')
st.set_page_config(page_title="Support Request Maker", layout="centered")
st.title(" Submit Request")

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
                "ClubID": club_id,
                "Type": event_type,
                "PosterImg": poster_img
            }

            try:
                response = requests.put(f"{BASE_URL}/pres/create_event", json=payload)
                if response.status_code == 200:
                    st.success("✅ Event created successfully!")
                else:
                    st.error(f"❌ Error: {response.text}")
            except Exception as e:
                st.error(f"❌ Failed to reach server: {e}")