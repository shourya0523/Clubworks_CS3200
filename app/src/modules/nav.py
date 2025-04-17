# Idea borrowed from https://github.com/fsmosca/sample-streamlit-authenticator

# This file has function to add certain functionality to the left side bar of the app

import streamlit as st


def HomeNav():
    st.sidebar.page_link("Home.py", label="Home", icon="🏠")

def StudentDisc():
    st.sidebar.page_link("pages/01_Discover", label="Discover", icon="🧠")
    
def StudentProf():
    st.sidebar.page_link("pages/14_Student_Profile", label="Profile", icon="🧠")

def ClubMan():
    st.sidebar.page_link(
        "pages/02_club_management.py", label="Manage Your Club", icon="👤"
    )


def AnalystHome():
    st.sidebar.page_link(
        "pages/07analystshome.py", label="World Bank Visualization", icon="🏦"
    )


def MapDemoNav():
    st.sidebar.page_link("pages/02_Map_Demo.py", label="Map Demonstration", icon="🗺️")


## ------------------------ Examples for Role of usaid_worker ------------------------
def ApiTestNav():
    st.sidebar.page_link("pages/12_API_Test.py", label="Test the API", icon="🛜")


def PredictionNav():
    st.sidebar.page_link(
        "pages/11_PredictionV2.py", label="Regression Prediction", icon="📈"
    )


def ClassificationNav():
    st.sidebar.page_link(
        "pages/13_Classification.py", label="Classification Demo", icon="🌺"
    )


#### ------------------------ Club President Role ------------------------
def clubmanagement02():
    st.sidebar.page_link("pages/02_club_management.py", label="Club Management", icon="🖥️")
    st.sidebar.page_link("pages/02.1_create_event.py", label="Create Event", icon="🏢")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(role=None):
    """Render role-appropriate sidebar navigation links"""
    st.sidebar.image("assets/logo.png", width=150)
    
    # Authentication checks
    if "authenticated" not in st.session_state or not st.session_state.authenticated:
        st.switch_page("Home.py")
    
    # Role-based navigation
    if role == "admin":
        st.sidebar.page_link("pages/admin_dashboard.py", label="Admin Dashboard", icon="🛠️")
        st.sidebar.page_link("pages/admin/system_health.py", label="System Health", icon="📊")
        st.sidebar.page_link("pages/admin/issue_tracker.py", label="Issue Tracker", icon="📩")
    elif role == "student":
        st.sidebar.page_link("pages/01_Discover.py", label="Discover Clubs", icon="🔍")
        st.sidebar.page_link("pages/14_Student_Profile.py", label="My Profile", icon="👤")
    elif role == "president":
        st.sidebar.page_link("pages/02_club_management.py", label="Club Dashboard", icon="🏛️")
        st.sidebar.page_link("pages/02.1_create_event.py", label="Create Event", icon="🎉")
    elif role == "analyst":
        st.sidebar.page_link("pages/07analysthome.py", label="Analytics Hub", icon="📈")
        st.sidebar.page_link("pages/07analystengagement.py", label="Engagement", icon="📊")

    # Universal elements
    if st.sidebar.button("🏠 Return Home"):
        st.switch_page("Home.py")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.switch_page("Home.py")


def clubmanagement02():
    st.sidebar.page_link("pages/02_club_management.py", label="Club Management", icon="🖥️")
    st.sidebar.page_link("pages/02.1_create_event.py", label="Create Event", icon="🏢")


# --------------------------------Links Function -----------------------------------------------
def SideBarLinks(show_home=True):
    """
    This function handles adding links to the sidebar of the app based upon the logged-in user's role, which was put in the streamlit session_state object when logging in.
    """

    # add a logo to the sidebar always
    st.sidebar.image("assets/logo.png", width=150)

    # If there is no logged in user, redirect to the Home (Landing) page
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.switch_page("Home.py")

    if show_home:
        # Show the Home page link (the landing page)
        HomeNav()

    # Show the other page navigators depending on the users' role.
    if st.session_state["authenticated"]:

        # Show World Bank Link and Map Demo Link if the user is a political strategy advisor role.
        if st.session_state["role"] == "Club President":
            clubmanagement02()


        # If the user role is usaid worker, show the Api Testing page
        if st.session_state["role"] == "Analyst":
            PredictionNav()
            ApiTestNav()
            ClassificationNav()

        # If the user is an administrator, give them access to the administrator pages
        if st.session_state["role"] == "Student":
            AdminPageNav()
            
        if st.session_state["role"] == "Systems Coordinator":
            AdminPageNav()

    # Always show the About page at the bottom of the list of links
    AboutPageNav()

    if st.session_state["authenticated"]:
        # Always show a logout button if there is a logged in user
        if st.sidebar.button("Logout"):
            del st.session_state["role"]
            del st.session_state["authenticated"]
            st.switch_page("Home.py")

