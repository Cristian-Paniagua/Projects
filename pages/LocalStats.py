import json
import math

import streamlit as st
import pandas as pd
import requests
from auth import require_login

host = 'http://databasephase1-e3daa06311f4.herokuapp.com'

box1, box2, box3 = st.columns(3)

with box1:
    if st.button("Local Stats"):
        st.switch_page("LocalStats.py")
with box2:
    if st.button("RUM Courses"):
        st.switch_page("pages/Classes.py")
with box3:
    if st.button("Global Stats"):
        st.switch_page("pages/GlobalStats.py")

st.write("")
st.write("")
st.write("")

def render():
    require_login()
    if "uid" not in st.session_state:
        st.error("You need to log in first.")
        return

    roomsList = requests.get(host + '/losprogramadores/room').json()
    sectionList = requests.get(host + '/losprogramadores/section').json()

    years = set()
    semester = set()
    buildings = set()
    classIds = set()
    for room in roomsList:
      buildings.add(room['building'])
      classIds.add(room['rid'])

    for section in sectionList:
        years.add(section['years'])
        semester.add(section['semester'])

    selectBuilding = st.selectbox(
        "Choose Building for Graphs",
        buildings,
    )

    st.write("You selected:", selectBuilding)


    st.write("")
    st.write("") #Line to create space in page
    st.write("")

    fetchTopThreeCap(selectBuilding, st.session_state["uid"])

    st.write("")
    st.write("")  #Lines to create space in page
    st.write("")

    fetchTopThreeRatio(selectBuilding, st.session_state["uid"])

    st.write("")
    st.write("")
    st.write("")

    selectIds = st.selectbox(
        "Choose Room Id for Stats",
        classIds,
    )
    fetchTopThreeMostTaught(selectIds, st.session_state["uid"])

    st.write("")
    st.write("")
    st.write("")

    col1, col2 = st.columns(2, vertical_alignment='bottom')

    with col1:
        selectYear = st.selectbox(
            "Choose Year",
            years,
        )
    with col2:
        selectSemester = st.selectbox(
            "Choose Semester",
            semester,
        )

    fetchMostTaughtClassesPerSemester(selectYear, selectSemester, st.session_state["uid"])

def fetchTopThreeCap(building, uid):

    st.write("Top Three Room Capacity per Building")

    response = requests.post( url = host + f"/losprogramadores/room/{building}/capacity", json = {"uid" : uid}).json()

    roomNums = []
    roomCaps = []
    for room in response:
        roomNums.append(room['room_number'])
        roomCaps.append(room['capacity'])

    chart_data = pd.DataFrame(
        {
            "Room Number": roomNums,
            "Capacity": roomCaps
        }
    )

    st.bar_chart(chart_data,x='Room Number',y='Capacity')

def fetchTopThreeRatio(building, uid):

    st.write("You selected:", building)
    st.write("Top Three Student Capacity to Section Capacity Ratio per Building")

    response = requests.post(url= host + f"/losprogramadores/room/{building}/ratio" , json = {"uid" : uid}).json()
    roomNums = []
    roomRatios = []
    for room in response:
        roomNums.append(room['room_number'])
        roomRatios.append(round(float(room['student_ratio'])*100,2))

    chart_data = pd.DataFrame(
        {
            "Room Number": roomNums,
            "Student-Capacity Ratio (%)": roomRatios
        }
    )

    st.bar_chart(chart_data, x='Room Number', y='Student-Capacity Ratio (%)')


def fetchTopThreeMostTaught(rid, uid):

    response = requests.post(url = host + f"/losprogramadores/room/{rid}/classes", json = {"uid" : uid}).json()

    classCount = []
    classCodeNameList = []
    for room in response:
        classCodeName = room['class_name'] + '-' + room['class_code']
        classCount.append(room['Count'])
        classCodeNameList.append(classCodeName)

    chart_data = pd.DataFrame(
        {
            "Classes Count": classCount,
            "Class Code-Name": classCodeNameList
        }
    )

    st.bar_chart(chart_data, x='Class Code-Name', y='Classes Count')


def fetchMostTaughtClassesPerSemester(year, semester, uid):

    lowerSemester = semester.lower()
    response = requests.post(url = host + f"/losprogramadores/classes/{year}/{lowerSemester}", json = {"uid" : uid}).json()


    sectionCount = []
    classNameList = []
    for course in response:
        if course == 'error':
            return st.text("There are no classes for this year and semester")

        className = course['cname'] + '-' + course['ccode']
        sectionCount.append(course['Sections'])
        classNameList.append(className)

    chart_data = pd.DataFrame(
        {
            "Classes Amount": sectionCount,
            "Class Code-Name": classNameList
        }
    )

    st.bar_chart(chart_data, x='Class Code-Name', y='Classes Amount')

# def fetchAllMeetings():
#
#     st.write("All Meetings")
#
#     response = requests.get(host + '/losprogramadores/meeting').json()
#
#     df = pd.DataFrame(response)
#
#
#     if 'mid' in df.columns:
#         df = df.drop(columns=['mid'])
#
#     df.columns = ['Code', 'Days', 'Start_Time', 'End_Time']
#
#     st.dataframe(df, height=400)
#
# def fetchAllRoom():
#     st.write("All Rooms")
#
#     response = requests.get(host + '/losprogramadores/room').json()
#
#     df = pd.DataFrame(response)
#
#     if 'rid' in df.columns:
#         df = df.drop(columns=['rid'])
#
#     df.columns = ['Building', 'Capacity', 'Room_Number']
#
#     st.dataframe(df, height=400)
#
# def fetchAllSections():
#     st.write("All Sections")
#
#     response = requests.get(host + '/losprogramadores/section').json()
#
#     df = pd.DataFrame(response)
#
#     if 'sid' in df.columns:
#         df = df.drop(columns=['sid'])
#     if 'room_id' in df.columns:
#         df = df.drop(columns=['room_id'])
#     if 'meeting_id' in df.columns:
#         df = df.drop(columns=['meeting_id'])
#     if 'class_id' in df.columns:
#         df = df.drop(columns=['class_id'])
#
#
#     df.columns = ['Capacity', 'Semester', 'Years']
#
#     st.dataframe(df, height=400)
#
# fetchAllMeetings()
# fetchAllRoom()
# fetchAllSections()

render()