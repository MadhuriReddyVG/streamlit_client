import streamlit as st
from streamlit_player import st_player
import logging
import logging.config
import sys 
import json

import user_preferences
from interface.interface import is_user_authentic, get_user_details, get_user_field
from utils import get_error_reason

def low_risk_workout_guide(age, fr_risk):
    st.markdown(
        f"<p style='text-align:center; font-size:18px; font-weight:bold; color:green;'>You are {age} years old and your Framingham Risk is {fr_risk}%. You are in the low risk profile. Follow this workout schedule</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<p style='text-align:center; font-size:14px; font-weight:bold;'>Brisk Walking: An easy, accessible form of cardiovascular exercise that can be done anywhere. Aim for at least 30 minutes on most days of the week.</p>",
        unsafe_allow_html=True
    )
    st_player("https://www.youtube.com/watch?v=wQrV75N2BrI")

    st.markdown(
        f"<p style='text-align:center; font-size:14px; font-weight:bold;'>Cycling: Either stationary or on a bike, cycling is excellent for cardiovascular health and can be adjusted in intensity to match fitness levels.</p>",
        unsafe_allow_html=True
    )
    st_player("https://www.youtube.com/watch?v=IrFtZF8DlvA")

    st.markdown(
        f"<p style='text-align:center; font-size:14px; font-weight:bold;'>Swimming: Provides a full-body workout, improving cardiovascular health, flexibility, and muscular strength without putting stress on the joints.</p>",
        unsafe_allow_html=True
    )
    st_player("https://www.youtube.com/watch?v=TzuvoTn3fic")



def medium_risk_workout_guide(age, fr_risk):
    st.markdown(
        f"<p style='text-align:center; font-size:18px; font-weight:bold; color:yellow;'>You are {age} years old and your Framingham Risk is {fr_risk}%. You are in the medium risk profile. Follow this workout schedule</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<p style='text-align:center; font-size:14px; font-weight:bold;'>Jogging or Light Running: Increases heart rate and improves cardiovascular endurance. Start with shorter distances, and gradually increase as fitness improves, ensuring to monitor heart rate and exertion levels.</p>",
        unsafe_allow_html=True
    )
    st_player("https://www.youtube.com/watch?v=9L2b2khySLE")

    st.markdown(
        f"<p style='text-align:center; font-size:14px; font-weight:bold;'>Aerobic Classes: Activities like Zumba or step aerobics are fun and can be adapted to various fitness levels. They help improve heart health and can be a good way to stay motivated.</p>",
        unsafe_allow_html=True
    )
    st_player("https://www.youtube.com/watch?v=uGi_c0ewmbg")

    st.markdown(
        f"<p style='text-align:center; font-size:14px; font-weight:bold;'>Strength Training: Incorporate light to moderate weight training to help control body weight, improve cholesterol, and manage blood sugar levels. Focus on major muscle groups, using a weight that allows for 12-15 repetitions per set.</p>",
        unsafe_allow_html=True
    )
    st_player("https://www.youtube.com/watch?v=UfnKkdcvCMg")


def high_risk_workout_guide(age, fr_risk):  
    st.markdown(
        f"<p style='text-align:center; font-size:18px; font-weight:bold; color:red;'>You are {age} years old and your Framingham Risk is {fr_risk}%. You are in the high risk profile. Follow this workout schedule</p>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<p style='text-align:center; font-size:14px; font-weight:bold;'>Guided Low-Impact Aerobics: Low-impact classes, possibly in a supervised setting, can help maintain cardiovascular health without putting too much strain on the heart. Water aerobics, for example, is gentle on the joints and can be quite beneficial.</p>",
        unsafe_allow_html=True
    )
    st_player("https://www.youtube.com/watch?v=kRk3w1uZY0E")

    st.markdown(
        f"<p style='text-align:center; font-size:14px; font-weight:bold;'>Walking: Start with short, leisurely walks, gradually increasing the duration and pace as tolerated. Walking is a low-risk activity that can be easily adapted to fitness levels.</p>",
        unsafe_allow_html=True
    )
    st_player("https://www.youtube.com/watch?v=u08lo0bESJc")

    st.markdown(
        f"<p style='text-align:center; font-size:14px; font-weight:bold;'>Tai Chi or Yoga: These forms of exercise focus on gentle movements, balance, and flexibility and have been shown to lower blood pressure and reduce stress, which are beneficial for heart health.</p>",
        unsafe_allow_html=True
    )
    st_player("https://www.youtube.com/watch?v=p9js_JEYmIc")

def workout_guide():
    # Load messages json file
    with open('config/messages.json', 'r', encoding='utf-8') as file:
        messages_data = json.load(file)    

    st.title(messages_data['WORKOUT_GUIDE_PAGE']['TITLE'][user_preferences.mylanguage])

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

    field_dct = {'framingham_risk': None, 'age': None}
    result, populated_field_dct = get_user_field(username, field_dct)
    if result != 'STATUS_OK':     
        error_reason =  get_error_reason(result=result)
        nouser_details_text = messages_data['ERROR_MESSAGES'][error_reason][language]
        st.markdown(f"<p style='white-space: pre-line; color:red;'>{nouser_details_text}</p>", unsafe_allow_html=True)
        return      

    logging.debug('get_user_field output dct: {}'.format(populated_field_dct))
    fr_risk = float(populated_field_dct['framingham_risk'].strip('%'))
    age = populated_field_dct['age']
    #TODO: Need to use these details
    #gender = user_details['gender']
    #weight_kgs = user_details['weight_kgs']
    #height_cms = user_details['height_cms']       
        
    logging.debug('fr_risk = {}, age = {}'.format(fr_risk, age))

    if (fr_risk < 10.0):
        low_risk_workout_guide(age, fr_risk)           
    elif (10.0 < fr_risk < 20.0):
        medium_risk_workout_guide(age, fr_risk) 
    else:
        high_risk_workout_guide(age, fr_risk)    

if __name__ == "__main__":
    workout_guide()
