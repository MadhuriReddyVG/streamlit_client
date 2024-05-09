import streamlit as st
import requests
import json 
import logging
import logging.config
#import urllib
import base64

import user_preferences
from interface.interface import is_user_authentic, query_healthbot
from utils import get_server_ip, get_error_reason

def display_pdf(file):
   # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

def hearthealth_bot():
    # Load messages json file
    with open('config/messages.json', 'r', encoding='utf-8') as file:
        messages_data = json.load(file)    

    st.title(messages_data['HEALTHBOT_PAGE']['TITLE'][user_preferences.mylanguage])

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
    
    text_input = messages_data['HEALTHBOT_PAGE']['BOT_MSG'][language]
    query = st.text_input(text_input)
    
    bot_button_msg = messages_data['HEALTHBOT_PAGE']['BOT_BUTTON_MSG'][language]
    bot_button = st.button(bot_button_msg)
    if bot_button:
        if query is not None:
            logging.debug('***User Query to the HealthBot: {}***'.format(query))
            result, query_response = query_healthbot(username, language, query)
            if result != 'STATUS_OK':
                error_reason =  get_error_reason(result=result)
                error_text = messages_data['ERROR_MESSAGES'][error_reason][language]
                st.markdown(f"<p style='white-space: pre-line; color:red;'>{error_text}</p>", unsafe_allow_html=True)
                return
    
            logging.debug('HealthBot Query Response: {}'.format(query_response))

            st.write(query_response)
            # Display the Health Bot Data Reference
            health_ref_url="https://academic.oup.com/eurheartj/article/42/34/3227/6358713"
            st.markdown("Note: The above response is based on [European Society of Cardiology CVD Guidelines](%s)"%health_ref_url)          
            
if __name__ == "__main__":
     hearthealth_bot()
