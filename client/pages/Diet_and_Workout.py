import streamlit as st
import sys
import json
import logging
import logging.config
import user_preferences
from interface.interface import is_user_authentic

sys.path.append('client/pages/personal_recommendation')
from client_recommendation import show_personal_recommendation, show_food_recommendation, show_workout_recommendation

def diet_and_workout():
    # Load messages json file
    with open('config/messages.json', 'r', encoding='utf-8') as file:
        messages_data = json.load(file)    

    st.title(messages_data['DIET_WORKOUT_PAGE']['TITLE'][user_preferences.mylanguage])

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

    # Show personal recommendation
    pers_rec_msg = messages_data['DIET_WORKOUT_PAGE']['PERSONAL_RECOMMENDATION_MESSAGE'][language]
    personal_rec_button = st.button(pers_rec_msg)
    if personal_rec_button:
        show_personal_recommendation()

    diet_rec_msg = messages_data['DIET_WORKOUT_PAGE']['DIET_RECOMMENDATION_MESSAGE'][language]
    food_rec_button = st.button(diet_rec_msg)
    if food_rec_button:
        show_food_recommendation()

    workout_rec_msg = messages_data['DIET_WORKOUT_PAGE']['WORKOUT_RECOMMENDATION_MESSAGE'][language]
    workout_rec_button = st.button(workout_rec_msg)
    if workout_rec_button:
        show_workout_recommendation()

if __name__ == "__main__":
    diet_and_workout()
