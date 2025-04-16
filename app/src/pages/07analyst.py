import streamlit as st
import requests
from modules.nav import SideBarLinks
from datetime import datetime
from email.utils import parsedate_to_datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd



st.set_page_config(
    page_title="Club Search",
    page_icon="🔍",
    layout="wide"
)

st.title("Welcome to Club Search 🎉")
st.write("")

st.sidebar.title("Search Clubs 🔎")

# Fetch and cache club list
if "clubs" not in st.session_state:
    response = requests.get("http://api:4000/a/get_clubs")
    response.raise_for_status()
    clubs_data = response.json()
    st.session_state.clubs = [club["ClubName"] for club in clubs_data]

selected_club = st.sidebar.selectbox(
    "Search clubs",
    options=st.session_state.clubs,
    placeholder="Type to search clubs..."
)

if selected_club:
    st.header("Club Details 📋")
    st.subheader(selected_club)

    clubs_data = requests.get("http://api:4000/a/get_clubs").json()

    club_info = next((club for club in clubs_data if club["ClubName"] == selected_club))
    
    # Get basic club data
    clubs_data = requests.get("http://api:4000/a/get_clubs").json()
    club_info = next((club for club in clubs_data if club["ClubName"] == selected_club), None)
    
    if club_info:
        club_id = club_info.get("ClubID")
        
        # Get extra club information
        extra_info_list = requests.get("http://api:4000/a/get_clubs_information").json()
        
        # Find the matching club in extra_info by ClubName
        matching_extra_info = next((info for info in extra_info_list if info.get("ClubName") == selected_club), None)
        
        # Update club_info with matching extra info if found
        if matching_extra_info:
            club_info.update(matching_extra_info)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            description = club_info.get('Description', '')
            if description and "N/A" not in description:
                st.markdown(f"**Description:** {description}")
        
        with col2:
            if club_info.get("Website"):
                st.markdown(f"🌐 [Visit Website]({club_info['Website']})")
            contact = club_info.get("Email", '')
            if contact and "N/A" not in contact:
                st.markdown(f"📧 **Contact:** {contact}")
            if club_info.get("LinkTree"):
                st.markdown(f"🌲 [LinkTree]({club_info['LinkTree']})")
            if club_info.get("CalendarLink"):
                st.markdown(f"📅 [Calendar]({club_info['CalendarLink']})")

        # Active Members
        st.subheader("Active Members 👥")
        all_members = requests.get("http://api:4000/a/active_member").json()

        # Filter members based on the selected club's ID
        club_members = [m for m in all_members if m.get("ClubName") == selected_club]

        if club_members:
            with st.container(height=300):
                for m in club_members:
                    name = f"{m.get('FirstName', '')} {m.get('LastName', '')}".strip() or "Unknown"
                    status = f"Attended {m.get('EventsAttended', 0)} event(s)"
                    st.write(f"**{name}** - *{status}*")
                    st.divider()
        else:
            st.info("ℹ️ No active members found for this club.")


        # Funding Requests
        st.subheader("Funding Requests 💰")
        all_requests = requests.get("http://api:4000/a/funding_requests").json()

        club_requests = [req for req in all_requests if req.get("ClubName") == selected_club]

        if club_requests:
            with st.container(height=300):
                for req in club_requests:
                    created_time = req.get("CreatedTime", "")
                    try:
                        date = parsedate_to_datetime(created_time).strftime("%b %d, %Y")
                    except:
                        date = "Unknown date"
                    rating = req.get("AvgClubRating")
                    rating_str = f"{float(rating):.1f}/5.0" if rating else "No ratings"
                    st.write(f"**Request #{req['RequestID']} - {req['RequestType']}**")
                    st.write(f"Status: **{req['Status']}** | Created: {date}")
                    st.divider()
        else:
            st.info("ℹ️ No funding requests found for this club.")

# Engagement Info
st.subheader("Engagement Information 📈")
metrics_tab, retention_tab, major_tab, comparison_tab = st.tabs(["Performance Metrics", "Retention Rate", "Engagement by Major", "Club Comparison"])

