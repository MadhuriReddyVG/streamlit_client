import requests
import json 
import logging 
import logging.config 

from utils import get_server_ip

def signup_user(username: str, password: str, token: str) -> str:
    """
    Send username, password from the client to the server for signing up and return if signing up is successful or not

    Args:
    - username: The username provided by the user to the client application.
    - password: The password provided by the user to the client application.
    - token: The unique token provided by the Engineering team

    Returns:
    - "STATUS_OK" if successful 
    - "STATUS_FAIL" if user already exists
    """

    # Create the payload with the username, password and the token
    payload = {"username": username, "password": password, "token": token}

    # Prepare the server url
    server_address = get_server_ip()
    url = f"http://{server_address}:5000/signup_user" 

    # Send the post request to the server
    try:
        response = requests.post(url, json=payload)
        
        # Check if the request was successful (status code 2xx)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        #st.error('Failed in HTTP request to logging user credentials: Check if the server is running')
        logging.error('Failed in HTTP request to signup of user: {}'.format(e))
        return 'STATUS_FAIL', 'Sever Not running'

    response_json = json.loads(response.content.decode("utf-8"))
    logging.debug('signup_user response result: {}, message: {}'.format(response_json['result'], response_json['message']))

    return response_json['result'], response_json['message']
    

def login_user(username: str, password: str, token: str) -> (str, str):
    """
    Send username, password from the client to the server and return if authentication is successful or not

    Args:
    - username: The username provided by the user to the client application.
    - password: The password provided by the user to the client application.
    - token: The unique token provided by the Engineering team

    Returns:
    - status ("STATUS_OK" if successful, "STATUS_FAIL" if login is not successful)
    - hashed_pwd: The hashed password; TODO: This needs to be removed
    """

    # Create the payload with the username and the password
    payload = {"username": username, "password": password, "token": token}

    # Prepare the server url
    server_address = get_server_ip()
    url = f"http://{server_address}:5000/login_user" 

    # Send the post request to the server
    try:
        response = requests.post(url, json=payload)
        
        # Check if the request was successful (status code 2xx)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        #st.error('Failed in HTTP request to logging user credentials: Check if the server is running')
        #logging.error('Failed in HTTP request to logging user credentials: {}'.format(e))
        logging.error('Failed in HTTP request to check is user logged in. Server is Down or not responding!')

        return "STATUS_SERVER_DOWN", None

    response_json = json.loads(response.content.decode("utf-8"))
    logging.debug('login_user repsonse result: {}, message: {}'.format(response_json['result'], response_json['message']))

    return response_json['result'], response_json['hashed_pwd']

def logout_user(username: str) -> str:
    """
    Logout user from the app; 

    Args:
    - username: The client's username

    Returns:
    - "STATUS_OK" if successful 
    """
     # Create the payload with the username
    payload = {"username": username}

    # Prepare the server url
    server_address = get_server_ip()
    url = f"http://{server_address}:5000/logout_user" 

    # Send the post request to the server
    try:
        response = requests.post(url, json=payload)
        
        # Check if the request was successful (status code 2xx)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        #st.error('Failed in HTTP request to logging user credentials: Check if the server is running')
        logging.error('Failed in HTTP request to logging out user: {}'.format(e))

    response_json = json.loads(response.content.decode("utf-8"))
    logging.debug('login_user response result: {}'.format(response_json['result']))

    return response_json['result']

#TODO: This is not working with streamlit; Needs to be investigated
def is_user_authentic(username: str) -> str:
    """
    Checks if User has successfully logged in

    Args:
    - username: Username of the client

    Returns:
    - status:
      "STATUS_OK" if user logged in
      "STATUS_NOT_LOGGED_IN" if user is not logged in
      "STATUS_SERVER_DOWN" if server not running
    """
     # Create the payload with the username
    payload = {"username": username}

     # Prepare the server url
    server_address = get_server_ip()
    url = f"http://{server_address}:5000/is_user_authentic" 

    # Send the post request to the server
    try:
        response = requests.post(url, json=payload)
        
        # Check if the request was successful (status code 2xx)
        response.raise_for_status()

        response_json = json.loads(response.content.decode("utf-8"))
        logging.debug('is_user_authentic response result: {}'.format(response_json['result']))

        return response_json['result']

    except requests.exceptions.RequestException as e:
        #st.error('Failed in HTTP request to logging user credentials: Check if the server is running')
        logging.error('Failed in HTTP request to check is user logged in. Server is Down or not responding!')

        return "STATUS_SERVER_DOWN"       

