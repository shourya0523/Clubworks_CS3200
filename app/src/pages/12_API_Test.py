# pages/12_API_Test.py
import datetime as dt
import logging
import requests
import streamlit as st

logging.basicConfig(level=logging.INFO)
BASE_URL = "http://api:4000"

DEFAULT_CLUB = 1
DEFAULT_EVENT = 1
DEFAULT_NUID = 123456789
DEFAULT_EMAIL = "test@neu.edu"
DEFAULT_PWD = "password123"

st.set_page_config(page_title="API Test Dashboard", layout="wide")
st.title("🧪 API Test Dashboard")


def dt_input(label: str, default: dt.datetime) -> dt.datetime:
    if hasattr(st, "datetime_input"):
        return st.datetime_input(label, default)
    cols = st.columns([2, 1])
    with cols[0]:
        d = st.date_input(label + " – date", default.date())
    with cols[1]:
        t = st.time_input(label + " – time", default.time())
    return dt.datetime.combine(d, t)


def show_response(resp: requests.Response):
    st.code(f"Status {resp.status_code}")
    if resp.headers.get("content-type", "").startswith("application/json"):
        try:
            st.json(resp.json())
        except Exception:
            st.write(resp.text)
    else:
        st.write(resp.text)


president_tab, analyst_tab, student_tab = st.tabs(
    ["👑 President", "📊 Analyst", "🎓 Student"]
)

# ───────── President ─────────
with president_tab:
    st.header("President routes")

    col1, col2, col3 = st.columns(3)
    with col1:
        club_id = st.number_input("Club ID", DEFAULT_CLUB, key="pres_club_id")
    with col2:
        event_id = st.number_input("Event ID", DEFAULT_EVENT, key="pres_event_id")
    with col3:
        exec_nuid = st.number_input("Exec NUID", DEFAULT_NUID, key="pres_exec_nuid")

    prez_get = {
        "attendance": f"/pres/attendance/{club_id}",
        "member_contact_information": f"/pres/member_contact_information/{club_id}",
        "obtain_anonamous_feedback": f"/pres/obtain_anonamous_feedback/{club_id}",
        "attendance_by_event_type": f"/pres/attendance_by_event_type/{club_id}",
        "event (first only)": f"/pres/event/{club_id}",
        "events (list IDs)": f"/pres/events/{club_id}",
        "profile": f"/pres/profile/{exec_nuid}",
        "loadevent": f"/pres/loadevent/{event_id}",
        "event_types": "/pres/event_types",
        "request_types": "/pres/request_types",
        "support_request_types": "/pres/support_request_types",
        "programs": "/pres/programs",
        "program_applications": "/pres/program_applications",
    }

    st.subheader("GET")
    for lbl, ep in prez_get.items():
        if st.button(lbl, key=f"prez_get_{ep}"):
            show_response(requests.get(f"{BASE_URL}{ep}"))

    st.subheader("POST / PUT")

    with st.expander("Create Event"):
        with st.form("create_event"):
            name = st.text_input("Name", "API‑Test Event")
            loc = st.text_input("Location", "Test Hall 101")
            start = dt_input("Start", dt.datetime.now() + dt.timedelta(days=7))
            end = dt_input("End", dt.datetime.now() + dt.timedelta(days=7, hours=2))
            club_ce = st.number_input("Club ID", DEFAULT_CLUB, key="ceclub")
            poster = st.text_input("Poster URL", "https://via.placeholder.com/300")
            ev_type = st.text_input("Event Type", "Workshop")
            if st.form_submit_button("Send"):
                payload = {
                    "Name": name,
                    "Location": loc,
                    "StartTime": start.strftime("%Y-%m-%d %H:%M:%S"),
                    "EndTime": end.strftime("%Y-%m-%d %H:%M:%S"),
                    "ClubID": club_ce,
                    "PosterImg": poster,
                    "Type": ev_type,
                }
                show_response(requests.post(f"{BASE_URL}/pres/create_event", json=payload))

    with st.expander("Edit Event"):
        with st.form("edit_event"):
            edit_id = st.number_input("Event ID", DEFAULT_EVENT, key="edit_event_id")
            new_name = st.text_input("New name", "Edited Event")
            new_loc = st.text_input("New location", "Room 42")
            new_start = dt_input("New start", dt.datetime.now() + dt.timedelta(days=10))
            new_end = dt_input("New end", dt.datetime.now() + dt.timedelta(days=10, hours=3))
            new_type = st.text_input("New type", "Seminar")
            new_post = st.text_input("New poster URL", "https://via.placeholder.com/400")
            if st.form_submit_button("Send"):
                payload = {
                    "Name": new_name,
                    "Location": new_loc,
                    "StartTime": new_start.strftime("%Y-%m-%d %H:%M:%S"),
                    "EndTime": new_end.strftime("%Y-%m-%d %H:%M:%S"),
                    "Type": new_type,
                    "PosterImg": new_post,
                }
                show_response(requests.put(f"{BASE_URL}/pres/edit_event/{edit_id}", json=payload))

    with st.expander("Make Executive Request"):
        with st.form("make_request"):
            desc = st.text_input("Description", "Extra funding")
            req_t = st.text_input("Type", "Budget")
            if st.form_submit_button("Send"):
                payload = {
                    "RequestDescription": desc,
                    "Status": "Pending",
                    "CreatedTime": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Type": req_t,
                    "ExecutiveID": exec_nuid,
                    "ExecutiveClub": club_id,
                    "ExecutivePosition": "President",
                }
                show_response(requests.put(f"{BASE_URL}/pres/make_request", json=payload))

    with st.expander("Make Support Request"):
        with st.form("support_request"):
            sr_desc = st.text_input("Support description", "Need AV")
            sr_type = st.text_input("Support type", "Logistics")
            if st.form_submit_button("Send"):
                payload = {"RequestID": 0, "RequestDescription": sr_desc, "Type": sr_type}
                show_response(requests.put(f"{BASE_URL}/pres/make_support_request", json=payload))

