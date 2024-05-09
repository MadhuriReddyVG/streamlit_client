import streamlit as st
#import sys 
#sys.path.append('./pages/database')
#from database_workout import DatabaseWorkout
import logging
import logging.config
import json

import user_preferences
from interface.interface import is_user_authentic, log_user_workout

def display_msg(msg):
     st.markdown(
        f"<p style='text-align:center; font-size:18px; font-weight:bold;'>{msg}</p>",
        unsafe_allow_html=True
    )

def log_duration_minutes(language, messages_data, key=None):
     duration_msg = messages_data['WORKOUT_LOGGER_PAGE']['DURATION_MSG'][language]
     duration_minutes = st.number_input(duration_msg, key=key)
     return duration_minutes

def log_exercise_notes(language, messages_data, key=None):
     exercise_notes_msg = messages_data['WORKOUT_LOGGER_PAGE']['EXERCISE_NOTES_MSG'][language]
     exercise_notes = st.text_input(exercise_notes_msg, key=key)
     return exercise_notes     
     
def log_cycling(username, language, messages_data):
    cycling_msg = messages_data['WORKOUT_LOGGER_PAGE']['CYCLING_TYPE_MSG'][language]
    cycling_dist_msg = messages_data['WORKOUT_LOGGER_PAGE']['CYCLING_DIST_MSG'][language]
    log_cycling_msg = messages_data['WORKOUT_LOGGER_PAGE']['LOG_CYCLING_MSG'][language]
    cycling_type = st.selectbox(cycling_msg, ["cycling_light", "stationary_cycling_light"])
    distance = st.number_input(cycling_dist_msg)
    duration_minutes = log_duration_minutes(language=language, messages_data=messages_data, key='cycling_duration')
    exercise_notes = log_exercise_notes(language=language, messages_data=messages_data, key='cycling_notes')
    if st.button(log_cycling_msg):
        # Prepare workout dictionary
        workout_dct = {'exercise_type': 'cycling', 'exercise_subtype': cycling_type, 'distance': distance, 'duration_minutes': duration_minutes, 'exercise_notes': exercise_notes}
        result = log_user_workout(username=username, language=language, workout_dct=workout_dct)
        if result == 'STATUS_OK':
            st.write('Logged the exercise successfully')
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

    #if st.button(log_cycling_msg):
     #       dbase_wout.add_cycling_session(username, hashed_pwd,
      #                                     distance, duration_minutes,
       #                                    cycling_type, exercise_notes)
            
def log_walking(username, language, messages_data):
    walking_msg = messages_data['WORKOUT_LOGGER_PAGE']['WALKING_TYPE_MSG'][language]
    walking_dist_msg = messages_data['WORKOUT_LOGGER_PAGE']['WALKING_DIST_MSG'][language]
    log_walking_msg = messages_data['WORKOUT_LOGGER_PAGE']['LOG_WALKING_MSG'][language] 
    walking_type = st.selectbox(walking_msg, ["Walking with stroller", "Walking the dog", "Walking 2.0 mph, slow"])
    distance = st.number_input(walking_dist_msg)
    duration_minutes = log_duration_minutes(language=language, messages_data=messages_data, key='walking_duration')
    exercise_notes = log_exercise_notes(language=language, messages_data=messages_data, key='walking_notes')
    if st.button(log_walking_msg):
        #dbase_wout.add_walking_session(username, hashed_pwd,
                                           #distance, duration_minutes,
                                           #walking_type, exercise_notes)
        # Prepare workout dictionary
        workout_dct = {'exercise_type': 'walking', 'exercise_subtype': walking_type, 'distance': distance, 'duration_minutes': duration_minutes, 'exercise_notes': exercise_notes}
        result = log_user_workout(username=username, language=language, workout_dct=workout_dct)
        if result == 'STATUS_OK':
            st.write('Logged the exercise successfully')
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
            
def log_swimming(username, language, messages_data):
    swimming_msg =  messages_data['WORKOUT_LOGGER_PAGE']['SWIMMING_TYPE_MSG'][language]  
    log_swimming_msg = messages_data['WORKOUT_LOGGER_PAGE']['LOG_SWIMMING_MSG'][language]
    swimming_type = st.selectbox(swimming_msg, ["freestyle_fast", "backstroke", "breaststroke", "butterfly"])
    duration_minutes = log_duration_minutes(language=language, messages_data=messages_data, key='swimming_duration')
    exercise_notes = log_exercise_notes(language=language, messages_data=messages_data, key='swimming_notes')
    if st.button(log_swimming_msg):
        #dbase_wout.add_swimming_session(username, hashed_pwd,
                                            #duration_minutes, swimming_type,
                                            #exercise_notes)
        # Prepare workout dictionary
        workout_dct = {'exercise_type': 'swimming', 'exercise_subtype': swimming_type, 'duration_minutes': duration_minutes, 'exercise_notes': exercise_notes}
        result = log_user_workout(username=username, language=language, workout_dct=workout_dct)
        if result == 'STATUS_OK':
            st.write('Logged the exercise successfully')
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
            
