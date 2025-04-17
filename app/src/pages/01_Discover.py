from narwhals import exclude
import streamlit as st
import pandas as pd
import requests
import datetime
from modules.filterframe import filter_dataframe

BASE_URL = "http://api:4000"

st.set_page_config(
    page_title="Discover",
    page_icon="🔍",
    layout="wide"
)

def rsvp_to_event(event_id):
    if 'nuid' in st.session_state:
        response = requests.post(
            f"{BASE_URL}/s/attend_event",
            json={
                'nuid': st.session_state['nuid'],
                'event_id': event_id
            }
        )

        if response.status_code == 201:
            st.success("Successfully RSVP'd to the event!")
        elif response.status_code == 200:
            st.info(response.json().get('message', 'You have already RSVP\'d to this event'))
        else:
            st.error(f"Error RSVP'ing to event: {response.text}")
    else:
        st.warning("Please log in to RSVP to events")

st.title("🔍 Discover")
st.write("Explore clubs, programs, and events at Northeastern")

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'student'
    st.session_state['first_name'] = 'Lucas'
    st.session_state['nuid'] = '123456789'

tab1, tab2, tab3 = st.tabs(["Clubs", "Programs", "Events"])

with tab1:
    st.header("Explore Clubs")
    
    clubs_response = requests.get(f"{BASE_URL}/s/clubs")
    
    if clubs_response.status_code == 200:
        clubs_data = clubs_response.json()
        
        if clubs_data:
            clubs_df = pd.DataFrame(clubs_data)
        
            if 'Rating' in clubs_df.columns:
                clubs_df['Rating'] = clubs_df['Rating']
            
            filtered_clubs = filter_dataframe(clubs_df,
                                              buttonkey='clubs',
                                              exclude=['ClubId',
                                                       'Complete',
                                                       'ImageLink',
                                                       'LinkTree',
                                                       'LogoLink',
                                                       'CalendarLink'])
            
            cols = st.columns(3)
            
            for i, (_, club) in enumerate(filtered_clubs.iterrows()):
                with cols[i % 3]:
                    with st.container(border=True):
                        if 'ImageLink' in club and club['ImageLink']:
                            st.image(club['ImageLink'], width=100)
                        else:
                            st.image("https://via.placeholder.com/100", width=100)
                            
                        st.subheader(club['ClubName'])
                        
                        if 'Description' in club and club['Description']:
                            st.write(club['Description'][:150] + "..." if len(club['Description']) > 150 else club['Description'])
                        
                        if 'Rating' in club and club['Rating']:
                            st.write(f"⭐ {club['Rating']}/5")
                        
                        if 'LinkTree' in club and club['LinkTree']:
                            st.link_button('LinkTree', club['LinkTree'])
                        
                        if 'CalendarLink' in club and club['CalendarLink']:
                            st.link_button('Calendar', club['CalendarLink'])
        else:
            st.info("No clubs found.")

