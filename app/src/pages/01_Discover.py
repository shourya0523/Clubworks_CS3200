from narwhals import exclude
import streamlit as st
import pandas as pd
import requests
import datetime
from modules.filterframe import filter_dataframe
import streamlit.components.v1 as components
import plotly.graph_objects as go

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

def follow_student_action(followee_nuid):
    if 'nuid' in st.session_state:
        follower_nuid = st.session_state['nuid']
        response = requests.post(
            f"{BASE_URL}/s/follow",
            json={
                'follower_nuid': follower_nuid,
                'followee_nuid': followee_nuid
            }
        )
        if response.status_code == 201:
            st.success("Successfully followed student=!")
        elif response.status_code == 400:
             st.warning(response.json().get('message', "Could not follow student"))


def show_feedback_dialog(club_id, club_name):
    """Fetches feedback and displays it in a dialog."""
    try:
        feedback_response = requests.get(f"{BASE_URL}/s/feedback/{club_id}")
        feedback_data = feedback_response.json()

        @st.dialog(f"Feedback for {club_name}")
        def display_feedback_content():
            """This function defines the content inside the dialog."""
            if feedback_data:
                st.write(f"Showing feedback for: **{club_name}**")
                st.divider()
                for feedback_item in feedback_data:
                    rating = feedback_item.get('Rating')
                    description = feedback_item.get('Description', 'No comment provided.')
                    if rating is not None:
                        st.write(f"Rating: {'⭐' * rating} ({rating}/5)")
                    else:
                        st.write("Rating: N/A")
                    st.caption(f"Comment: {description}")
                    st.divider()
            else:
                st.info("No feedback has been submitted for this club yet.")


        display_feedback_content()

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching feedback: {e}")
    except Exception as e:
        st.error(f"An error occurred while displaying feedback: {e}")
st.title("🔍 Discover")
st.write("Explore clubs, programs, and events at Northeastern")

tab_rec, tab1, tab2, tab3, tab4 = st.tabs(["⭐ Recommended", "Clubs", "Applications", "Events", "Students"])

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = True
    st.session_state['role'] = 'student'
    st.session_state['first_name'] = 'Lucas'
    st.session_state['nuid'] = '123456789'


with tab1:
    st.header("Explore Clubs")
    
    clubs_response = requests.get(f"{BASE_URL}/s/clubs")
    
    if clubs_response.status_code == 200:
        clubs_data = clubs_response.json()
        
        if clubs_data:
            clubs_df = pd.DataFrame(clubs_data)
        
            if 'Rating' in clubs_df.columns:
                 clubs_df['Rating'] = pd.to_numeric(clubs_df['Rating'], errors='coerce')

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
                        logo_url = club.get('LogoLink', "https://via.placeholder.com/100")
                        if not logo_url:
                            logo_url = "https://via.placeholder.com/100"
                        st.image(logo_url, width=100)

                        st.subheader(club.get('ClubName', 'N/A'))

                        description = club.get('Description', '')
                        if description:
                            st.write(description[:150] + "..." if len(description) > 150 else description)

                        rating_value = club.get('Rating')
                        club_id = club.get('ClubId')
                        club_name = club.get('ClubName', 'This Club')

                        if pd.notna(rating_value) and club_id is not None:
                            rating_display = f"⭐ {rating_value:.1f}/5"
                            st.button(rating_display,
                                      key=f"feedback_btn_{club_id}_{i}",
                                      on_click=show_feedback_dialog,
                                      args=(club_id, club_name),
                                      help=f"Click to see feedback for {club_name}")
                        else:
                            st.caption("No rating yet")

                        btn_cols = st.columns(2)
                        with btn_cols[0]:
                            if club.get('LinkTree'):
                                st.link_button('LinkTree', club['LinkTree'], use_container_width=True)
                        with btn_cols[1]:
                            if club.get('CalendarLink'):
                                st.link_button('Calendar', club['CalendarLink'], use_container_width=True)
        else:
            st.info("No clubs found matching criteria.")

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
            exclude=['ApplicationDescription', 'ApplyLink', 'FormattedDeadline']
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
                                st.link_button("Apply Now", app['ApplyLink'],
                                               use_container_width=True,
                                               type="primary")
                        with btn_cols[1]:
                            st.button("Add to My Apps",
                                      on_click=add_app_to_apps,
                                      args=(app['NAME'],), 
                                      key=f"add_app_{app['NAME']}_{i}",
                                      use_container_width=True,
                                      type="primary")
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
             
             filtered_events = filter_dataframe(
                                                events_df,
                                                buttonkey='events',
                                                exclude=['EventID',
                                                         'PosterLink',
                                                         'FormattedStartTime'
                                                         ,'FormattedEndTime'])
            
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

