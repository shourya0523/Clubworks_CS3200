import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks
import pandas as pd

SideBarLinks()

st.write("# Testing All API Routes")

"""
Testing all API routes from the different modules. 
If the container isn't running, this will be very unhappy.
But the Streamlit app should not totally die.
"""

# Define base URL
BASE_URL = "http://api:4000"

# Tab structure for organizing tests
tab1, tab2, tab3 = st.tabs(["Club President", "Analyst", "Student"])

# --------------------------------------------------------
# Club President Route Tests
# --------------------------------------------------------
with tab1:
    st.header("Club President API Tests")
    
    # Test attendance endpoint
    st.subheader("Attendance Count")
    try:
        attendance = requests.get(f'{BASE_URL}/pres/attendance').json()
        st.dataframe(attendance)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve attendance data: {e}")
    
    # Test member contact information endpoint
    st.subheader("Member Contact Information")
    try:
        member_contacts = requests.get(f'{BASE_URL}/pres/member_contact_information').json()
        st.dataframe(member_contacts)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve member contact information: {e}")
    
    # Test anonymous feedback endpoint
    st.subheader("Anonymous Feedback")
    try:
        feedback = requests.get(f'{BASE_URL}/pres/obtain_anonamous_feedback').json()
        st.dataframe(feedback)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve anonymous feedback: {e}")
    
    # Test attendance by event type endpoint
    st.subheader("Attendance by Event Type")
    try:
        attendance_by_type = requests.get(f'{BASE_URL}/pres/attendance_by_event_type').json()
        st.dataframe(attendance_by_type)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve attendance by event type: {e}")
    
    # PUT request test UI elements
    st.subheader("Create Event (PUT Request Test)")
    with st.form("create_event_form"):
        event_name = st.text_input("Event Name", "Test Event")
        event_location = st.text_input("Location", "Test Location")
        event_id = st.text_input("Event ID", 1001)
        club_id = st.text_input("Club ID", 1)
        submitted = st.form_submit_button("Test Create Event")
        
        if submitted:
            try:
                import datetime
                test_event = {
                    "EventID": event_id,
                    "Name": event_name,
                    "Location": event_location,
                    "StartTime": (datetime.datetime.now() + datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S"),
                    "EndTime": (datetime.datetime.now() + datetime.timedelta(days=7, hours=2)).strftime("%Y-%m-%d %H:%M:%S"),
                    "ClubID": club_id,
                    "PosterImg": 1,
                    "Type": 1
                }
                response = requests.put(f'{BASE_URL}/pres/create_event', json=test_event)
                st.write(f"Response: {response.text}")
                st.write(f"Status code: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.subheader("Make Request (PUT Request Test)")
    with st.form("make_request_form"):
            request_id = st.text_input("Request ID", "2001")
            request_desc = st.text_input("Request Description", "Test Request")
            request_submitted = st.form_submit_button("Test Make Request")
            
            if request_submitted:
                try:
                    import datetime
                    test_request = {
                        "RequestID": request_id,
                        "RequestDescription": request_desc,
                        "Status": "1",
                        "CreatedTime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Type": "1",
                        "ExecutiveID": "123456789",
                        "ExecutiveClub": "1",
                        "ExecutivePosition": "President"
                    }
                    response = requests.put(f'{BASE_URL}/pres/make_request', json=test_request)
                    st.write(f"Response: {response.text}")
                    st.write(f"Status code: {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")

# --------------------------------------------------------
# Analyst Route Tests
# --------------------------------------------------------
with tab2:
    st.header("Analyst API Tests")
    
    # Test club performance endpoint
    st.subheader("Club Performance")
    try:
        performance = requests.get(f'{BASE_URL}/a/get_performance').json()
        st.dataframe(performance)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve club performance data: {e}")
    
    # Test demographics insights endpoint
    st.subheader("Demographics Insights")
    try:
        demographics = requests.get(f'{BASE_URL}/a/demographics_insights').json()
        st.dataframe(demographics)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve demographics insights: {e}")
    
    # Test active members endpoint
    st.subheader("Active Members")
    try:
        active_members = requests.get(f'{BASE_URL}/a/active_member').json()
        st.dataframe(active_members)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve active members data: {e}")
    
    # Test retention endpoint
    st.subheader("Club Retention Rate")
    try:
        retention = requests.get(f'{BASE_URL}/a/retention').json()
        st.dataframe(retention)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve retention rate data: {e}")
    
    # Test attendance by major endpoint
    st.subheader("Attendance by Major")
    try:
        attendance_major = requests.get(f'{BASE_URL}/a/attendance_major').json()
        st.dataframe(attendance_major)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve attendance by major data: {e}")
    
    # Test engagement by major endpoint
    st.subheader("Engagement by Major")
    try:
        engagement_major = requests.get(f'{BASE_URL}/a/engagement_major').json()
        st.dataframe(engagement_major)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve engagement by major data: {e}")
    
    # Test performance metrics endpoint
    st.subheader("Performance Metrics")
    try:
        metrics = requests.get(f'{BASE_URL}/a/performance_metrics').json()
        st.dataframe(metrics)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve performance metrics: {e}")
    
    # Test funding requests endpoint
    st.subheader("Funding Requests")
    try:
        funding = requests.get(f'{BASE_URL}/a/funding_requests').json()
        st.dataframe(funding)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve funding requests data: {e}")

# --------------------------------------------------------
# Student Route Tests
# --------------------------------------------------------
with tab3:
    st.header("Student API Tests")
    
    # Test open applications endpoint
    st.subheader("Open Applications")
    try:
        open_apps = requests.get(f'{BASE_URL}/s/open_apps').json()
        st.dataframe(open_apps)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve open applications: {e}")
    
    # Test student feedback endpoint
    st.subheader("Student Feedback")
    try:
        student_feedback = requests.get(f'{BASE_URL}/s/feedback').json()
        st.dataframe(student_feedback)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve student feedback: {e}")
    
    # Test follow count endpoint
    st.subheader("Follow Count")
    try:
        follow_count = requests.get(f'{BASE_URL}/s/followcount').json()
        st.dataframe(follow_count)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve follow count data: {e}")
    
    # Test follows endpoint
    st.subheader("Follows")
    try:
        follows = requests.get(f'{BASE_URL}/s/follows').json()
        st.dataframe(follows)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve follows data: {e}")
    
    # Test browse clubs endpoint
    st.subheader("Browse Clubs")
    try:
        clubs = requests.get(f'{BASE_URL}/s/browseclubs').json()
        st.dataframe(clubs)
    except Exception as e:
        st.write(f"Could not connect to database to retrieve clubs data: {e}")