with tab2:
    st.header("Explore Program Applications")
    st.write("Browse and filter open applications for club programs and opportunities.")


    openapps_response = requests.get(f"{BASE_URL}/s/open_apps")
    openapps_data = None 

    if openapps_response.status_code == 200:
        openapps_data = openapps_response.json()
    else:
        st.error(f"Error fetching applications: {openapps_response.status_code}")

    def add_app_to_apps(app_name):

        nuid = st.session_state['nuid']
        response = requests.post(
            f"{BASE_URL}/s/apply_to_app",
            json={
                'nuid': nuid,
                'application_name': app_name
            }
        )
        if response.status_code == 201:
            st.success(f"Successfully added '{app_name}' to your applications!")
            st.rerun()
        elif response.status_code == 200:
            st.info(response.json().get('message', f"You have already added '{app_name}'"))
        else:
            st.error(f"Error adding application: {response.text}")

    if openapps_data:
        apps_df = pd.DataFrame(openapps_data)

        if 'Deadline' in apps_df.columns:
            apps_df['Deadline'] = pd.to_datetime(apps_df['Deadline']) # Ensure it's datetime
            apps_df['FormattedDeadline'] = apps_df['Deadline'].dt.strftime('%B %d, %Y')
            apps_df['DaysLeft'] = (apps_df['Deadline'] - datetime.datetime.now()).dt.days
            apps_df = apps_df[apps_df['DaysLeft'] >= 0]

        filtered_apps = filter_dataframe(
            apps_df,
            buttonkey='program_apps',
            exclude=['ApplicationDescription', 'ApplyLink', 'FormattedDeadline', 'DaysLeft', 'Deadline'] # Exclude columns from filter UI
        )

        if not filtered_apps.empty:
            st.subheader("Open Applications")
            cols = st.columns(3) 

            for i, (_, app) in enumerate(filtered_apps.iterrows()):
                with cols[i % 3]:
                    with st.container(border=True):
                        st.subheader(app.get('NAME', 'N/A'))
                        st.caption(f"**Club:** {app.get('ClubName', 'N/A')}")

                        days_left = app.get('DaysLeft', -1)
                        deadline_str = app.get('FormattedDeadline', 'N/A')

                        if days_left >= 0:
                            if days_left > 10:
                                st.caption(f"Deadline: {deadline_str} (🟢 {days_left} days left)")
                            elif days_left > 3:
                                st.caption(f"Deadline: {deadline_str} (🟠 {days_left} days left)")
                            else:
                                st.caption(f"Deadline: {deadline_str} (🔴 {days_left} days left)")
                        else:
                             st.caption(f"Deadline: {deadline_str} (Past)")


                        if 'ApplicationDescription' in app and app['ApplicationDescription']:
                            st.write(app['ApplicationDescription'])

                        if 'Status' in app and app['Status']:
                            st.write(f"Status: {app['Status']}")

                        btn_cols = st.columns(2)
                        with btn_cols[0]:
                            if 'ApplyLink' in app and app['ApplyLink']:
                                st.link_button("Apply Now", app['ApplyLink'], use_container_width=True)
                        with btn_cols[1]:
                            st.button("Add to My Apps",
                                      on_click=add_app_to_apps,
                                      args=(app['NAME'],), 
                                      key=f"add_app_{app['NAME']}_{i}",
                                      use_container_width=True)
        else:
            st.info("No open applications match your filter criteria.")

    else:
        st.info("There are currently no open applications available.")

    st.markdown("---")
    st.subheader("Your Tracked Applications")

    if 'nuid' in st.session_state:
        student_apps_response = requests.get(f"{BASE_URL}/s/applications/{st.session_state['nuid']}")
        if student_apps_response.status_code == 200:
            student_apps = student_apps_response.json()
            if student_apps and len(student_apps) > 0:
                st.write("Here are the applications you are tracking:")
                for app in student_apps:
                    with st.expander(f"{app.get('application_name', 'Unknown Application')} ({app.get('club_name', 'Unknown Club')})"):
                        st.write(f"**Status:** {app.get('status', 'Pending')}")
                        if 'Deadline' in app:
                             deadline = pd.to_datetime(app['Deadline'])
                             st.write(f"**Deadline:** {deadline.strftime('%B %d, %Y')}")
                        if 'ApplyLink' in app and app['ApplyLink']:
                             st.link_button("Go to Application", app['ApplyLink'])

            else:
                st.info("You haven't added any applications to track yet. Use the 'Add to My Apps' button above.")
        else:
             st.error(f"Could not fetch your tracked applications (Error: {student_apps_response.status_code})")

    else:
        st.warning("Log in to see your tracked applications.")

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


with tab3:
    st.header("Events")
    
    events_response = requests.get(f"{BASE_URL}/s/events")
    
    if events_response.status_code == 200:
        events_data = events_response.json()
        
        if events_data:
            events_df = pd.DataFrame(events_data)
            
            if 'StartTime' in events_df.columns:
                events_df['StartTime'] = pd.to_datetime(events_df['StartTime'])
                events_df['FormattedStartTime'] = events_df['StartTime'].dt.strftime('%B %d, %Y - %I:%M %p')
            
            if 'EndTime' in events_df.columns:
                events_df['EndTime'] = pd.to_datetime(events_df['EndTime'])
                events_df['FormattedEndTime'] = events_df['EndTime'].dt.strftime('%I:%M %p')
            
            events_df['DaysUntil'] = (events_df['StartTime'] - datetime.datetime.now()).dt.days
                        
            filtered_events = filter_dataframe(events_df, buttonkey='events', exclude=['EventID', 'PosterLink', 'FormattedStartTime', 'FormattedEndTime'])
            
            for _, event in filtered_events.iterrows():
                with st.container(border=True):
                    cols = st.columns([3, 7])

                    with cols[0]:
                        if 'PosterLink' in event and event['PosterLink']:
                            st.image(event['PosterLink'], width=200)
                        else:
                            if 'ClubName' in event:
                                st.subheader(event['ClubName'])
                            st.caption("No event image available")

                    with cols[1]:
                        st.subheader(event['Name'])

                        if 'PosterLink' in event and event['PosterLink'] and 'ClubName' in event:
                             st.write(f"**Organized by:** {event['ClubName']}")
                        elif 'ClubName' not in event:
                             st.write(f"**Organized by:** Unknown")


                        if 'EventType' in event:
                            st.write(f"**Event Type:** {event['EventType']}")

                        if 'Location' in event:
                            st.write(f"**Location:** {event['Location']}")

                        if 'FormattedStartTime' in event and 'FormattedEndTime' in event:
                            st.write(f"**When:** {event['FormattedStartTime']} to {event['FormattedEndTime']}")

                        if 'EventID' in event:
                            st.button("RSVP to Event",
                                      key=f"event_{event['EventID']}",
                                      type="primary",
                                      on_click=lambda event_id=event['EventID']: rsvp_to_event(event_id))
        else:
            st.info("No upcoming events found.")
    else:
        st.error(f"Error fetching events: {events_response.status_code}")
        
    