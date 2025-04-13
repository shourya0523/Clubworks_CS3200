import logging
logger = logging.getLogger(__name__)
import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

SideBarLinks()

st.title("# Welcome to the System's Coordinator Dashboard, Connor!")
st.write("# Organize and access club data and metrics")

