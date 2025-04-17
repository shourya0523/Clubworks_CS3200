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
    st.header("Explore Programs")
    
    programs_response = requests.get(f"{BASE_URL}/s/programs")
    
    if programs_response.status_code == 200:
        programs_data = programs_response.json()
        
        if programs_data:
            programs_df = pd.DataFrame(programs_data)
            
            filtered_programs = filter_dataframe(programs_df, buttonkey='programs', exclude=['ProgramID', 'ClubID', 'ProgramDescription'])
            
            cols = st.columns(2)
            
            for i, (_, program) in enumerate(filtered_programs.iterrows()):
                with cols[i % 2]:
                    with st.container(border=True):
                        st.subheader(program['ProgramName'])
                        
                        if 'ClubName' in program:
                            st.caption(f"Offered by: {program['ClubName']}")
                        
                        if 'ProgramDescription' in program:
                            st.write(program['ProgramDescription'][:200] + "..." if len(program['ProgramDescription']) > 200 else program['ProgramDescription'])
                        
                        if 'ProgramID' in program:
                            app_response = requests.get(f"{BASE_URL}/s/program_applications/{program['ProgramID']}")
                            
                            if app_response.status_code == 200:
                                apps = app_response.json()
                                
                                if apps and len(apps) > 0:
                                    st.info(f"{len(apps)} open application(s) available")
                                    
                                    for app in apps:
                                        if 'Deadline' in app:
                                            deadline = pd.to_datetime(app['Deadline'])
                                            days_left = (deadline - datetime.datetime.now()).days
                                            
                                            if days_left > 0:
                                                st.write(f"Application deadline: {deadline.strftime('%B %d, %Y')} ({days_left} days left)")
                        
                        if 'InfoLink' in program and program['InfoLink']:
                            st.link_button("Learn More", program['InfoLink'], type="primary", use_container_width=True)
        else:
            st.info("No programs found.")
    else:
        st.error(f"Error fetching programs: {programs_response.status_code}")

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
                        
            filtered_events = filter_dataframe(events_df, buttonkey='events', exclude=['EventID', 'PosterLink', 'EventType', 'Location', 'FormattedStartTime', 'FormattedEndTime', 'StartTime', 'EndTime'])
            
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
        
    