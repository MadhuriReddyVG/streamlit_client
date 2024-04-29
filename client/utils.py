import json
import logging
import logging.config
import streamlit as st

# Start Display Work in Progress
def start_display_wip(wip_str):        
    # Display "Calculating Heart Age" message during computation
    progress_bar = st.progress(0)
    status_text = st.empty()
    #status_text.text("Calculating Heart Age...")

    md_str = "\"<p style='text-align:center; font-size:24px; font-weight:bold;'>" + wip_str + "...</p>\""
    # Styling for the message
    status_text.markdown(
            md_str,
            unsafe_allow_html=True
    )

    return progress_bar, status_text

def stop_display_wip(progress_bar, status_text):
    # Update UI after computation
    progress_bar.empty()
    status_text.empty()

def load_json_file(filename):
    with open(filename, 'r') as file:
        config = json.load(file)

    return config    

def get_server_ip():
    st.write("IP ADDR: ", st.secrets["ip_addr"])

    # Temporary Hack to deploy to streamlit cloud
    return st.secrets["ip_addr"]

    #Load server IP from the config.json
    config = load_json_file(filename='config/config.json')

    server_address = config['server_ip_address']
    if server_address is None:
        logging.error("Unable to get server IP address")
            
    return server_address

def check_windows_machine():
    config = load_json_file(filename='config.json')

    is_win_machine = config['windows_dev_machine']
    
    return is_win_machine

def get_fitbit_token():
    config = load_json_file(filename='client/pages/fitbit_integration/fitbit.json')

    fitbit_access_token = config['fitbit_access_token']
    if fitbit_access_token is None:
        logging.error("Unable to get Fitbit Access Token")
            
    return fitbit_access_token

def get_error_reason(result) -> str:
    if result == "STATUS_NOT_LOGGED_IN":
        error_reason = 'USER_NOT_LOGGED_IN'     
    elif result == 'STATUS_SERVER_DOWN':
        error_reason = 'SERVER_DOWN'
    elif result == 'STATUS_NO_USER_DETAILS':
        error_reason = 'USER_DETAILS_NOT_AVAILABLE'
    elif result == 'STATUS_INVALID_FIELDS':
        error_reason = 'GENERIC_ERROR'
    elif result == 'STATUS_INVALID_CREDENTIALS':
        error_reason = 'INVALID_CREDENTIALS'     
    
    return error_reason
