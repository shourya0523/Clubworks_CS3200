import streamlit as st
import pandas as pd
import requests as re

BASE_URL = 'http://api:4000'

st.set_page_config(page_title="Profile", layout="wide")

if 'nuid' in st.session_state:
    NUID = st.session_state['nuid']
else:
    st.switch_page('Home.py')

re.get(f'{BASE_URL}/s/get_student/{NUID}')


