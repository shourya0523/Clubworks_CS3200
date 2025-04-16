from matplotlib.colors import BASE_COLORS
import streamlit as st
import requests
import pandas as pd
import datetime

BASE_URL = "http://api:4000"

st.set_page_config(
    page_title="Apply to Club Programs",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Apply to Club Programs")
st.write("Browse open applications for club programs and opportunities")

st.session_state['authenticated'] = True
st.session_state['role'] = 'club_executive'
st.session_state['first_name'] = 'Tyla'
st.session_state['nuid'] = '456789123'



openapps = requests.get("http://api:4000/s/open_apps")

if openapps.status_code == 200:
    openapps = openapps.json()
else:
    st.error(f"Error fetching applications: {response.status_code}")


if openapps:

    apps_df = pd.DataFrame(open_apps)
    
    if 'Deadline' in apps_df.columns:
        apps_df['FormattedDeadline'] = pd.to_datetime(apps_df['Deadline']).dt.strftime('%B %d, %Y')
        apps_df['DaysLeft'] = (pd.to_datetime(apps_df['Deadline']) - datetime.datetime.now()).dt.days
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["All Applications", "Applications by Club"])
    
    with tab1:
        # Display all applications in a card layout
        st.subheader("Open Applications")
        
        # Create a grid layout for cards
        cols = st.columns(3)
        
        for i, app in enumerate(open_apps):
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(app['NAME'])
                    st.caption(f"**Club:** {app['ClubName']}")
                    
                    # Show deadline with days remaining
                    deadline = pd.to_datetime(app['Deadline'])
                    days_left = (deadline - datetime.datetime.now()).days
                    
                    if days_left > 10:
                        st.caption(f"📅 Deadline: {deadline.strftime('%B %d, %Y')} ({days_left} days left)")
                    elif days_left > 3:
                        st.caption(f"📅 Deadline: {deadline.strftime('%B %d, %Y')} (🟠 {days_left} days left)")
                    else:
                        st.caption(f"📅 Deadline: {deadline.strftime('%B %d, %Y')} (🔴 {days_left} days left)")
                    
                    if app['ApplicationDescription']:
                        st.write(description)
                    
                    if app['ApplyLink']:
                        st.link_button("Apply Now", app['ApplyLink'], type="primary")
    
    with tab2:

        clubs = apps_df['ClubName'].unique()
        
        for club in clubs:
            st.subheader(club)
            club_apps = apps_df[apps_df['ClubName'] == club]
            
            for _, app in club_apps.iterrows():
                with st.expander(app['NAME']):
                    st.write(f"**Description:** {app['ApplicationDescription']}")
                    st.write(f"**Deadline:** {app['FormattedDeadline']} ({app['DaysLeft']} days remaining)")
                    
                    if app['ApplyLink']:
                        st.link_button("Apply Now", app['ApplyLink'], type="primary")
else:
    st.info("There are currently no open applications available. Please check back later.")

st.markdown("---")
st.markdown("### Tips for a Successful Application")
tips_col1, tips_col2 = st.columns(2)

with tips_col1:
    st.markdown("""
    - Be specific about why you want to join this particular club
    - Highlight relevant skills and experiences
    - Show enthusiasm and commitment
    - Proofread your application before submitting
    """)
    
with tips_col2:
    st.markdown("""
    - Research the club before applying
    - Be honest about your time commitment
    - Ask questions if you're unsure about anything
    - Follow up after submitting your application
    """)

st.markdown("---")
st.subheader("Your Applications")

# This would typically fetch from an API, but for now we'll use a placeholder
if "nuid" in st.session_state:
    # Function to get student applications (placeholder)
    def get_student_applications(nuid):
        # In a real implementation, this would call an API endpoint
        # For now, return an empty list
        return []
    
    student_apps = get_student_applications(st.session_state["nuid"])
    
    if student_apps:
        # Display student applications
        st.write("Here are your current applications:")
        # Display applications table
    else:
        st.info("You haven't applied to any programs yet. Browse the open applications above to get started!")
else:
    st.warning("Please log in to track your applications.")