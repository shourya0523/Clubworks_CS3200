import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.write("# Accessing a REST API from Within Streamlit")

"""
Simply retrieving data from a REST api running in a separate Docker Container.

If the container isn't running, this will be very unhappy.  But the Streamlit app 
should not totally die. 
"""

attendance = requests.get('http://api:4000/pres/attendance').json()

try:
  st.dataframe(attendance)
except:
  st.write("Could not connect to database to retrieve attendance")

st.dataframe(attendance)


