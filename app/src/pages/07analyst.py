import streamlit as st
import requests
from modules.nav import SideBarLinks
from datetime import datetime

st.set_page_config(
    page_title="Club Search",
    page_icon="🔍",
    layout="wide"
)

st.title("Welcome to Club Search")
st.write('')

st.sidebar.title("Search Clubs")

if 'clubs' not in st.session_state:
    st.session_state.clubs = []
    try:
        clubs_response = requests.get("http://api:4000/a/get_clubs")
        if clubs_response.status_code == 200:
            results = clubs_response.json()
            st.session_state.clubs = [club["ClubName"] for club in results]
    except:
        pass

selected_club = st.sidebar.selectbox(
    "Search clubs",
    options=st.session_state.clubs,
    placeholder="Type to search clubs..."
)

if selected_club:
    st.header("Club Details")
    st.subheader(selected_club)
    
    try:
        clubs_data = requests.get("http://api:4000/a/get_clubs").json()
        selected_club_data = next((club for club in clubs_data if club["ClubName"] == selected_club), None)
        
        if selected_club_data:
            club_id = selected_club_data.get("ClubID")  # Get the club ID for member lookup
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                if "Description" in selected_club_data:
                    st.markdown(f"**Description:** {selected_club_data['Description']}")
                if "Category" in selected_club_data:
                    st.markdown(f"**Category:** {selected_club_data['Category']}")
                if "MeetingTimes" in selected_club_data:
                    st.markdown(f"**Meeting Times:** {selected_club_data['MeetingTimes']}")
                if "Location" in selected_club_data:
                    st.markdown(f"**Location:** {selected_club_data['Location']}")
            
            with col2:
                if "Website" in selected_club_data:
                    st.markdown(f"[Visit Website]({selected_club_data['Website']})")
                if "Email" in selected_club_data:
                    st.markdown(f"**Contact:** {selected_club_data['Email']}")
            
            # Add a section for active members
            st.subheader("Active Members")
            
            try:
                # Call the API to get active members for the selected club
                active_members_response = requests.get(f"http://api:4000/a/active_member?club_id={club_id}")
                
                if active_members_response.status_code == 200:
                    active_members = active_members_response.json()
                    
                    if active_members and len(active_members) > 0:
                        # Create a container with max height for the list
                        st.write("### Members List")
                        
                        # Use expander for scrollable list effect without custom CSS
                        with st.container():
                            # Calculate how many members to show per page
                            members_per_page = 10
                            total_members = len(active_members)
                            
                            # Add a scrollable area using st.container with fixed height
                            scroll_container = st.container(height=300)
                            
                            with scroll_container:
                                # Display each member in the scrollable container
                                for member in active_members:
                                    # Handle the API response format with FirstName and LastName
                                    first_name = member.get("FirstName", "")
                                    last_name = member.get("LastName", "")
                                    full_name = f"{first_name} {last_name}".strip()
                                    if not full_name:
                                        full_name = "Unknown"
                                    
                                    # Get events attended as the role/status
                                    events_attended = member.get("EventsAttended", 0)
                                    status = f"Attended {events_attended} event{'s' if events_attended != 1 else ''}"
                                    
                                    # Display member info with basic Streamlit formatting
                                    st.write(f"**{full_name}** - *{status}*")
                                    st.divider()  # Add a divider between members
                    else:
                        st.info("No active members found for this club.")
                else:
                    st.error("Failed to retrieve active members. Please try again later.")
            except Exception as e:
                st.error(f"Error fetching active members: {str(e)}")
            
            # Add a section for funding requests
            st.subheader("Funding Requests")
            
            try:
                # Call the API to get funding requests
                funding_response = requests.get(f"http://api:4000/a/funding_requests")
                
                if funding_response.status_code == 200:
                    all_funding_requests = funding_response.json()
                    
                    # Filter requests for the current club
                    club_funding_requests = [req for req in all_funding_requests if req.get("ClubName") == selected_club]
                    
                    if club_funding_requests and len(club_funding_requests) > 0:
                        st.write("### Funding Requests List")
                        
                        # Create a scrollable container for funding requests
                        funding_container = st.container(height=300)
                        
                        with funding_container:
                            for request in club_funding_requests:
                                # Extract relevant request information
                                request_id = request.get("RequestID", "Unknown")
                                request_type = request.get("RequestType", "Unknown")
                                status = request.get("Status", "Pending")
                                created_time = request.get("CreatedTime", "Unknown")
                                event_attendance = request.get("EventAttendance", 0)
                                avg_rating = request.get("AvgClubRating", 0)
                                
                                # Format the rating with 1 decimal place if available
                                if avg_rating is not None:
                                    try:
                                        # Convert to float if it's a string
                                        avg_rating_float = float(avg_rating)
                                        rating_display = f"{avg_rating_float:.1f}/5.0"
                                    except (ValueError, TypeError):
                                        # If conversion fails, just display as is
                                        rating_display = f"{avg_rating}/5.0"
                                else:
                                    rating_display = "No ratings"
                                
                                # Format created time if it's a datetime string
                                try:
                                    # Parse the datetime (assuming ISO format)
                                    date_obj = datetime.fromisoformat(created_time.replace('Z', '+00:00'))
                                    formatted_date = date_obj.strftime("%b %d, %Y")
                                except:
                                    formatted_date = created_time
                                
                                # Display request with relevant details
                                st.write(f"**Request #{request_id} - {request_type}**")
                                st.write(f"Status: **{status}** | Created: {formatted_date}")
                                st.write(f"Event Attendance: {event_attendance} | Club Rating: {rating_display}")
                                st.divider()
                    else:
                        st.info("No funding requests found for this club.")
                else:
                    st.error("Failed to retrieve funding requests. Please try again later.")
            except Exception as e:
                st.error(f"Error fetching funding requests: {str(e)}")
                
            # Add a comprehensive engagement information section
            st.subheader("Engagement Information")
            
            # Create tabs for different metrics
            metrics_tab, retention_tab, major_tab = st.tabs(["Performance Metrics", "Retention Rate", "Engagement by Major"])
            
            with metrics_tab:
                try:
                    # Get performance metrics
                    performance_response = requests.get("http://api:4000/a/performance_metrics")
                    
                    if performance_response.status_code == 200:
                        performance_data = performance_response.json()
                        
                        # Filter for current club
                        club_performance = next((p for p in performance_data if p.get("ClubName") == selected_club), None)
                        
                        if club_performance:
                            # Create metrics display
                            col1, col2, col3 = st.columns(3)
                            
                            # Extract and format metrics
                            total_attendance = club_performance.get("TotalAttendance", 0)
                            avg_rating = club_performance.get("AvgRating", 0)
                            funding_requests = club_performance.get("FundingRequests", 0)
                            
                            # Format rating
                            try:
                                avg_rating_float = float(avg_rating) if avg_rating else 0
                                rating_display = f"{avg_rating_float:.1f}/5.0"
                            except (ValueError, TypeError):
                                rating_display = "N/A"
                            
                            # Display metrics
                            with col1:
                                st.metric("Total Attendance", total_attendance)
                            
                            with col2:
                                st.metric("Average Rating", rating_display)
                            
                            with col3:
                                st.metric("Funding Requests", funding_requests)
                            
                            # Get club performance data
                            performance_by_event_response = requests.get("http://api:4000/a/get_performance")
                            
                            if performance_by_event_response.status_code == 200:
                                performance_by_event = performance_by_event_response.json()
                                
                                # Filter for current club
                                club_event_data = [p for p in performance_by_event if p.get("ClubName") == selected_club]
                                
                                if club_event_data:
                                    st.write("### Attendance by Event Type and Interest")
                                    
                                    # Create a scrollable container
                                    event_container = st.container(height=250)
                                    
                                    with event_container:
                                        # Group by event type
                                        event_types = {}
                                        for item in club_event_data:
                                            event_type = item.get("EventType", "Unknown")
                                            interest = item.get("InterestName", "General")
                                            attendance = item.get("TotalAttendance", 0)
                                            
                                            if event_type not in event_types:
                                                event_types[event_type] = []
                                            
                                            event_types[event_type].append({
                                                "interest": interest,
                                                "attendance": attendance
                                            })
                                        
                                        # Display by event type
                                        for event_type, interests in event_types.items():
                                            st.write(f"**{event_type} Events**")
                                            
                                            for interest_data in interests:
                                                interest = interest_data["interest"] or "General Interest"
                                                attendance = interest_data["attendance"]
                                                st.write(f"- {interest}: {attendance} attendees")
                                            
                                            st.divider()
                                else:
                                    st.info("No event performance data available for this club.")
                            else:
                                st.error("Failed to retrieve event performance data.")
                        else:
                            st.info("No performance metrics available for this club.")
                    else:
                        st.error("Failed to retrieve performance metrics.")
                except Exception as e:
                    st.error(f"Error fetching performance metrics: {str(e)}")
            
            with retention_tab:
                try:
                    # Get retention data
                    retention_response = requests.get("http://api:4000/a/retention")
                    
                    if retention_response.status_code == 200:
                        retention_data = retention_response.json()
                        
                        # Filter for current club
                        club_retention = next((r for r in retention_data if r.get("ClubName") == selected_club), None)
                        
                        if club_retention:
                            # Extract retention metrics
                            total_members = club_retention.get("TotalMembers", 0)
                            active_participants = club_retention.get("ActiveParticipants", 0)
                            retention_rate = club_retention.get("RetentionRate", 0)
                            
                            # Format retention rate
                            try:
                                retention_rate_float = float(retention_rate) if retention_rate else 0
                                retention_display = f"{retention_rate_float:.1f}%"
                            except (ValueError, TypeError):
                                retention_display = "N/A"
                            
                            # Display metrics
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.metric("Total Members", total_members)
                            
                            with col2:
                                st.metric("Active Participants", active_participants)
                            
                            with col3:
                                st.metric("Retention Rate", retention_display)
                            
                            # Calculate inactive members
                            inactive_members = int(total_members) - int(active_participants)
                            
                            # Display member breakdown
                            st.write("### Member Participation Breakdown")
                            
                            # Create a simple horizontal bar for visualization
                            total_width = 100
                            active_width = int((int(active_participants) / int(total_members)) * total_width) if int(total_members) > 0 else 0
                            inactive_width = total_width - active_width
                            
                            st.write(f"Active: {active_participants} | Inactive: {inactive_members}")
                            
                            # Simple bar representation
                            st.progress(float(active_participants) / float(total_members) if int(total_members) > 0 else 0)
                            st.caption(f"Active members: {retention_display} of total membership")
                        else:
                            st.info("No retention data available for this club.")
                    else:
                        st.error("Failed to retrieve retention data.")
                except Exception as e:
                    st.error(f"Error fetching retention data: {str(e)}")
            
            with major_tab:
                try:
                    # Get engagement by major
                    engagement_response = requests.get("http://api:4000/a/engagement_major")
                    
                    if engagement_response.status_code == 200:
                        engagement_data = engagement_response.json()
                        
                        # Filter for current club
                        club_engagement = [e for e in engagement_data if e.get("ClubName") == selected_club]
                        
                        if club_engagement:
                            st.write("### Engagement by Major")
                            
                            # Create a scrollable container
                            major_container = st.container(height=250)
                            
                            with major_container:
                                # Sort by event attendance (highest first)
                                sorted_engagement = sorted(
                                    club_engagement,
                                    key=lambda x: int(x.get("EventAttendance", 0)),
                                    reverse=True
                                )
                                
                                for engagement in sorted_engagement:
                                    major = engagement.get("Major", "Undeclared")
                                    attendance = engagement.get("EventAttendance", 0)
                                    
                                    # Display major and attendance
                                    st.write(f"**{major}**")
                                    st.write(f"Event Attendance: {attendance}")
                                    st.divider()
                            
                            # Get attendance by major data for comparison
                            attendance_major_response = requests.get("http://api:4000/a/attendance_major")
                            
                            if attendance_major_response.status_code == 200:
                                attendance_data = attendance_major_response.json()
                                
                                # Get overall top major for context
                                top_majors = {}
                                for item in attendance_data:
                                    major = item.get("Major", "Unknown")
                                    count = item.get("AttendanceCount", 0)
                                    
                                    if major not in top_majors:
                                        top_majors[major] = 0
                                    
                                    top_majors[major] += int(count)
                                
                                # Sort and get top 3
                                sorted_majors = sorted(
                                    [(major, count) for major, count in top_majors.items()],
                                    key=lambda x: x[1],
                                    reverse=True
                                )
                                
                                if sorted_majors:
                                    st.write("### Top Majors Across All Events")
                                    for i, (major, count) in enumerate(sorted_majors[:3]):
                                        st.write(f"{i+1}. **{major}**: {count} total attendances")
                        else:
                            st.info("No engagement by major data available for this club.")
                    else:
                        st.error("Failed to retrieve engagement by major data.")
                except Exception as e:
                    st.error(f"Error fetching engagement by major data: {str(e)}")
        else:
            st.write(f"Selected: {selected_club}")
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.write(f"Selected: {selected_club}")
elif st.session_state.clubs:
    st.info("Search and select a club to view details")
else:
    st.info("No clubs available")

SideBarLinks()
