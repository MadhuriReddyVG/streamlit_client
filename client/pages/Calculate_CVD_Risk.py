import streamlit as st
from st_circular_progress import CircularProgress
import pandas as pd
import plotly.express as px 
import plotly.graph_objects as go
import logging
import logging.config
import json

import user_preferences
from interface.interface import is_user_authentic, calculate_cvd_risk
from utils import start_display_wip, stop_display_wip, get_error_reason

def display_cvd_risk(results):
    # https://discuss.streamlit.io/t/how-to-create-a-horizontal-bar-chart-with-streamlit/18162
    data = pd.DataFrame(results, columns=["Risk Evaluation Method", "Percentage"])
    #st.bar_chart(data.set_index("Category")["Percentage"], use_container_width=True, color=data["Color"])
    #fig=px.bar(data,x='Percentage',y='Risk Evaluation Method', orientation='h', text_auto=True, color='Percentage')
    #st.write(fig)

    logging.debug('CVD results: {}'.format(results))

    fig1 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = results[0][1],
        title = {'text': "Framingham Risk Percent"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': 'blue'},
        }))
    st.plotly_chart(fig1)
    
    fig2 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = results[1][1],
        title = {'text': "SCORE2 Risk percent"},
        domain = {'x': [0, 1], 'y': [0, 1]},
        gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': 'green'},
        }))
    st.plotly_chart(fig2)

    # https://docs.streamlit.io/library/api-reference/data/st.dataframe
    st.dataframe(data, use_container_width=True) 

    st.markdown(
            "<p style='text-align:center; font-size:24px; font-weight:bold;'>Checkout Diet and Workout page on the left for improving Heart Health...</p>",
            unsafe_allow_html=True
    )       

def calculate_risk(age, gender, sbp, bp_treatment, smoker, diabetes, total_chol, hdl_chol, height_cm, weight_kg, username, hashed_pwd):
 result, message, framingham_risk, score2_risk = calculate_cvd_risk(age, gender, sbp, bp_treatment, smoker, diabetes, total_chol, hdl_chol, height_cm, weight_kg, username, hashed_pwd)

 return result, message, framingham_risk, score2_risk

def calculate_and_display_risk(messages_data, age, gender,
                                 sbp, bp_treatment,
                                 smoker, diabetes,
                                 total_chol, hdl_chol,
                                 height_cm, weight_kg):
    language = user_preferences.mylanguage

    logging.debug("height_cm={}, weight_kg={}, age = {}".format(height_cm, weight_kg, age))

    # Initialize Risks Levels to invalid values
    framingham_risk = -1
    score2_risk = -1

    risk_button_msg = messages_data['CALCULATE_CVD_PAGE']['RISK_BUTTON_MSG'][language]
    risk_button = st.button(risk_button_msg)

    # Input fields based on the selected method
    if risk_button:    
        wip_msg = messages_data['CALCULATE_CVD_PAGE']['CALCULATING_CVD_RISK'][language]         
        progress_bar, status_text = start_display_wip(wip_msg)
        username = user_preferences.username
        hashed_pwd = user_preferences.hashed_pwd
        logging.debug('username ={}, hashed_pwd={}'.format(username, hashed_pwd))
        result, message, framingham_risk, score2_risk = calculate_risk(age, gender, sbp, bp_treatment, smoker, diabetes, total_chol, hdl_chol, height_cm, weight_kg, username, hashed_pwd)
        stop_display_wip(progress_bar, status_text)

        if result != 'STATUS_OK':  
            error_reason =  get_error_reason(result=result)     
            st.error(messages_data['ERROR_MESSAGES'][error_reason][user_preferences.mylanguage])
        else:
            results = [
                ("Framingham Risk", framingham_risk),
                ("SCORE2 Risk", score2_risk)           
            ]                       
            display_cvd_risk(results=results)
            
def hearthealthapp():
    # Load messages json file
    with open('config/messages.json', 'r', encoding='utf-8') as file:
        messages_data = json.load(file)    

    st.title(messages_data['CALCULATE_CVD_PAGE']['TITLE'][user_preferences.mylanguage])

    # Check if user has logged in, to access this page
    result = is_user_authentic(user_preferences.username)
    if result != 'STATUS_OK':
        error_reason =  get_error_reason(result=result)   
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

        logging.debug('CVD Input Params types: age:{}, gender:{}, sbp:{}, bp_treatment:{}, smoker:{}, diabetes:{}, total_chol:{}, hdl_chol:{}, height_cm:{}, weight_kg:{}'.format(type(age), type(gender), type(sbp), type(bp_treatment), type(smoker), type(diabetes), type(total_chol), type(hdl_chol), type(height_cm), type(weight_kg)))
                
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
        
    calculate_and_display_risk(messages_data, age, gender, sbp, bp_treatment, smoker, diabetes, total_chol, hdl_chol, height_cm, weight_kg)
             
if __name__ == "__main__":
    hearthealthapp()   
