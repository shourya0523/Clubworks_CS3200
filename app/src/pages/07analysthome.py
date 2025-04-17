import logging
logger = logging.getLogger(__name__)

import streamlit as st
from modules.nav import SideBarLinks

st.set_page_config(layout = 'wide')

SideBarLinks()
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.switch_page('Home')
    
if st.session_state['role'] != 'Analyst':
    st.switch_page('Home')

if 'first_name' in st.session_state:
    first_name = st.session_state['first_name']
else:
    first_name = "Analyst"  

st.title(f"Welcome {first_name}!")
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
