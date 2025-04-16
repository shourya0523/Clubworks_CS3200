import streamlit as st
import requests
import pandas as pd

BASE_URL = 'http://api:4000'  

st.set_page_config(page_title="Club Management Dashboard", layout="wide")

st.title("Club Management Dashboard")


# To create the buttons for Create Event and Make Request
st.markdown("---")
st.subheader("Club Actions")

if st.button("➕ Create Event"):
    st.switch_page("pages/02.1_create_event.py")  


if st.button("➕ Make Request"):
    st.switch_page("make_request.py")

# Create Tabs
tab1, tab2, tab3 = st.tabs(["📅 Attendance", "📇 Members", "🗣️ Feedback"])

# ---------------------------
# TAB 1: Attendance Section
# ---------------------------
with tab1:
    st.subheader("Event Attendance")

    res = requests.get(f'{BASE_URL}/pres/attendance')
    df_attendance = pd.DataFrame(res.json())
    st.dataframe(df_attendance)


    st.subheader("Attendance by Event Type")
    try:
        res = requests.get(f'{BASE_URL}/pres/attendance_by_event_type')
        df_type = pd.DataFrame(res.json())
        st.dataframe(df_type)
    except:
        st.warning("Could not load attendance by event type.")


# ---------------------------
# TAB 2: Member Contacts
# ---------------------------
with tab2:
    st.subheader("Club Member Contact Info")
    try:
        res = requests.get(f'{BASE_URL}/pres/member_contact_information')
        df_contacts = pd.DataFrame(res.json())
        st.dataframe(df_contacts)
    except:
        st.warning("Could not load contact information.")

# ---------------------------
# TAB 3: Anonymous Feedback
# ---------------------------
with tab3:
    st.subheader("Anonymous Feedback")
    try:
        res = requests.get(f'{BASE_URL}/pres/obtain_anonamous_feedback')
        df_feedback = pd.DataFrame(res.json())
        st.dataframe(df_feedback)
    except:
        st.warning("Could not load feedback.")