with metrics_tab:
    # Fetch performance data
    performance = requests.get("http://api:4000/a/performance_metrics").json()

    # Get metrics for the selected club
    metrics = next((p for p in performance if p.get("ClubName") == selected_club), None)

    if metrics:
        # Display total attendance, average rating, and funding requests
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Attendance", metrics.get("TotalAttendance", 0))
        col2.metric("Average Rating", f"{float(metrics.get('AvgRating', 0)):.1f}/5.0")
        col3.metric("Funding Requests", metrics.get("FundingRequests", 0))

        # Display feedback description (if exists)
        feedback_str = metrics.get("FeedbackDescription", "")
        feedback_list = [fb.strip() for fb in feedback_str.split(",") if fb.strip()]

        if feedback_list:
            st.write("### Member Feedback")
            for fb in feedback_list:
                st.write(f"💬 {fb}")
        else:
            st.info("ℹ️ No feedback available for this club.")

        # Fetch event performance data
        events_data = requests.get("http://api:4000/a/get_performance").json()

        # Filter events for the selected club
        events = [e for e in events_data if e.get("ClubName") == selected_club]

        if events:
            st.write("### Attendance by Event Type and Interest")
            with st.container(height=250):
                event_map = {}
                for e in events:
                    etype = e.get("EventType", "Unknown")
                    interest = e.get("InterestName", "General")
                    count = e.get("TotalAttendance", 0)
                    if etype not in event_map:
                        event_map[etype] = []
                    event_map[etype].append((interest, count))

                for etype in event_map:
                    st.write(f"**{etype} Events**")
                    for item in event_map[etype]:
                        st.write(f"- {item[0]}: {item[1]} attendees")
                    st.divider()
        else:
            st.info("ℹ️ No event performance data available.")
    else:
        st.info("ℹ️ No performance metrics found for this club.")

        with retention_tab:
            retention = requests.get("http://api:4000/a/retention").json()
            data = next((r for r in retention if r.get("ClubName") == selected_club), None)

            if data:
                total = data.get("TotalMembers", 0)
                active = data.get("ActiveParticipants", 0)
                rate = float(data.get("RetentionRate", 0))
                cols = st.columns(3)
                cols[0].metric("Total Members", total)
                cols[1].metric("Active Participants", active)
                cols[2].metric("Retention Rate", f"{rate:.1f}%")
                st.progress(active / total if total > 0 else 0)
                st.caption(f"Active members: {rate:.1f}% of total membership")
            else:
                st.info("ℹ️ No retention data available.")

        with major_tab:
            engagement = requests.get("http://api:4000/a/engagement_major").json()
            club_engagement = [e for e in engagement if e.get("ClubName") == selected_club]

            if club_engagement:
                st.write("### Engagement by Major")
                with st.container(height=250):
                    sorted_engagement = sorted(club_engagement, key=lambda x: int(x.get("EventAttendance", 0)), reverse=True)
                    for e in sorted_engagement:
                        st.write(f"**{e['Major']}** — Event Attendance: {e['EventAttendance']}")
                        st.divider()

                attendance_data = requests.get("http://api:4000/a/attendance_major").json()

                majors = {}
                for item in attendance_data:
                    major = item["Major"]
                    majors[major] = majors.get(major, 0) + item.get("AttendanceCount", 0)

                major_items = sorted(majors.items(), key=lambda x: x[1], reverse=True)
                st.write("### Top Majors Across All Events")
                for i in range(min(3, len(major_items))):
                    m, c = major_items[i]
                    st.write(f"{i + 1}. **{m}**: {c} total attendances")
            else:
                st.info("ℹ️ No engagement by major data available.")




        with comparison_tab:
            all_metrics = requests.get("http://api:4000/a/performance_metrics").json()

            for m in all_metrics:
                m["EngagementScore"] = m.get("TotalAttendance", 0) + m.get("FundingRequests", 0)

            df = pd.DataFrame(all_metrics)
            df = df.sort_values(by="EngagementScore", ascending=False)

            colors = ["orange" if club == selected_club else "skyblue" for club in df["ClubName"]]

            fig, ax = plt.subplots(figsize=(8, 12))
            sns.barplot(
                data=df,
                y="ClubName",
                x="EngagementScore",
                palette=colors,
                ax=ax
            )
            ax.set_xlabel("Engagement Score")
            ax.set_ylabel("Club Name")
            ax.set_title(f"Engagement Score: {selected_club} vs All Clubs 🔥")
            st.pyplot(fig)
