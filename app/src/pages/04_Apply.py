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
st.session_state['nuid'] = '123456789'



openapps = requests.get("http://api:4000/s/open_apps")

if openapps.status_code == 200:
    openapps = openapps.json()
else:
    st.error(f"Error fetching applications: {openapps.status_code}")

def add_app_to_apps(app_name, club_name, apply_link, deadline, description):
    
    nuid = st.session_state['nuid']
    
    response = requests.post(
        f"{BASE_URL}/s/apply_to_app",
        json={
            'nuid': nuid,
            'application_name': app_name
        }
    )
    if response.status_code == 201:
        st.success("Successfully added!")
    elif response.status_code == 200:
        st.info(response.json().get('message', 'You have already applied to this program'))
    else:
        st.error(f"Error adding applicationsr: {response.text}")
                        
if openapps:

    apps_df = pd.DataFrame(openapps)
    
    if 'Deadline' in apps_df.columns:
        apps_df['FormattedDeadline'] = pd.to_datetime(apps_df['Deadline']).dt.strftime('%B %d, %Y')
        apps_df['DaysLeft'] = (pd.to_datetime(apps_df['Deadline']) - datetime.datetime.now()).dt.days
    
    tab1, tab2 = st.tabs(["All Applications", "Applications by Club"])
    
    with tab1:
        st.subheader("Open Applications")
        
        cols = st.columns(3)
        
        for i, app in enumerate(openapps):
            with cols[i % 3]:
                with st.container(border=True):
                    st.subheader(app['NAME'])
                    st.caption(f"**Club:** {app['ClubName']}")
                    
                    deadline = pd.to_datetime(app['Deadline'])
                    days_left = (deadline - datetime.datetime.now()).days
                    
                    if days_left > 10:
                        st.caption(f"Deadline: {deadline.strftime('%B %d, %Y')} (🟢{days_left} days left)")
                    elif days_left > 3:
                        st.caption(f"Deadline: {deadline.strftime('%B %d, %Y')} (🟠 {days_left} days left)")
                    
                    if app['ApplicationDescription']:
                        st.write(app['ApplicationDescription'])
                    
                    if app['Status']:
                        st.write(app['Status'])
                    
                    if app['ApplyLink']:
                        st.link_button("Apply Now", app['ApplyLink'], type="primary",)
                        
                    st.button("Add to My Applications", 
                              on_click=add_app_to_apps, 
                              args=(app['NAME'],
                                    app['ClubName'],
                                    app['ApplyLink'],
                                    app['Deadline'],
                                    app['ApplicationDescription']),
                              type="primary",
                              key=f"add_app_{i}")
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

student_apps_response = requests.get(f"{BASE_URL}/s/applications/{st.session_state['nuid']}")


student_apps = student_apps_response.json()
if student_apps and len(student_apps) > 0:
    st.write("Here are your current applications:")
    for app in student_apps:
        with st.expander(app.get('application_name', 'Unknown Application')):
            st.write(f"**Club:** {app.get('club_name', 'Unknown Club')}")
            st.write(f"**Status:** {app.get('status', 'Pending')}")
else:
    st.info("You haven't applied to any programs yet. Browse the open applications above to get started!")
