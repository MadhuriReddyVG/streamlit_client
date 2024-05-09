import streamlit as st
import pandas as pd
import sys
import logging
import logging.config
import json

import user_preferences
from interface.interface import is_user_authentic, get_user_details

def display_userdetails(userdetails):
    # Clear any cached data and fetch fresh from the database
    #st.cache_data.clear()

    # Remove unique_id
    #keys_to_remove = ['_id', 'unique_id']

    #new_dct = {key: [value] for key, value in userdetails.items() if key not in keys_to_remove}
    userdetails_dct = [ (key, value) for key, value in userdetails.items() ]
    
    #logging.debug('new_dct={}'.format(new_dct))

    #pagination = st.container()
    #data = pd.DataFrame(new_dct, columns=["User Health Params", "Values"]) 
    data = pd.DataFrame(userdetails_dct, columns=["User Health Params", "Values"]) 
    #TODO: Fix the disable-scrolling option
    st.dataframe(data, use_container_width=True)
    #pagination.dataframe(data, use_container_width=True)
    
    # Create a table to display the dictionary
    #st.table(new_dct)

def display_my_details():
    # Load messages json file
    with open('config/messages.json', 'r', encoding='utf-8') as file:
        messages_data = json.load(file)    

    st.title(messages_data['MY_DETAILS_PAGE']['TITLE'][user_preferences.mylanguage])

    # Check if user has logged in, to access this page
    result = is_user_authentic(user_preferences.username)
    if result != 'STATUS_OK':
        if result == "STATUS_NOT_LOGGED_IN":
            error_reason = 'USER_NOT_LOGGED_IN'     
        elif result == 'STATUS_SERVER_DOWN':
            error_reason = 'SERVER_DOWN'
        else:
            error_reason = 'GENERIC_ERROR'       
        st.error(messages_data['ERROR_MESSAGES'][error_reason][user_preferences.mylanguage])
        return   

    username = user_preferences.username
    language = user_preferences.mylanguage    

    result, user_details = get_user_details(username)
    if result == 'STATUS_OK':
        st.subheader(messages_data['MY_DETAILS_PAGE']['DISPLAY_USER_DETAILS'][language].format(username))
        display_userdetails(user_details)
    else:
        if result == "STATUS_NOT_LOGGED_IN":
            error_reason = 'USER_NOT_LOGGED_IN'     
        elif result == 'STATUS_SERVER_DOWN':
            error_reason = 'SERVER_DOWN'
        elif result == 'STATUS_NO_USER_DETAILS':
            error_reason = 'USER_DETAILS_NOT_AVAILABLE'     
        error_text = messages_data['ERROR_MESSAGES'][error_reason][language]
        st.markdown(f"<p style='white-space: pre-line; color:red;'>{error_text}</p>", unsafe_allow_html=True)
        return      
    
if __name__ == "__main__":
    display_my_details()