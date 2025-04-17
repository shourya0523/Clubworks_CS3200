import streamlit as st
import requests as re
import pandas as pd
from modules.nav import SideBarLinks
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Student Profile",
    page_icon="👤",
    layout="wide"
)

SideBarLinks("student")

BASE_URL = 'http://api:4000'

if 'nuid' in st.session_state:
    NUID = st.session_state['nuid']
else:
    st.switch_page('Home.py')

response = re.get(f'{BASE_URL}/s/get_student_profile/{NUID}')
if response.status_code == 200:
    student = response.json()[0]
    
    header_col1, header_col2 = st.columns([1, 3])
    
    with header_col1:
        if 'ImageLink' in student['ImageLink']:
            st.image(student['ImageLink'], width=200)
        else:
            st.image("https://pics.craiyon.com/2023-09-25/dc204a03135d4e4e9a395fbe99502814.webp", width=200)
    
    with header_col2:
        st.title(f"{student['FirstName']} {student['LastName']}")
        
        info_cols = st.columns(3)
        with info_cols[0]:
            st.write(f"**Major:** {student.get('Major', 'Not specified')}")
        with info_cols[1]:
            st.write(f"**Graduation:** {(student.get('GradDate'))}")
        with info_cols[2]:
            st.write(f"**Joined:** {(student.get('JoinDate'))}")
        
        st.write(f"**Email:** {student['Email']}")
        st.write(f"**NUID:** {student['NUID']}")
        
        profile_items = ['Major', 'AboutMe', 'ProfileIMG', 'Interests']
        completed_items = sum(1 for item in profile_items if student.get(item))
        completion_percentage = (completed_items / len(profile_items)) * 100
        
        st.progress(completion_percentage / 100, f"Profile Completion: {int(completion_percentage)}%")
    
    tab1, tab2, tab3, tab4 = st.tabs(["About", "Clubs & Activities", "Network", "Events"])
    
    with tab1:
        with st.container(border=True):
            st.subheader("About Me")
            if 'AboutMe' in student and student['AboutMe']:
                st.write(student['AboutMe'])
            else:
                st.info("No bio added yet. Edit your profile to add information about yourself.")
            
            st.subheader("Interests")
            if 'Interests' in student and student['Interests']:
                interests_list = [interest.strip() for interest in student['Interests'].split(',')]
                
                interests = ""
                for interest in interests_list:
                    interests += f" • {interest} "
                
                st.markdown(interests)
            else:
                st.info("No interests added yet.")
    
    with tab2:
        memberships_response = re.get(f'{BASE_URL}/s/memberships/{NUID}')
        
        if memberships_response.status_code == 200:
            memberships_data = memberships_response.json()
            
            st.subheader("Club Memberships")
            if memberships_data:
                for club in memberships_data:
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.subheader(club.get('ClubName', 'Unknown Club'))
                            if club.get('Description'):
                                st.write(club.get('Description'))
                        with col2:
                            if club.get('Position'):
                                st.info(f"Position: {club.get('Position')}")
                            else:
                                st.write("Member")
            else:
                st.info("You are not a member of any clubs yet.")
            
            st.subheader("Event Attendance")
            attendance_response = re.get(f'{BASE_URL}/s/attendance/{NUID}')
            
            if attendance_response.status_code == 200:
                attendance_data = attendance_response.json()
                
                if attendance_data:
                    club_attendance = {}
                    for event in attendance_data:
                        club_name = event.get('ClubName', 'Unknown')
                        club_attendance[club_name] = club_attendance.get(club_name, 0) + 1
                    
                    import plotly.express as px
                    attendance_df = pd.DataFrame({
                        'Club': list(club_attendance.keys()),
                        'Events Attended': list(club_attendance.values())
                    })
                    
                    fig = px.bar(
                        attendance_df, 
                        x='Club', 
                        y='Events Attended',
                        color='Events Attended',
                        color_continuous_scale = 'reds',
                        labels={'Club': 'Club Name', 'Events Attended': 'Number of Events'},
                        title='Events Attended by Club',
                        height=400
                    )
                    
                    fig.update_layout(
                        xaxis_title="Club",
                        yaxis_title="Number of Events",
                        coloraxis_showscale=False,
                        hoverlabel=dict(bgcolor="white", font_size=14)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    st.subheader("Recent Events Attended")
                    for event in attendance_data[:5]:  
                        event_time = event.get('StartTime', '')
                        formatted_time = event_time
                        st.write(f"• {event.get('Name')} ({event.get('ClubName')}) - {formatted_time}")
                else:
                    st.info("You haven't attended any events yet.")
    
    with tab3:
        follow_response = re.get(f'{BASE_URL}/s/followcount/{NUID}')
        follows_response = re.get(f'{BASE_URL}/s/follows/{NUID}')
        
        if follow_response.status_code == 200 and follows_response.status_code == 200:
            follow_data = follow_response.json()[0]
            follows_data = follows_response.json()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Followers", follow_data.get("Followers", 0))
            with col2:
                st.metric("Following", follow_data.get("Following", 0))
            
            follower_col, following_col = st.columns(2)
            
            with follower_col:
                with st.container(border=True):
                    st.subheader("Followers")
                    if "followers" in follows_data and follows_data["followers"]:
                        for follower in follows_data["followers"]:
                            st.write(f"• {follower}")
                    else:
                        st.write("You don't have any followers yet.")
            
            with following_col:
                with st.container(border=True):
                    st.subheader("Following")
                    if "following" in follows_data and follows_data["following"]:
                        for following in follows_data["following"]:
                            st.write(f"• {following}")
                    else:
                        st.write("You aren't following anyone yet.")
    
    with tab4:
        st.subheader("Upcoming Events")
        
        upcoming_events_response = re.get(f'{BASE_URL}/s/upcoming_events/{NUID}')
        
        if upcoming_events_response.status_code == 200:
            upcoming_events = upcoming_events_response.json()
            
            if upcoming_events:
                for event in upcoming_events:
                    with st.container(border=True):
                        event_col1, event_col2 = st.columns([3, 1])
                        with event_col1:
                            st.subheader(event.get('Name', 'Event Name'))
                            st.write(f"**Club:** {event.get('ClubName', 'Unknown Club')}")
                            st.write(f"**Location:** {event.get('Location', 'TBD')}")
                            st.write(f"**Time:** {event.get('StartTime')} - {event.get('EndTime')}")
                        with event_col2:
                            st.markdown(event.get('StartTime'))
            else:
                st.info("You don't have any upcoming events.")
        else:
            st.info("Could not load upcoming events.")
else:
    st.error("Could not load profile data")