with tab4:
    st.header("Discover Students")
    st.write("Find and connect with other students.")

    if 'nuid' in st.session_state:
        current_nuid = st.session_state['nuid']
        students_response = requests.get(f"{BASE_URL}/s/all_students/{current_nuid}")
        students_data = None

        if students_response.status_code == 200:
            students_data = students_response.json()
        else:
            st.error(f"Error fetching students: {students_response.status_code}")

        if students_data:
            students_df = pd.DataFrame(students_data)

            filtered_students = filter_dataframe(
                students_df,
                buttonkey='students_filter',
                exclude=['NUID', 'Email']
            )

            if not filtered_students.empty:
                st.subheader("Students")
                cols = st.columns(3) 

                for i, (_, student) in enumerate(filtered_students.iterrows()):
                    with cols[i % 3]:
                        with st.container(border=True):
                            st.subheader(f"{student.get('FirstName', '')} {student.get('LastName', '')}")
                            if 'Email' in student and student['Email']: 
                                st.caption(student['Email'])
                            if 'Major' in student and student['Major']:
                                st.caption(f"Major: {student['Major']}")

                            followee_nuid = student.get('NUID')
                            if followee_nuid:
                                st.button("Follow",
                                          key=f"follow_{followee_nuid}_{i}",
                                          on_click=follow_student_action,
                                          args=(followee_nuid,),
                                          use_container_width=True,
                                          type="primary")
            else:
                st.info("No students match your filter criteria.")

        else:
            st.info("Could not load student data.")
  