def calculate_cvd_risk(age: int, gender: str, sbp: int, bp_treatment: str, smoker: bool, diabetes: bool, total_chol: int, hdl_chol: int, height_cm: int, weight_kg: int, username: str, hashed_pwd: str) -> (str, str, float, float):
    """
    Calculate the Framingham and SCORE2 Risk Values based on the user (client) input values. Returns the status, Framingham and SCORE2 Risk Values

    Args:
    - age: Age of the user
    - gender: Gender of the user
    - sbp: Systolic Blood Pressure of the user
    - bp_treatment: Whether the user is under BP medications
    - smoker: Whether the user is a smoker
    - diabetes: Whether the user is diabetic
    - total_chol: Total Cholestrol Level of the user
    - hdl_chol: HDL Cholestrol Level of the user
    - height_cm: Height in cms
    - weight_kg: Weight in KGs
    - username: Username of the user; TODO: Needs to be removed
    - hashed_pwd: Hashed password; TODO: Needs to be removed
    
    Returns:
    - status ("STATUS_OK" if successful, "STATUS_FAIL" if the CVD calculation fails")
    - message (Response Message indicating CVD calculation status, useful when calculation fails)
    - Framingham Risk Value (-1 if status is set to STATUS_FAIL)
    - SCORE2 Risk Value (-1 if status is set to STATUS_FAIL)
    """
     # Create the payload with the user provided params
    payload = {"age": age, "gender": gender, "sbp":sbp, "bp_treatment":bp_treatment, "smoker":smoker, "diabetes":diabetes, "total_chol":total_chol, "hdl_chol":hdl_chol, "height_cm":height_cm, "weight_kg":weight_kg, "username": username, "hashed_pwd": hashed_pwd}

    # Prepare the server url
    server_address = get_server_ip()
    url = f"http://{server_address}:5000/calculate_cvd_risk" 

    # Send the post request to the server
    try:
        response = requests.post(url, json=payload)
        
        # Check if the request was successful (status code 2xx)
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        #st.error('Failed in HTTP request to logging user credentials: Check if the server is running')
        logging.error('Failed in HTTP request to calculate CVD Risk: {}'.format(e))

    response_json = json.loads(response.content.decode("utf-8"))
    logging.debug('calculate_cvd_risk response result: {}, message = {}, Framingham Risk: {}, "SCORE2 Risk": {}'.format(response_json['result'], response_json['message'], response_json['framingham_risk'], response_json['score2_risk']))

    return response_json['result'], response_json['message'], response_json['framingham_risk'], response_json['score2_risk']

    
def get_user_details(username: str) -> (str, dict):
    """
    Get all the user details like weight, height, CVD score

    Args:
    - username: Username of the client

    Returns:
    - status:
      "STATUS_OK" if user logged in
      "STATUS_NOT_LOGGED_IN" if user is not logged in
      "STATUS_SERVER_DOWN" if server not running
    - user_details:
      Valid user details if query successful, else None
    """
     # Create the payload with the username
    payload = {"username": username}

     # Prepare the server url
    server_address = get_server_ip()
    url = f"http://{server_address}:5000/get_user_details" 

    # Send the post request to the server
    try:
        response = requests.post(url, json=payload)
        
        # Check if the request was successful (status code 2xx)
        response.raise_for_status()

        response_json = json.loads(response.content.decode("utf-8"))
        logging.debug('get_user_details response result: {}'.format(response_json['result']))
        logging.debug('get_user_details response user_details: {}'.format(response_json['user_details']))

        return response_json['result'], response_json['user_details']

    except requests.exceptions.RequestException as e:
        #st.error('Failed in HTTP request to logging user credentials: Check if the server is running')
        logging.error('Failed in HTTP request to check is user logged in. Server is Down or not responding!')

        return "STATUS_SERVER_DOWN", None       