def log_running(username, language, messages_data):
     running_msg =  messages_data['WORKOUT_LOGGER_PAGE']['RUNNING_TYPE_MSG'][language]  
     running_dist_msg =  messages_data['WORKOUT_LOGGER_PAGE']['RUNNING_DIST_MSG'][language]
     log_running_msg = messages_data['WORKOUT_LOGGER_PAGE']['LOG_RUNNING_MSG'][language] 
     running_type = st.selectbox(running_msg, ["Slow Running, 6 mph", "Fast Running, 10 mph"])
     distance = st.number_input(running_dist_msg)
     duration_minutes = log_duration_minutes(language=language, messages_data=messages_data, key='running_duration')
     exercise_notes = log_exercise_notes(language=language, messages_data=messages_data, key='running_notes')
     if st.button(log_running_msg):
        #dbase_wout.add_running_session(username, hashed_pwd,
                                           #distance, duration_minutes,
                                           #running_type, exercise_notes)
        # Prepare workout dictionary
        workout_dct = {'exercise_type': 'running', 'exercise_subtype': running_type, 'distance': distance, 'duration_minutes': duration_minutes, 'exercise_notes': exercise_notes}
        result = log_user_workout(username=username, language=language, workout_dct=workout_dct)
        if result == 'STATUS_OK':
            st.write('Logged the exercise successfully')
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
            
def log_aerobics(username, language, messages_data):  
     aerobics_msg =  messages_data['WORKOUT_LOGGER_PAGE']['AEROBICS_TYPE_MSG'][language]  
     log_aerobics_msg = messages_data['WORKOUT_LOGGER_PAGE']['LOG_AEROBICS_MSG'][language] 
     aerobics_type = st.selectbox(aerobics_msg, ["Aerobics, low impact", "Aerobics, high impact", "Aerobics, step aerobics"])
     duration_minutes = log_duration_minutes(language=language, messages_data=messages_data, key='aerobics_duration')
     exercise_notes = log_exercise_notes(language=language, messages_data=messages_data, key='aerobics_notes')
     if st.button(log_aerobics_msg):
        #dbase_wout.add_aerobics_session(username, hashed_pwd,
                                            #duration_minutes, aerobics_type,
                                            #exercise_notes)
        # Prepare workout dictionary
        workout_dct = {'exercise_type': 'swimming', 'exercise_subtype': aerobics_type, 'duration_minutes': duration_minutes, 'exercise_notes': exercise_notes}
        result = log_user_workout(username=username, language=language, workout_dct=workout_dct)
        if result == 'STATUS_OK':
            st.write('Logged the exercise successfully')
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
            
def log_yoga(username, language, messages_data):
     yoga_msg = messages_data['WORKOUT_LOGGER_PAGE']['YOGA_TYPE_MSG'][language]  
     log_yoga_msg = messages_data['WORKOUT_LOGGER_PAGE']['LOG_YOGA_MSG'][language] 
     yoga_type = st.selectbox(yoga_msg, ["Stretching, hatha yoga"])
     duration_minutes = log_duration_minutes(language=language, messages_data=messages_data, key='yoga_duration')
     exercise_notes = log_exercise_notes(language=language, messages_data=messages_data, key='yoga_notes')
     if st.button(log_yoga_msg):
        #dbase_wout.add_yoga_session(username, hashed_pwd,
                                            #duration_minutes, yoga_type,
                                            #exercise_notes)     
        # Prepare workout dictionary
        workout_dct = {'exercise_type': 'yoga', 'exercise_subtype': yoga_type, 'duration_minutes': duration_minutes, 'exercise_notes': exercise_notes}
        result = log_user_workout(username=username, language=language, workout_dct=workout_dct)
        if result == 'STATUS_OK':
            st.write('Logged the exercise successfully')
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
     
def log_workout():
    # Load messages json file
    with open('config/messages.json', 'r', encoding='utf-8') as file:
        messages_data = json.load(file)    

    st.title(messages_data['WORKOUT_LOGGER_PAGE']['TITLE'][user_preferences.mylanguage])

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

    # Initialize Workout Database Class
    #dbase_wout = DatabaseWorkout()

    cycling_msg = messages_data['WORKOUT_LOGGER_PAGE']['CYCLING'][language]
    display_msg(cycling_msg)
    log_cycling(username, language, messages_data)  

    walking_msg = messages_data['WORKOUT_LOGGER_PAGE']['WALKING'][language]
    display_msg(walking_msg)
    log_walking(username, language, messages_data)

    swimming_msg = messages_data['WORKOUT_LOGGER_PAGE']['SWIMMING'][language]
    display_msg(swimming_msg)
    log_swimming(username, language, messages_data)

    running_msg = messages_data['WORKOUT_LOGGER_PAGE']['RUNNING'][language]
    display_msg(running_msg)
    log_running(username, language, messages_data)

    aerobics_msg = messages_data['WORKOUT_LOGGER_PAGE']['AEROBICS'][language]
    display_msg(aerobics_msg)
    log_aerobics(username, language, messages_data)

    strength_training_msg = messages_data['WORKOUT_LOGGER_PAGE']['STRENGTH_TRAINING'][language]
    display_msg(strength_training_msg)
    wip_msg = messages_data['WORKOUT_LOGGER_PAGE']['WIP_MSG'][language]
    st.write(wip_msg)

    yoga_msg = messages_data['WORKOUT_LOGGER_PAGE']['YOGA'][language]
    display_msg(yoga_msg)
    log_yoga(username, language, messages_data)
    
    fitbit_msg = messages_data['WORKOUT_LOGGER_PAGE']['FITBIT'][language]
    display_msg(fitbit_msg)
    wip_msg = messages_data['WORKOUT_LOGGER_PAGE']['WIP_MSG'][language]
    st.write(wip_msg)
    
    upload_img_msg = messages_data['WORKOUT_LOGGER_PAGE']['IMAGE_UPLOAD'][language]
    display_msg(upload_img_msg)
    wip_msg = messages_data['WORKOUT_LOGGER_PAGE']['WIP_MSG'][language]
    st.write(wip_msg)

if __name__ == "__main__":
    log_workout()
