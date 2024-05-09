import streamlit as st
import pandas as pd
import math
import plotly.express as px 
import logging
import logging.config
import json

import user_preferences
from interface.interface import is_user_authentic, calculate_cvd_risk

# Start Display Work in Progress
def start_display_wip():        
    # Display "Calculating Heart Age" message during computation
    progress_bar = st.progress(0)
    status_text = st.empty()
    #status_text.text("Calculating Heart Age...")

    if user_preferences.mylanguage == "English":
        # Styling for the message
        status_text.markdown(
                "<p style='text-align:center; font-size:24px; font-weight:bold;'>Calculating Heart Age...</p>",
                unsafe_allow_html=True
        )
    elif user_preferences.mylanguage == "Deutsch":
        # Styling for the message
        status_text.markdown(
                "<p style='text-align:center; font-size:24px; font-weight:bold;'>Berechnung des Herzalters...</p>",
                unsafe_allow_html=True
        )

    return progress_bar, status_text

def stop_display_wip(progress_bar, status_text):
    # Update UI after computation
    progress_bar.empty()
    status_text.empty()

def display_results(results):
    # https://discuss.streamlit.io/t/how-to-create-a-horizontal-bar-chart-with-streamlit/18162
    data = pd.DataFrame(results, columns=["Risk Evaluation Method", "Percentage"])
    #st.bar_chart(data.set_index("Category")["Percentage"], use_container_width=True, color=data["Color"])
    fig=px.bar(data,x='Percentage',y='Risk Evaluation Method', orientation='h', text_auto=True, color='Percentage')
    st.write(fig)

    # https://docs.streamlit.io/library/api-reference/data/st.dataframe
    st.dataframe(data, use_container_width=True) 

    st.markdown(
            "<p style='text-align:center; font-size:24px; font-weight:bold;'>Checkout Diet and Workout page on the left for improving Heart Health...</p>",
            unsafe_allow_html=True
    )       

def calculate_and_display_risk(age, gender,
                                 sbp, bp_treatment,
                                 smoker, diabetes,
                                 total_chol, hdl_chol,
                                 height_cm, weight_kg):
    if user_preferences.mylanguage == "English":
        st.title("Heart Risk Score Calculator")
    elif user_preferences.mylanguage == "Deutsch":
        st.title("Rechner für den Herzrisiko-Score")
    
    logging.debug("height_cm={}, weight_kg={}, age = {}".format(height_cm, weight_kg, age))

    # Initialize Risks Levels to invalid values
    framingham_risk = -1
    score2_risk = -1

    if user_preferences.mylanguage == "English":
        risk_button = st.button("Calculate Risk")
    elif user_preferences.mylanguage == "Deutsch":
        risk_button = st.button("Risiko berechnen")

    # Input fields based on the selected method
    if risk_button:                
        progress_bar, status_text = start_display_wip()
        username = user_preferences.username
        hashed_pwd = user_preferences.hashed_pwd
        logging.debug('username ={}, hashed_pwd={}'.format(username, hashed_pwd))
        result, message, framingham_risk, score2_risk = calculate_cvd_risk(age, gender, sbp, bp_treatment, smoker, diabetes, total_chol, hdl_chol, height_cm, weight_kg, username, hashed_pwd)
        stop_display_wip(progress_bar, status_text)

        if result != 'STATUS_OK':
            if result == "STATUS_NOT_LOGGED_IN":
                error_reason = 'USER_NOT_LOGGED_IN'     
            elif result == 'STATUS_SERVER_DOWN':
                error_reason = 'SERVER_DOWN'
            else:
                error_reason = 'GENERIC_ERROR'       
            st.error(messages_data['ERROR_MESSAGES'][error_reason][user_preferences.mylanguage])
        else:
            results = [
                ("Framingham Risk", framingham_risk),
                ("SCORE2 Risk", score2_risk)           
            ]                       
            display_results(results=results)
            
def hearthealthapp():
    # Load messages json file
    with open('config/messages.json', 'r', encoding='utf-8') as file:
        messages_data = json.load(file)    

    st.title(messages_data['TITLE_MESSAGES']['CALCULATE_CVD_PAGE'][user_preferences.mylanguage])

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

    if user_preferences.mylanguage == "English":
        # User inputs common to both methods
        age = st.slider("Age", min_value=30, max_value=80, value=40)
        gender = st.radio("Gender", ["Male", "Female"])
        sbp = st.number_input("Systolic Blood Pressure (mmHg)", min_value=80, max_value=200, value=120)
        bp_treatment = st.radio("Blood Pressure medical treatment", ["Yes", "No"])
        smoker = st.checkbox("Smoker")
        logging.debug("****smoker={}******".format(smoker))
        diabetes = st.checkbox("Diabetes")

        # User inputs for cholestrol
        total_chol = st.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=400, value=200)
        hdl_chol = st.number_input("HDL Cholesterol (mg/dL)", min_value=20, max_value=150, value=50)   

        # User inputs for height and weight
        height_cm = st.number_input("Height in cms", value=160)
        weight_kg = st.number_input("Weight in kgs", value=60)  

        #TODO: Revisit this and fix cleanly
        logging.debug("Blood Pressure Treatment = {}".format(bp_treatment))
        #Change bp_treatment from Yes/No to True/False
        if bp_treatment == "Yes":
            bp_treatment = "True"
        else:
            bp_treatment = "False"        
    elif user_preferences.mylanguage == "Deutsch":
        # User inputs common to both methods
        age = st.slider("Alter", min_value=30, max_value=80, value=40)

        gender = st.radio("Geschlecht", ["Männlich", "Weiblich"])
        if gender == "Männlich":
            gender = "Male"
        else:
            gender = "Female"
            
        sbp = st.number_input("Systolischer Blutdruck (mmHg)", min_value=80, max_value=200, value=120)

        bp_treatment = st.radio("Medizinische Behandlung des Blutdrucks", ["Ja", "Nein"])
        #Change bp_treatment from Yes/No to True/False
        if bp_treatment == "Ja":
            bp_treatment = "True"
        else:
            bp_treatment = "False"
         #TODO: Revisit this and fix cleanly
        logging.debug("Blood Pressure Treatment = {}".format(bp_treatment))

        smoker = st.checkbox("Raucher")
        diabetes = st.checkbox("Diabetes")

        # User inputs for cholestrol
        total_chol = st.number_input("Gesamtcholesterin (mg/dL)", min_value=100, max_value=400, value=200)
        hdl_chol = st.number_input("HDL-Cholesterin (mg/dL)", min_value=20, max_value=150, value=50)   

        # User inputs for height and weight
        height_cm = st.number_input("Höhe in cm", value=160)
        weight_kg = st.number_input("Gewicht in kg", value=60)         
        
    calculate_and_display_risk(age, gender, sbp, bp_treatment, smoker, diabetes, total_chol, hdl_chol, height_cm, weight_kg)
             
if __name__ == "__main__":
    hearthealthapp()   
