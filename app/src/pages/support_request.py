import streamlit as st
import requests

st.title("Submit a Support Request 🛠️")

# Assume user has logged in and we have their NUID
if 'nuid' in st.session_state:
    nuid = st.session_state['nuid']

    response = requests.get(f'requests.get(f"http://api:4000/s/student_login/{nuid}")')
    response.raise_for_status()
else:
    st.switch_page('Home.py')

if nuid:
    # Get request types
    type_response = requests.get(f"http://api:4000/students/get_request_types/{nuid}")
    
    if type_response.status_code == 200:
        request_types = type_response.json()
        type_options = {item['RequestType']: item['RequestTypeID'] for item in request_types}
        
        selected_type = st.selectbox("Request Type", list(type_options.keys()))
        request_description = st.text_area("Describe your request")

        if st.button("Submit Request"):
            if selected_type and request_description:
                payload = {
                    "Type": type_options[selected_type],
                    "RequestDescription": request_description
                }

                post_response = requests.post(
                    f"http://api:4000/students/support_request/{nuid}",
                    json=payload
                )

                if post_response.status_code == 200:
                    st.success("✅ Your support request was submitted!")
                else:
                    st.error("❌ Failed to submit the request.")
            else:
                st.warning("Please fill in all fields.")
    else:
        st.error("❌ Failed to fetch request types.")
