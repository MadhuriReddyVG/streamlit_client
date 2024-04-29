import streamlit as st
import pandas as pd
from interface.interface import signup_user, login_user, logout_user
import user_preferences
import logging 
import logging.config

def main():
	# Set the logging framework
	logging.config.fileConfig(fname='config.ini', disable_existing_loggers=False)
	# Get the logger specified in the file
	logger = logging.getLogger(__name__)
	logger.debug('This is a debug message')

	lang_menu = ["English","Deutsch"]
	lang_choice = st.sidebar.selectbox("Language", lang_menu)
	user_preferences.mylanguage = lang_choice

	if lang_choice == "English":
		st.write("# Welcome to Heart Health App! 👋") 
		st.markdown(
			"""
        	Heart Health App is an AI based application built for improving the heart Health 
        	of the Users and towards a better lifestyle.
        	**👈  Login/Signup from the sidebar** to explore the
        	different features of the Heart Health App!       
    		"""
    	)
		
		#st.write("## Heart Health App Features")

		menu = ["Home","Login","SignUp", "Logout"]
		choice = st.sidebar.selectbox("Menu",menu)

		if choice == "Home":
			st.subheader("Home")
		elif choice == "Login":
			st.subheader("Login Section")
			username = st.sidebar.text_input("User Name")
			password = st.sidebar.text_input("Password",type='password')
			if st.sidebar.checkbox("Login"):
				result, hashed_pwd = login_user(username=username, password=password)
				if result == 'STATUS_OK':
					#user_preferences.user_loggedin = True
					user_preferences.username = username
					user_preferences.hashed_pwd = hashed_pwd
					st.success("Logged In as {}".format(username))					
				else:
					logger.warning("Incorrect Username/Password in main app")
					st.warning("Incorrect Username/Password")
		elif choice == "Logout":
				username = user_preferences.username
				logging.debug('Logging out the user {}'.format(username))
				result = logout_user(username=username)
				if result == 'STATUS_OK':
					#user_preferences.user_loggedin = False
					st.success("Logged Out Successfully")
					user_preferences.username = None
					user_preferences.hashed_pwd = None
				else:
					logger.warning("Logout failure")
					st.warning("Logout failure")
		elif choice == "SignUp":
			st.subheader("Create New Account")
			new_user = st.text_input("Username")
			new_password = st.text_input("Password",type='password')	
			if st.button("Signup"):
				result = signup_user(username=new_user, password=new_password)
				if result == 'STATUS_OK':
					st.success("You have successfully created a valid Account")
					st.info("Go to Login Menu to login")
				else:
					logger.warning("Username already Exists. Try with a different  Username in main app")
					st.warning("Username already Exists. Try with a different  Username in main app")
	elif lang_choice == "Deutsch":
		st.write("# Willkommen in der Herzgesundheitsapp! 👋")
		st.markdown(
			"""
        	Die Heart Health App ist eine KI-basierte Anwendung, die zur Verbesserung der Herzgesundheit 
			der Benutzer und für einen besseren Lebensstil entwickelt wurde.
        	**👈  Anmelden Sie sich über die Seitenleiste an/registrieren Sie sich** 
			um die verschiedenen Funktionen der Heart Health App zu erkunden!       
    		"""
    	)

		#st.write("## Heart Health App Features")

		menu = ["Startseite","Anmeldung","Melden", "Ausloggen"]
		choice = st.sidebar.selectbox("Menu",menu)

		if choice == "Startseite":
			st.subheader("Startseite")
		elif choice == "Anmeldung":
			st.subheader("Anmeldung Section")
			username = st.sidebar.text_input("Nutzername")
			password = st.sidebar.text_input("Passwort",type='password')
			if st.sidebar.checkbox("Anmeldung"):
				result = login_user(username=username, password=password)
				if result == 'STATUS_OK':				
					st.success("Angemeldet als {}".format(username))
				else:
					logger.warning("Incorrect Username/Password in main app")
					st.warning("Falscher Benutzername / Passwort")
		elif choice == "Ausloggen":
			username = user_preferences.username
			logging.debug('Logging out the user {}'.format(username))
			result = logout_user(username)
			if result == 'STATUS_OK':
				st.success("Logged Out Successfully")
			else:
				logger.warning("Erfolgreich abgemeldet")
				st.warning("Erfolgreich abgemeldet")
		elif choice == "Melden":
			st.subheader("Neuen Account erstellen")
			new_user = st.text_input("Nutzername")
			new_password = st.text_input("Passwort",type='password')

			if st.button("Melden"):
				result = signup_user(username=new_user, password=new_password)
				if result == 'STATUS_OK':
					st.success("Sie haben erfolgreich ein gültiges Konto erstellt")
					st.info("Gehen Sie zum Anmeldemenü, um sich anzumelden")
				else:
					logger.warning("Benutzername existiert bereits. Versuchen Sie es mit einem anderen Benutzernamen in der Haupt-App")
					st.warning("Benutzername existiert bereits. Versuchen Sie es mit einem anderen Benutzernamen in der Haupt-App")

if __name__ == '__main__':
	main()
