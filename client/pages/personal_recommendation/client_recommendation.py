import requests
import streamlit as st
import logging
import logging.config
import sys 
#sys.path.append('./pages/database')
#from server.database import Database
import user_preferences
from interface.interface import get_user_field, get_food_recommendation, get_workout_recommendation
from utils import get_server_ip, get_error_reason

import json

def low_risk_profile(fr_risk):
    #rec_text = "Your Framingham Risk is . Please select CalculateHeartHealth in the HeartHealthMenu options on the left"
    #st.markdown(f"<p style='white-space: pre-line; color:red;'>{nouser_details_text}</p>", unsafe_allow_html=True)
    st.markdown(
        f"<p style='text-align:center; font-size:18px; font-weight:bold; color:green;'>Your Framingham Risk is {fr_risk}%. You are in the low risk profile</p>",
        unsafe_allow_html=True
    )
     
    st.markdown(
        """
        Please follow these recommendations to maintain your low risk profile:
        - **Maintain Healthy Lifestyle**: Adopt and maintain a healthy diet, regular physical activity, and avoid tobacco use.
        - **Regular Monitoring**: Please undertake annual health check-ups to monitor blood pressure, cholesterol levels, and other relevant metrics
        """
    )

def medium_risk_profile(fr_risk):
    st.markdown(
        f"<p style='text-align:center; font-size:18px; font-weight:bold; color:yellow;'>Your Framingham Risk is {fr_risk}%. You are in the medium risk profile</p>",
        unsafe_allow_html=True
    )
     
    st.markdown(
        """
        Please follow these recommendations to move to low risk profile:
        - **Lifestyle Adjustments**: Recommend specific lifestyle changes such as adopting a heart-healthy diet (e.g., DASH or Mediterranean diet), increasing physical activity, and quitting smoking if applicable.
        - **Stress Management**: Provide tips on stress management techniques, such as mindfulness, yoga, or regular exercise.
        """
    )

def high_risk_profile(fr_risk):
    st.markdown(
        f"<p style='text-align:center; font-size:18px; font-weight:bold; color:red;'>Your Framingham Risk is {fr_risk}%. You are in the high risk profile</p>",
        unsafe_allow_html=True
    )
     
    st.markdown(
        """
        Please follow these recommendations to move to low risk profile:
        - **Medical Consultation**: Strongly recommend you to consult a healthcare professional for a comprehensive evaluation and personalized plan.
        - **Medication Adherence**: If on medication, please adhere to prescribed treatments.
        - **Targeted Lifestyle Changes**: Follow more targeted lifestyle changes, possibly including working with a dietitian, fitness coach, or joining support groups for smoking cessation.
        """
    )

def show_personal_recommendation():
     # Load messages json file
    with open('config/messages.json', 'r', encoding='utf-8') as file:
        messages_data = json.load(file)  
    
    username = user_preferences.username
    language = user_preferences.mylanguage

    field_dct = {'framingham_risk': None}
    result, populated_field_dct = get_user_field(username, field_dct)
    if result != 'STATUS_OK':     
        error_reason =  get_error_reason(result=result)
        nouser_details_text = messages_data['ERROR_MESSAGES'][error_reason][language]
        st.markdown(f"<p style='white-space: pre-line; color:red;'>{nouser_details_text}</p>", unsafe_allow_html=True)
        return      

    logging.debug('get_user_field output dct: {}'.format(populated_field_dct))
    fr_risk = float(populated_field_dct['framingham_risk'].strip('%'))
    logging.debug('fr_risk = {}'.format(fr_risk))

    if (fr_risk < 10.0):
        low_risk_profile(fr_risk)           
    elif (10.0 < fr_risk < 20.0):
        medium_risk_profile(fr_risk) 
    else:
        high_risk_profile(fr_risk)     

def show_food_recommendation():
     # Load messages json file
    with open('config/messages.json', 'r', encoding='utf-8') as file:
        messages_data = json.load(file)  
    
    username = user_preferences.username
    language = user_preferences.mylanguage

    result, food_rec = get_food_recommendation(username=username, language=language)
    if result != 'STATUS_OK':     
        error_reason =  get_error_reason(result=result)
        error_text = messages_data['ERROR_MESSAGES'][error_reason][language]
        st.markdown(f"<p style='white-space: pre-line; color:red;'>{error_text}</p>", unsafe_allow_html=True)
        return
    
    logging.debug('Diet Recommendation Response: {}'.format(food_rec))

    st.write(food_rec)

    # Display the Reference
    diet_ref_url="https://www.ahajournals.org/doi/10.1161/CIR.0000000000001031"
    st.markdown("Note: The above recommendation is based on [American Heart Association Diet Recommendation](%s)"%diet_ref_url)  
           
def show_workout_recommendation():
    # Load messages json file
    with open('config/messages.json', 'r', encoding='utf-8') as file:
        messages_data = json.load(file)  
    
    username = user_preferences.username
    language = user_preferences.mylanguage

    result, workout_rec = get_workout_recommendation(username=username, language=language)
    if result != 'STATUS_OK':     
        error_reason =  get_error_reason(result=result)
        error_text = messages_data['ERROR_MESSAGES'][error_reason][language]
        st.markdown(f"<p style='white-space: pre-line; color:red;'>{error_text}</p>", unsafe_allow_html=True)
        return
    
    logging.debug('Diet Recommendation Response: {}'.format(workout_rec))

    st.write(workout_rec)

    # Display the Reference; TODO: Enable this
    #workout_ref_url="https://www.ahajournals.org/doi/10.1161/CIR.0000000000001031"
    #st.markdown("Note: The above recommendation is based on [American Heart Association Diet Recommendation](%s)"%diet_ref_url) 