with tab_rec:
    st.header("⭐ Recommended For You")
    st.write("Clubs and events tailored to your interests.")

    if 'nuid' in st.session_state:
        current_nuid = st.session_state['nuid']
        try:
            rec_response = requests.get(f"{BASE_URL}/s/recommendations/{current_nuid}")

            rec_data = rec_response.json()
            student_interest_names = set(rec_data.get('student_interest_names', []))
            recommended_clubs = rec_data.get('recommended_clubs', [])
            recommended_events = rec_data.get('recommended_events', [])

            if not recommended_clubs and not recommended_events:
                st.info("We couldn't find specific recommendations based on your current interests. Try adding more interests to your profile or explore the other tabs!")

            if recommended_clubs and student_interest_names:
                st.subheader("Interest Overlap")
                all_recommended_interests = set()
                for club in recommended_clubs:
                    all_recommended_interests.update(club.get('interest_names', []))

                interests_sorted = sorted(student_interest_names)
                clubs_sorted = [club.get('ClubName', 'N/A') for club in recommended_clubs]
                matrix = []
                for interest in interests_sorted:
                    row = []
                    for club in recommended_clubs:
                        club_interests = set(club.get('interest_names', []))
                        row.append(1 if interest in club_interests else 0)
                    matrix.append(row)

                fig = go.Figure(data=go.Heatmap(
                    z=matrix,
                    x=clubs_sorted,
                    y=interests_sorted,
                    colorscale='Reds',
                    showscale=False,
                    hovertemplate='Interest: %{y}<br>Club: %{x}<br>Shared: %{z}<extra></extra>'
                ))
                fig.update_layout(
                    title="Your Interests vs. Recommended Clubs",
                    xaxis_title="Recommended Club",
                    yaxis_title="Your Interest",
                    height=300 + 30*len(interests_sorted)
                )
                st.plotly_chart(fig, use_container_width=True)

                shared_interests = student_interest_names.intersection(all_recommended_interests)
                if shared_interests:
                    st.write("Interests shared with recommended clubs:")
                    st.write(f"`{', '.join(shared_interests)}`")
                st.divider()
            relevant_recommended_interests = all_recommended_interests.intersection(student_interest_names)


            if recommended_clubs:
                st.subheader("Recommended Clubs")
                rec_clubs_df = pd.DataFrame(recommended_clubs)
                if 'Rating' in rec_clubs_df.columns:
                    rec_clubs_df['Rating'] = pd.to_numeric(rec_clubs_df['Rating'], errors='coerce')

                cols_rec_clubs = st.columns(3)
                for i, (_, club) in enumerate(rec_clubs_df.iterrows()):
                     with cols_rec_clubs[i % 3]:
                        with st.container(border=True):
                            logo_url = club.get('LogoLink', "https://via.placeholder.com/100")
                            if not logo_url: logo_url = "https://via.placeholder.com/100"
                            st.image(logo_url, width=100)
                            st.subheader(club.get('ClubName', 'N/A'))
                            desc = club.get('Description', '')
                            if desc: st.write(desc[:150] + "..." if len(desc) > 150 else desc)

                            rating_value = club.get('Rating')
                            club_id = club.get('ClubId')
                            club_name = club.get('ClubName', 'This Club')
                            if pd.notna(rating_value) and club_id is not None:
                                rating_display = f"⭐ {rating_value:.1f}/5"
                                st.button(rating_display, key=f"rec_feedback_btn_{club_id}_{i}",
                                          on_click=show_feedback_dialog, args=(club_id, club_name),
                                          help=f"Click to see feedback for {club_name}")
                            else:
                                st.caption("No rating yet")

                            btn_cols_rec = st.columns(2)
                            with btn_cols_rec[0]:
                                if club.get('LinkTree'): st.link_button('LinkTree', club['LinkTree'], use_container_width=True)
                            with btn_cols_rec[1]:
                                if club.get('CalendarLink'): st.link_button('Calendar', club['CalendarLink'], use_container_width=True)
                st.divider() 

            if recommended_events:
                st.subheader("Recommended Events")
                rec_events_df = pd.DataFrame(recommended_events)
                if 'StartTime' in rec_events_df.columns:
                    rec_events_df['StartTime'] = pd.to_datetime(rec_events_df['StartTime'])
                    rec_events_df['FormattedStartTime'] = rec_events_df['StartTime'].dt.strftime('%b %d, %Y - %I:%M %p')
                if 'EndTime' in rec_events_df.columns:
                    rec_events_df['EndTime'] = pd.to_datetime(rec_events_df['EndTime'])
                    rec_events_df['FormattedEndTime'] = rec_events_df['EndTime'].dt.strftime('%I:%M %p')

                for _, event in rec_events_df.iterrows():
                    with st.container(border=True):
                        cols_rec_event = st.columns([3, 7])
                        with cols_rec_event[0]:
                            poster = event.get('PosterLink')
                            if poster: st.image(poster, width=200)
                            else: st.caption("No event image")
                        with cols_rec_event[1]:
                            st.subheader(event.get('Name', 'N/A'))
                            st.write(f"**Organized by:** {event.get('ClubName', 'N/A')}")
                            if event.get('EventType'): st.write(f"**Type:** {event.get('EventType')}")
                            if event.get('Location'): st.write(f"**Location:** {event.get('Location')}")
                            start_time = event.get('FormattedStartTime', 'N/A')
                            end_time = event.get('FormattedEndTime', '')
                            st.write(f"**When:** {start_time}{' to ' + end_time if end_time else ''}")
                            event_id = event.get('EventID')
                            if event_id:
                                st.button("RSVP", key=f"rec_event_{event_id}", type="primary",
                                          on_click=rsvp_to_event, args=(event_id,))
            else:
                 if recommended_clubs:
                     st.info("No upcoming events found from your recommended clubs.")


        except requests.exceptions.RequestException as e:
            st.error(f"Could not load recommendations: {e}")
