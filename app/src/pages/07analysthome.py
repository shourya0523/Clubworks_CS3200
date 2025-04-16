import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

# Show appropriate sidebar links for the role of the currently logged in user
SideBarLinks()

st.title(f"Welcome Analyst!")
st.write('')
st.write('')
st.write('### What would you like to do today?')

if st.button('ClubSearch', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/07analyst.py')

if st.button('Engagement Tracker', 
             type='primary',
             use_container_width=True):
  st.switch_page('pages/07analystengagement.py')
