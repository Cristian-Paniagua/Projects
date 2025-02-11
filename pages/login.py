import streamlit as st
import requests


#host = "http://127.0.0.1:5000/losprogramadores"

host = "http://databasephase1-e3daa06311f4.herokuapp.com/losprogramadores"


def login():
    st.title("Login")
    st.subheader("Welcome!")


    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", placeholder="Enter your password", type="password")


    if st.button("Login"):
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            try:

                response = requests.post(f"{host}/login", json={"username": username, "password": password})
                if response.status_code == 200:

                    data = response.json()
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = data["username"]
                    st.session_state["current_page"] = "app"
                    st.session_state["uid"] = data["uid"]
                    st.success(f"Welcome, {data['username']}!")
                else:
                    st.error("Invalid username or password.")
            except Exception as e:
                st.error(f"Error connecting to the server: {str(e)}")




def app():
    st.title("Main Application")
    st.success(f"Welcome, {st.session_state['username']}!")


    st.write("This is the main content of the application.")


    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["current_page"] = "login"


def authentication_required():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("You must log in to access this page.")
        st.session_state["current_page"] = "login"
        login()
        st.stop()


def main():

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "login"


    if st.session_state["current_page"] == "login":
        login()
    elif st.session_state["current_page"] == "app":
        authentication_required()
        app()

def require_login():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("You must log in to access this page.")
        st.session_state["current_page"] = "login"
        login()
        st.stop()


if __name__ == "__main__":
    main()
