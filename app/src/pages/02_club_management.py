import streamlit as st
import requests
import pandas as pd

BASE_URL = 'http://api:4000'  

st.set_page_config(page_title="Club Management Dashboard", layout="wide")


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

st.title("Club Management Dashboard")


st.markdown("---")
st.subheader("Club Actions")


if st.button("➕ Create Event"):
    st.switch_page("pages/02.1_create_event.py")  


if st.button("➕ Make Request"):
    st.switch_page("pages/make_request.py")

tab1, tab2, tab3, tab4 = st.tabs(["📅 Attendance", "📇 Members", "🗣️ Feedback", "📋 Programs & Applications"])

# TAB 1: Attendance Section
with tab1:
    st.subheader("Event Attendance")

    res = requests.get(f'{BASE_URL}/pres/attendance/{CLUB_ID}')
    try:
        df_attendance = pd.DataFrame(res.json())
        st.dataframe(df_attendance)
    except:
        st.write('No students yet!')
    st.subheader("Attendance by Event Type")
    
    try:
        res = requests.get(f'{BASE_URL}/pres/attendance_by_event_type/{CLUB_ID}')
        df_type = pd.DataFrame(res.json())
        st.dataframe(df_type)
    except:
        st.warning("Could not load attendance by event type.")


# TAB 2: Member Contacts
with tab2:
    st.subheader("Club Member Contact Info")

    res = requests.get(f'{BASE_URL}/pres/member_contact_information/{CLUB_ID}')
    df_members = pd.DataFrame(res.json())
    st.dataframe(df_members)

    try:
        res = requests.get(f'{BASE_URL}/pres/member_contact_information/{CLUB_ID}')
        df_contacts = pd.DataFrame(res.json())
        st.dataframe(df_contacts)
    except:
        st.warning("Could not load contact information.")

# TAB 3: Anonymous Feedback
with tab3:
    st.subheader("Anonymous Feedback")
    
    try:
        res = requests.get(f'{BASE_URL}/pres/obtain_anonamous_feedback/{CLUB_ID}')
        df_feedback = pd.DataFrame(res.json())
        st.dataframe(df_feedback)
    except:
        st.warning("Could not load feedback.")

print(st.session_state['nuid'])

# TAB 4: Programs & Applications

with tab4:
    st.subheader("Programs for Your Club")

    try:
        all_programs = requests.get(f'{BASE_URL}/pres/programs')
        programs_df = pd.DataFrame(all_programs.json())

        if not programs_df.empty:
            filtered_programs = programs_df[programs_df["ClubName"] == CLUB_NAME]
            st.dataframe(filtered_programs)
        else:
            st.info("No programs found.")
    except:
        st.warning("Could not load programs.")

    st.subheader("Applications & Applicants")

    try:
        all_apps = requests.get(f'{BASE_URL}/pres/program_applications')
        apps_df = pd.DataFrame(all_apps.json())

        if not apps_df.empty:
            filtered_apps = apps_df[apps_df["ClubName"] == CLUB_NAME]
            
            # Reorder columns to show applicant first
            display_columns = [
                "FirstName", "LastName", "Email", "NUID", 
                "ProgramName", "ApplicationName", 
                "ApplicationDescription", "Deadline", 
                "ApplyLink", "PostedDate", "StatusText"
            ]
            filtered_apps = filtered_apps[[col for col in display_columns if col in filtered_apps.columns]]
            st.dataframe(filtered_apps)
        else:
            st.info("No applications found.")
    except:
        st.warning("Could not load program applications.")
from modules.nav import SideBarLinks

# Add at beginning of file
SideBarLinks('president')