def get_user_field(username: str, field_dct: dict) -> (str, dict):
    """
    Get a subset of user details from the database

    Args:
    - username: Username of the client
    - field_dct: Dictionary of user field strings whose values have to be populated by the server

    Returns:
    - status:
      "STATUS_OK" if user logged in
      "STATUS_NOT_LOGGED_IN" if user is not logged in
      "STATUS_SERVER_DOWN" if server not running
    - user_fields:
      user fields if query successful, else None
    """
     # Create the payload with the username
    payload = {"username": username, 'field_dct': field_dct}

     # Prepare the server url
    server_address = get_server_ip()
    url = f"http://{server_address}:5000/get_user_fields" 

    # Send the post request to the server
    try:
        response = requests.post(url, json=payload)
        
        # Check if the request was successful (status code 2xx)
        response.raise_for_status()

        response_json = json.loads(response.content.decode("utf-8"))
        logging.debug('get_user_field response result: {}'.format(response_json['result']))
        logging.debug('get_user_field response user_details: {}'.format(response_json['field_dct']))

        return response_json['result'], response_json['field_dct']
    
    except requests.exceptions.RequestException as e:
        #st.error('Failed in HTTP request to logging user credentials: Check if the server is running')
        logging.error('Failed in HTTP request to check is user logged in. Server is Down or not responding!')

        return "STATUS_SERVER_DOWN", None  

def get_food_recommendation(username: str, language: str) -> (str, str):
    """
    Get the food recommendations for a user

    Args:
    - username: Username of the client
    
    Returns:
    - status:
      "STATUS_OK" if user logged in
      "STATUS_NOT_LOGGED_IN" if user is not logged in
      "STATUS_SERVER_DOWN" if server not running
    - food_recommendation:
      food_recommendation if query successful, else None
    """
     # Create the payload with the username
    payload = {"username": username, "language": language}

     # Prepare the server url
    server_address = get_server_ip()
    url = f"http://{server_address}:5000/get_food_recommendation" 

    # Send the post request to the server
    try:
        response = requests.post(url, json=payload)
        
        # Check if the request was successful (status code 2xx)
        response.raise_for_status()

        response_json = json.loads(response.content.decode("utf-8"))
        logging.debug('get_food_recommendation response result: {}'.format(response_json['result']))
        logging.debug('get_food_recommendation response food_recommendation: {}'.format(response_json['food_rec']))

        return response_json['result'], response_json['food_rec']
    
    except requests.exceptions.RequestException as e:
        #st.error('Failed in HTTP request to logging user credentials: Check if the server is running')
        logging.error('Failed in HTTP request to get_food_recommendation. Server is Down or not responding!')

        return "STATUS_SERVER_DOWN", None  

def get_workout_recommendation(username: str, language: str) -> (str, str):
    """
    Get the workout recommendations for a user

    Args:
    - username: Username of the client
    - language: The language of the client
    
    Returns:
    - status:
      "STATUS_OK" if user logged in
      "STATUS_NOT_LOGGED_IN" if user is not logged in
      "STATUS_SERVER_DOWN" if server not running
    - workout_recommendation:
      workout_recommendation if query successful, else None
    """
     # Create the payload with the username
    payload = {"username": username, "language": language}

     # Prepare the server url
    server_address = get_server_ip()
    url = f"http://{server_address}:5000/get_workout_recommendation" 

    # Send the post request to the server
    try:
        response = requests.post(url, json=payload)
        
        # Check if the request was successful (status code 2xx)
        response.raise_for_status()

        response_json = json.loads(response.content.decode("utf-8"))
        logging.debug('get_workout_recommendation response result: {}'.format(response_json['result']))
        logging.debug('get_workout_recommendation response workout_recommendation: {}'.format(response_json['workout_rec']))

        return response_json['result'], response_json['workout_rec']
    
    except requests.exceptions.RequestException as e:
        #st.error('Failed in HTTP request to logging user credentials: Check if the server is running')
        logging.error('Failed in HTTP request to get_workout_recommendation. Server is Down or not responding!')

        return "STATUS_SERVER_DOWN", None  
    
def query_healthbot(username: str, language: str, query: str) -> (str, str):
    """
    Query the HealthBot regarding Heart Health

    Args:
    - username: Username of the client
    - language: The language of the client
    - query: The user query
    
    Returns:
    - status:
      "STATUS_OK" if user logged in
      "STATUS_NOT_LOGGED_IN" if user is not logged in
      "STATUS_SERVER_DOWN" if server not running
    - query response:
      Response to the user query if query was successful, else None
    """
     # Create the payload with the username
    payload = {"username": username, "language": language, "query": query}

     # Prepare the server url
    server_address = get_server_ip()
    url = f"http://{server_address}:5000/query_healthbot" 

    # Send the post request to the server
    try:
        response = requests.post(url, json=payload)
        
        # Check if the request was successful (status code 2xx)
        response.raise_for_status()

        response_json = json.loads(response.content.decode("utf-8"))
        logging.debug('query_healthbot response result: {}'.format(response_json['result']))
        logging.debug('query_healthbot response: {}'.format(response_json['query_response']))

        return response_json['result'], response_json['query_response']
    
    except requests.exceptions.RequestException as e:
        #st.error('Failed in HTTP request to logging user credentials: Check if the server is running')
        logging.error('Failed in HTTP request to query_healthbot. Server is Down or not responding!')

        return "STATUS_SERVER_DOWN", None  
    
