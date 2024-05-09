import streamlit as st

import logging
import logging.config
import pandas as pd
import json

import user_preferences
from utils import get_error_reason
from interface.interface import is_user_authentic, get_user_workout

def create_datetime_column(df):
    # Concatenate 'date' and 'time_of_day' columns into a new column
    df['datetime_combined'] = df['current_date'] + ' ' + df['time_of_day']

    # Convert 'datetime_combined' column to datetime format if needed
    df['datetime_combined'] = pd.to_datetime(df['datetime_combined'], format='%d.%m.%Y %H:%M:%S')

def get_workout_dataframe(workout_list):
    df = pd.DataFrame(workout_list)

    #Drop the _id and unique_id columns
    #df.drop(columns=['_id', 'unique_id'], inplace=True)

    #Club date and time into a single column
    create_datetime_column(df)

    return df

def daily_dashboard(username, language):
     # Load messages json file
    with open('config/messages.json', 'r', encoding='utf-8') as file:
        messages_data = json.load(file)   
 
    result, daily_lst = get_user_workout(username)
    if result != 'STATUS_OK':     
        error_reason =  get_error_reason(result=result)
        nouser_details_text = messages_data['ERROR_MESSAGES'][error_reason][language]
        logging.error('Failed in daily_dashboard with error: {}'.format(nouser_details_text))
        st.markdown(f"<p style='white-space: pre-line; color:red;'>{nouser_details_text}</p>", unsafe_allow_html=True)
        return     
    
    logging.debug('daily workout list: {}'.format(daily_lst))
    #st.write(daily_lst)

    df = get_workout_dataframe(daily_lst)
    #st.write(df.head())
    logging.debug('df = {}'.format(df))

    # Calculate some metrics
    recent_cal_burnt = df.sort_values(by = 'datetime_combined', ascending=False)['calories_burnt'].iloc[0]
    delta_cal_burnt = recent_cal_burnt - df.sort_values(by = 'datetime_combined', ascending=False)['calories_burnt'].iloc[1]

    col1, col2 = st.columns([1.5, 1.5])

    with col1:
        #st.line_chart(df[['calories_burnt']])
        #st.line_chart(data=df.set_index('datetime_combined')[['calories_burnt']])
        st.line_chart(data=df, x="datetime_combined", y="calories_burnt")

    #col2.subheader("Sweat points 💦")
    col2.subheader("Calories Burnt 🧘🏻‍♀️")
    col2.metric("Recent", recent_cal_burnt, str(delta_cal_burnt))
    col2.metric("Average", df['calories_burnt'].mean().round(2))
    col2.write("🏅 Best day: " +str(df.loc[df['calories_burnt'].idxmax()]['datetime_combined']) + " with " + str(df['calories_burnt'].max()) + " calories burnt")
    col2.write("Total number  of workouts: " + str(len(df)))

    

    st.write("---")
    ################################################################################################################
    
    col1, col2 = st.columns([3, 1])
    col1.subheader("Overview")
    with col1:
        asc = st.radio( "Sort by: ", ["newest", "oldest"], horizontal = True)

    df_ov = df[['duration_minutes', 'exercise_type', 'distance', 'calories_burnt', 'datetime_combined']]
    if asc == 'newest':
        #col1.dataframe(df_ov.sort_values(by = 'datetime_combined', ascending=False))
        st.dataframe(df_ov.sort_values(by = 'datetime_combined', ascending=False), use_container_width=True)
    else:
        #col1.dataframe(df_ov.sort_values(by = 'datetime_combined', ascending=True))
        st.dataframe(df_ov.sort_values(by = 'datetime_combined', ascending=True), use_container_width=True)
        
    #TODO: Need to enable the Stats column
    #col1, col2 = st.columns([3, 1])
    #col1.subheader("Stats")    

    st.write("---")
    ################################################################################################################



def workout_tracker():
     # Load messages json file
    with open('config/messages.json', 'r', encoding='utf-8') as file:
        messages_data = json.load(file)    

    st.title(messages_data['WORKOUT_TRACKER_PAGE']['TITLE'][user_preferences.mylanguage])

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

    daily_dashboard(username, language)
    
if __name__ == "__main__":
    workout_tracker()