
import streamlit as st
import re
import json

import user_preferences
from interface.interface import is_user_authentic

mcq_list = [{'question': 'What are some factors that can affect heart health?', 'option_1': 'a) Genetics', 'option_2': 'b) Diet', 'option_3': 'c) Exercise', 'option_4': 'd) All of the above', 'answer': 'd) All of the above'}, {'question': "Which type of cholesterol is considered 'bad'?", 'option_1': 'a) HDL cholesterol', 'option_2': 'b) Total cholesterol', 'option_3': 'c) LDL cholesterol', 'option_4': 'd) None of the above', 'answer': 'c) LDL cholesterol'}, {'question': 'What are the optimal levels of LDL cholesterol for adults?', 'option_1': 'a) Less than 100 mg/dL', 'option_2': 'b) Less than 200 mg/dL', 'option_3': 'c) 60 mg/dL or higher', 'option_4': 'd) None of the above', 'answer': 'a) Less than 100 mg/dL'}, {'question': 'What is the normal range of systolic pressure for adults?', 'option_1': 'a) Less than 120 mmHg', 'option_2': 'b) Less than 80 mmHg', 'option_3': 'c) Less than 140 mg/dL', 'option_4': 'd) None of the above', 'answer': 'a) Less than 120 mmHg'}, {'question': 'What is the normal range of fasting blood sugar for adults?', 'option_1': 'a) 70 to 99 mg/dL', 'option_2': 'b) Less than 120 mmHg', 'option_3': 'c) Less than 80 mmHg', 'option_4': 'd) None of the above', 'answer': 'a) 70 to 99 mg/dL'}]

# Initialize session state variables if they don't exist yet
if "current_question" not in st.session_state:
    st.session_state.answers = {}
    st.session_state.current_question = 0
    st.session_state.questions = []
    st.session_state.right_answers = 0
    st.session_state.wrong_answers = 0

# Define a function to display the current question and options
def display_question(mcq_list):
    if st.session_state.current_question >= len(mcq_list):
        st.write("Reached the end of quiz.")
        st.write(f"Right answers: {st.session_state.right_answers}")
        st.write(f"Wrong answers: {st.session_state.wrong_answers}")

        st.session_state.answers = {}
        st.session_state.current_question = 0
        st.session_state.questions = []
        st.session_state.right_answers = 0
        st.session_state.wrong_answers = 0

        return

    pattern = re.compile(r'\b\w\) (.+)$')

    # Handle first case
    if len(st.session_state.questions) == 0:
        try:
            #first_question = get_quiz_from_topic(topic, api_key)
            first_question = mcq_list[st.session_state.current_question]
        except:
            st.error(
                "Error in fetching the question. "                
            )
            return
        st.session_state.questions.append(first_question)

    # Disable the submit button if the user has already answered this question
    submit_button_disabled = st.session_state.current_question in st.session_state.answers

    # Get the current question from the questions list
    question = st.session_state.questions[st.session_state.current_question]

    # Display the question prompt
    st.write(f"{st.session_state.current_question + 1}. {question['question']}")

    # Use an empty placeholder to display the radio button options
    options = st.empty()

    # Display the radio button options and wait for the user to select an answer
    q_options = [
        pattern.search(question['option_1']).group(1),
        pattern.search(question['option_2']).group(1),
        pattern.search(question['option_3']).group(1),
        pattern.search(question['option_4']).group(1)
    ]
    user_answer = options.radio("Your answer:", q_options, key=st.session_state.current_question)

    # Display the submit button and disable it if necessary
    submit_button = st.button("Submit", disabled=submit_button_disabled)

    # If the user has already answered this question, display their previous answer
    if st.session_state.current_question in st.session_state.answers:
        index = st.session_state.answers[st.session_state.current_question]
        options.radio(
            "Your answer:",
            q_options,
            key=float(st.session_state.current_question),
            index=index,
        )

    # If the user clicks the submit button, check their answer and show the explanation
    if submit_button:
        # Record the user's answer in the session state
        st.session_state.answers[st.session_state.current_question] = q_options.index(user_answer)

        # Correct Answer
        ans_str = pattern.search(question['answer']).group(1)

        # Check if the user's answer is correct and update the score
        if user_answer == ans_str:
            st.write("Correct!")
            st.session_state.right_answers += 1
        else:
            st.write(f"Sorry, the correct answer was {question['answer']}.")
            st.session_state.wrong_answers += 1

        # Show an expander with the explanation of the correct answer
        #with st.expander("Explanation"):
            #st.write(question["explanation"])

    # Display the current score
    #st.write(f"Right answers: {st.session_state.right_answers}")
    #st.write(f"Wrong answers: {st.session_state.wrong_answers}")


# Define a function to go to the next question
def next_question(mcq_list):
    # Move to the next question in the questions list
    st.session_state.current_question += 1

    # If we've reached the end of the questions list, get a new question
    if st.session_state.current_question > len(st.session_state.questions) - 1:
        try:
            #next_question = get_quiz_from_topic(topic, api_key)
            #if st.session_state.current_question >= len(mcq_list):
             #   st.write("Reached the end of quiz.")
             #   st.write(f"Right answers: {st.session_state.right_answers}")
             #   st.write(f"Wrong answers: {st.session_state.wrong_answers}")

            next_question = mcq_list[st.session_state.current_question]
        except:
            #st.session_state.current_question -= 1
            return
        st.session_state.questions.append(next_question)


# Define a function to go to the previous question
def prev_question():
    # Move to the previous question in the questions list
    if st.session_state.current_question > 0:
        st.session_state.current_question -= 1
        st.session_state.explanation = None
 
def do_quiz():
    # Load messages json file
    with open('config/messages.json', 'r', encoding='utf-8') as file:
        messages_data = json.load(file)    

    st.title(messages_data['HEARTHEALTH_QUIZ_PAGE']['TITLE'][user_preferences.mylanguage])

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
    st.title('')

    #output_content = generate_mcqs()

    # Parse the string into list of dictionaries
    #mcq_list = parse_json_like(output_content)
    print(mcq_list)

    #do_quiz(mcq_list)

    # Create a 3-column layout for the Prev/Next buttons and the question display
    col1, col2, col3 = st.columns([1, 6, 1])

    # Add a Prev button to the left column that goes to the previous question
    with col1:
        if col1.button("Prev"):
            prev_question()

    # Add a Next button to the right column that goes to the next question
    with col3:
        if col3.button("Next"):
            next_question(mcq_list)

    # Display the actual quiz question
    with col2:
        display_question(mcq_list)


if __name__ == "__main__":
    do_quiz()