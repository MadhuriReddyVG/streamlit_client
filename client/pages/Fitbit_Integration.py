import requests
import streamlit as st
import pandas as pd
from utils import get_fitbit_token
import logging 
import logging.config
import json

import user_preferences
from interface.interface import is_user_authentic, get_fitbit_data

def display_sleep_pattern(fitbit_access_token=None, base_date=None, end_date=None, messages_data=None):  
    username = user_preferences.username
    language = user_preferences.mylanguage
    activity_type = 'sleep'    
    result, sleepList = get_fitbit_data(username, fitbit_access_token, activity_type, base_date, end_date)
    if result != 'STATUS_OK':
        if result == "STATUS_NOT_LOGGED_IN":
            error_reason = 'USER_NOT_LOGGED_IN'     
        elif result == 'STATUS_SERVER_DOWN':
            error_reason = 'SERVER_DOWN'
        else:
            error_reason = 'GENERIC_ERROR'     
        error_text = messages_data['ERROR_MESSAGES'][error_reason][language]
        st.markdown(f"<p style='white-space: pre-line; color:red;'>{error_text}</p>", unsafe_allow_html=True)
        return      
    if sleepList is None:
        logging.debug('Fitbit data is empty')
        st.write('Fitbit data is empty')
        return
    if sleepList is None:
        return

    datetime_lst = []
    timeinbed_lst = []
    efficiency_lst = []
    for sleepItem in sleepList:
        mainSleep = sleepItem['isMainSleep']
        if mainSleep == True:
            datetime_lst.append(sleepItem['dateOfSleep'])
            timeinbed_lst.append(sleepItem['timeInBed']/60.0)
            efficiency_lst.append(sleepItem['efficiency'])
    #st.write(datetime_lst)
    #st.write(timeinbed_lst)
    #st.write(efficiency_lst)

    df = pd.DataFrame({'date_of_sleep': datetime_lst, 'time_in_bed(hours)': timeinbed_lst, 'sleep_efficiency':  efficiency_lst})

    col1, col2 = st.columns([1.5, 1.5])

    with col1:
        st.line_chart(data=df, x="date_of_sleep", y="time_in_bed(hours)")
    with col2:
        st.line_chart(data=df, x="date_of_sleep", y="sleep_efficiency")

def display_resting_heartrate(fitbit_access_token=None, base_date=None, end_date=None, messages_data=None):
    # List of activity types to retrieve from Fitbit API
    activityList = ['activities/minutesSedentary', 'activities/minutesLightlyActive','activities/minutesFairlyActive', 'activities/minutesVeryActive', 'activities/heart']

    base_date='2023-01-01'
    end_date='2024-03-21'
    #heartRate_lst = df_fitbit(activityList[4], base_date, end_date, fitbit_access_token)['activities-heart']

    username = user_preferences.username
    language = user_preferences.mylanguage
    activity_type = 'heartrate'    
    result, heartRate_lst = get_fitbit_data(username, fitbit_access_token, activity_type, base_date, end_date)
    if result != 'STATUS_OK':
        if result == "STATUS_NOT_LOGGED_IN":
            error_reason = 'USER_NOT_LOGGED_IN'     
        elif result == 'STATUS_SERVER_DOWN':
            error_reason = 'SERVER_DOWN'
        else:
            error_reason = 'GENERIC_ERROR'     
        error_text = messages_data['ERROR_MESSAGES'][error_reason][language]
        st.markdown(f"<p style='white-space: pre-line; color:red;'>{error_text}</p>", unsafe_allow_html=True)
        return      
    if heartRate_lst is None:
        logging.debug('Fitbit data is empty')
        st.write('Fitbit data is empty')
        return

    resting_hr_lst = []
    datetime_lst = []
    for dct in heartRate_lst:
        if 'restingHeartRate' in dct['value']:
            resting_hr_lst.append(dct['value']['restingHeartRate'])
            datetime_lst.append(dct['dateTime'])

    #logging.debug('datetime: {}'.format(datetime_lst))
    #logging.debug('resting_hr: {}'.format(resting_hr_lst))
    df = pd.DataFrame({'datetime': datetime_lst, 'resting heart rate': resting_hr_lst})
            
    st.line_chart(data=df, x="datetime", y="resting heart rate")

def display_fitbit_data(messages_data):
    fitbit_access_token = get_fitbit_token()

    #TODO: Make the base date and end date configurable
    display_sleep_pattern(fitbit_access_token=fitbit_access_token, base_date='2023-10-01', end_date='2023-11-30', messages_data=messages_data)
    display_resting_heartrate(fitbit_access_token=fitbit_access_token, base_date='2023-01-01', end_date='2023-03-21', messages_data=messages_data)


def fitbit_integration():
    # Load messages json file
    with open('config/messages.json', 'r', encoding='utf-8') as file:
        messages_data = json.load(file)    

    st.title(messages_data['FITBIT_PAGE']['TITLE'][user_preferences.mylanguage])

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
    
    sleep_hr_msg = messages_data['FITBIT_PAGE']['SHOW_SLEEP_PATTERN'][user_preferences.mylanguage]
    fitbit_button = st.button(sleep_hr_msg)
    if fitbit_button:
        display_fitbit_data(messages_data)
    
if __name__ == "__main__":
     fitbit_integration()