# ───────── Analyst ─────────
with analyst_tab:
    st.header("Analyst routes")

    analyst_eps = {
        "Clubs": "/a/get_clubs",
        "Club info": "/a/get_clubs_information",
        "Performance": "/a/get_performance",
        "Demographics": "/a/demographics_insights",
        "Active members": "/a/active_member",
        "Retention": "/a/retention",
        "Attendance by major": "/a/attendance_major",
        "Engagement by major": "/a/engagement_major",
        "Metrics": "/a/performance_metrics",
        "Funding": "/a/funding_requests",
        "Club interests": "/a/club_interests",
        "Club engagement": "/a/club_engagement",
        "Top clubs": "/a/top_club",
    }
    for lbl, ep in analyst_eps.items():
        if st.button(lbl, key=f"analyst_{ep}"):
            show_response(requests.get(f"{BASE_URL}{ep}"))

# ───────── Student ─────────
with student_tab:
    st.header("Student routes")

    col1, col2, col3 = st.columns(3)
    with col1:
        stu_nuid = st.number_input("Student NUID", DEFAULT_NUID, key="stu_nuid")
    with col2:
        club_fb = st.number_input("Club ID", DEFAULT_CLUB, key="stu_club_fb")
    with col3:
        program_id = st.number_input("Program ID", 1, key="stu_program_id")

    student_gets = {
        "Login": f"/s/student_login?email={DEFAULT_EMAIL}&password={DEFAULT_PWD}",
        "Profile": f"/s/get_student_profile/{stu_nuid}",
        "Follow count": f"/s/followcount/{stu_nuid}",
        "Follows": f"/s/follows/{stu_nuid}",
        "Open apps": "/s/open_apps",
        "All feedback": "/s/feedback",
        "Club feedback": f"/s/feedback/{club_fb}",
        "Clubs": "/s/clubs",
        "Programs": "/s/programs",
        "Program apps": f"/s/program_applications/{program_id}",
        "Events": "/s/events",
        "Attendance": f"/s/attendance/{stu_nuid}",
        "Memberships": f"/s/memberships/{stu_nuid}",
        "Upcoming events": f"/s/upcoming_events/{stu_nuid}",
        "Student interests": f"/s/student_interests/{stu_nuid}",
        "Interests": "/s/interests",
        "Recommended clubs": f"/s/recommended_clubs/{stu_nuid}",
        "Recommendations": f"/s/recommendations/{stu_nuid}",
        "Club interests": f"/s/club_interests/{club_fb}",
        "Other students": f"/s/all_students/{stu_nuid}",
        "Network": f"/s/personal_network/{stu_nuid}",
    }
    st.subheader("GET")
    for lbl, ep in student_gets.items():
        if st.button(lbl, key=f"stu_get_{ep}"):
            show_response(requests.get(f"{BASE_URL}{ep}"))

    st.subheader("POST")

    with st.expander("Attend event"):
        with st.form("attend_event"):
            ae_event = st.number_input("Event ID", DEFAULT_EVENT, key="ae_event")
            if st.form_submit_button("RSVP"):
                payload = {"nuid": stu_nuid, "event_id": ae_event}
                show_response(requests.post(f"{BASE_URL}/s/attend_event", json=payload))

    with st.expander("Apply to application"):
        with st.form("apply_app"):
            app_name = st.text_input("Application name", "Sample Application")
            if st.form_submit_button("Apply"):
                payload = {"nuid": stu_nuid, "application_name": app_name}
                show_response(requests.post(f"{BASE_URL}/s/apply_to_app", json=payload))

    with st.expander("Follow student"):
        with st.form("follow_form"):
            followee = st.number_input("Followee NUID", DEFAULT_NUID + 1, key="followee_nuid")
            if st.form_submit_button("Follow"):
                payload = {"follower_nuid": stu_nuid, "followee_nuid": followee}
                show_response(requests.post(f"{BASE_URL}/s/follow", json=payload))