def log_user_workout(username: str, language: str, workout_dct: dict) -> str:
    """
    Log the user workout

    Args:
    - username: Username of the client
    - language: The language of the client
    - workout_dct: The user workout details stored in a dictionary
    
    Returns:
    - status:
      "STATUS_OK" if user logged in
      "STATUS_NOT_LOGGED_IN" if user is not logged in
      "STATUS_SERVER_DOWN" if server not running
    - query response:
      Response to the user query if query was successful, else None
    """
     # Create the payload with the username
    payload = {"username": username, "language": language, "workout_dct": workout_dct}

     # Prepare the server url
    server_address = get_server_ip()
    url = f"http://{server_address}:5000/log_user_workout" 

    # Send the post request to the server
    try:
        response = requests.post(url, json=payload)
        
        # Check if the request was successful (status code 2xx)
        response.raise_for_status()

        response_json = json.loads(response.content.decode("utf-8"))
        logging.debug('log_user_workout response result: {}'.format(response_json['result']))

        return response_json['result']
    
    except requests.exceptions.RequestException as e:
        #st.error('Failed in HTTP request to logging user credentials: Check if the server is running')
        logging.error('Failed in HTTP request to query_healthbot. Server is Down or not responding!')

        return "STATUS_SERVER_DOWN"

def get_fitbit_data(username: str, fitbit_access_token: str, activity_type: str, base_date: str, end_date: str) -> list:
    """
    Get the fitbit data of the user

    Args:
    - username: Username of the client
    - fitbit_access_token: Fitbit access token of the user
    - activity_type: The activity type. Currently supported:
      sleep
      resting heart rate
    - base_date: The starting date from which data is required
    - end_date: The ending date till which data is required
    
    Returns:
    - status:
      "STATUS_OK" if successful in getting fitbit data
      "STATUS_NOT_LOGGED_IN" if user is not logged in
      "STATUS_SERVER_DOWN" if server not running
      "STATUS_FAIL" if failed to get data from fitbit server
    - fitbit activity data:
      Fitbit activity data of the user, if query was successful, else None
    """
     # Create the payload with the username
    payload = {"username": username, "fitbit_access_token": fitbit_access_token, "activity_type": activity_type, "base_date": base_date, 'end_date': end_date}

     # Prepare the server url
    server_address = get_server_ip()
    url = f"http://{server_address}:5000/get_fitbit_data" 

    # Send the post request to the server
    try:
        response = requests.post(url, json=payload)
        
        # Check if the request was successful (status code 2xx)
        response.raise_for_status()

        response_json = json.loads(response.content.decode("utf-8"))
        logging.debug('log_user_workout response result: {}'.format(response_json['result']))

        return response_json['result'], response_json['fitbit_data']
    
    except requests.exceptions.RequestException as e:
        #st.error('Failed in HTTP request to logging user credentials: Check if the server is running')
        logging.error('Failed in HTTP request to query_healthbot. Server is Down or not responding!')

        return "STATUS_SERVER_DOWN", None
    
def get_user_workout(username: str) -> (str, list):
    """
    Get the workout details of the user

    Args:
    - username: Username of the client
    
    Returns:
    - status:
      "STATUS_OK" if successful in getting fitbit data
      "STATUS_NOT_LOGGED_IN" if user is not logged in
      "STATUS_SERVER_DOWN" if server not running
      "STATUS_FAIL" if failed to get data from fitbit server
    - workout data:
      Workout data details of the user, if query was successful, else None
    """
     # Create the payload with the username
    payload = {"username": username}

     # Prepare the server url
    server_address = get_server_ip()
    url = f"http://{server_address}:5000/get_user_workout" 

    # Send the post request to the server
    try:
        response = requests.post(url, json=payload)
        
        # Check if the request was successful (status code 2xx)
        response.raise_for_status()

        response_json = json.loads(response.content.decode("utf-8"))
        logging.debug('log_user_workout response result: {}'.format(response_json['result']))

        return response_json['result'], response_json['workout_details']
    
    except requests.exceptions.RequestException as e:
        #st.error('Failed in HTTP request to logging user credentials: Check if the server is running')
        logging.error('Failed in HTTP request to get_workout_details. Server is Down or not responding!')

        return "STATUS_SERVER_DOWN", None