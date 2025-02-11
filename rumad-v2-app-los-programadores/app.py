import streamlit as st
import pandas as pd
import requests

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.warning("You must log in to access this application.")
    st.session_state["current_page"] = "login"
    st.stop()
host = 'http://127.0.0.1:5000'

def fetchAllMeetings():

    st.write("All Meetings")

    response = requests.get(host + '/losprogramadores/meeting').json()

    df = pd.DataFrame(response)


    if 'mid' in df.columns:
        df = df.drop(columns=['mid'])

    df.columns = ['Code', 'Days', 'Start_Time', 'End_Time']

    st.dataframe(df, height=400)

def fetchAllRoom():
    st.write("All Rooms")

    response = requests.get(host + '/losprogramadores/room').json()

    df = pd.DataFrame(response)

    if 'rid' in df.columns:
        df = df.drop(columns=['rid'])

    df.columns = ['Building', 'Capacity', 'Room_Number']

    st.dataframe(df, height=400)

def fetchAllSections():
    st.write("All Sections")

    response = requests.get(host + '/losprogramadores/section').json()

    df = pd.DataFrame(response)

    if 'sid' in df.columns:
        df = df.drop(columns=['sid'])
    if 'room_id' in df.columns:
        df = df.drop(columns=['room_id'])
    if 'meeting_id' in df.columns:
        df = df.drop(columns=['meeting_id'])
    if 'class_id' in df.columns:
        df = df.drop(columns=['class_id'])


    df.columns = ['Capacity', 'Semester', 'Years']

    st.dataframe(df, height=400)

fetchAllMeetings()
fetchAllRoom()
fetchAllSections()
