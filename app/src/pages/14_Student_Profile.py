import streamlit as st
import requests as re
import pandas as pd
BASE_URL = 'http://api:4000'

if 'nuid' in st.session_state:
    NUID = st.session_state['nuid']
else:
    st.switch_page('Home.py')

response = re.get(f'{BASE_URL}/s/get_student_profile/{NUID}')
if response.status_code == 200:
    student = response.json()[0]
    
    st.title(f"{student['FirstName']} {student['LastName']}")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if 'ImageLink' in student and student['ImageLink']:
            st.image(student['ImageLink'])
    
    with col2:
        st.write(f"**Major:** {student['Major']}")
        st.write(f"**Email:** {student['Email']}")
        st.write(f"**NUID:** {student['NUID']}")
    
    if 'AboutMe' in student and student['AboutMe']:
        st.header("About Me")
        st.write(student['AboutMe'])
        st.write(f"**Interests:** {student['Interests']}")
    
    follow_response = re.get(f'{BASE_URL}/s/followcount/{NUID}')
    if follow_response.status_code == 200:
        follow_data = follow_response.json()[0]
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Followers", follow_data.get("Followers", 0))
        with col2:
            st.metric("Following", follow_data.get("Following", 0))
            
    follows_response = re.get(f'{BASE_URL}/s/follows/{NUID}')

if follows_response.status_code == 200:
    follows_data = follows_response.json()
    
    tab1, tab2 = st.tabs(["Followers", "Following"])
    
    with tab1:
        if "followers" in follows_data and follows_data["followers"]:
            st.write("People who follow you:")
            for follower in follows_data["followers"]:
                st.write(f"• {follower}")
        else:
            st.write("You don't have any followers yet.")
    
    with tab2:
        if "following" in follows_data and follows_data["following"]:
            st.write("People you follow:")
            for following in follows_data["following"]:
                st.write(f"• {following}")
        else:
            st.write("You aren't following anyone yet.")
else:
    st.error("Could not load profile data")