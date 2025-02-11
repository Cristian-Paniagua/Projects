
import streamlit as st
import pandas as pd
import requests
from auth import require_login

host = 'http://databasephase1-e3daa06311f4.herokuapp.com'
#host = ''

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
    payload = {
        "uid" : st.session_state["uid"]
    }
    st.write("Graph for the stats of the Total Sections Each Year")
    fetchTotalSectionsPerYear(payload)

    st.write("")
    st.write("")
    st.write("")

    st.write("Graph for the stats of the Top Three Classes By Pre-requisite")
    fetchTopThreeClassesPerPreq(payload)

    st.write("")
    st.write("")
    st.write("")

    st.write("Graph for the stats of the Top 5 Meeting with the Most Sections")
    fetchMeetingWithMostSections(payload)

    st.write("")
    st.write("")
    st.write("")

    st.write("Graph for the stats of the Top 3 Classes that were offered the least")
    fetchTopThreeLeastOfferedClasses(payload)

def fetchTotalSectionsPerYear(payload):

    response = requests.post(url=host + '/losprogramadores/section/year', json = payload).json()

    sectionCount = []
    years = []

    for data in response:
        sectionCount.append(data['Count'])
        years.append(data['year'])

    df = pd.DataFrame(response)

    chart_data = pd.DataFrame(
        {
            "Total Sections": sectionCount,
            "Year": years
        }
    )

    st.bar_chart(chart_data, x = 'Year', y = 'Total Sections')


def fetchTopThreeClassesPerPreq(payload):

    response = requests.post(url= host + '/losprogramadores/most/prerequisite', json= payload).json()

    reqCount = []
    classCodeNameList = []

    for data in response:
        classCodeName = data['cname'] + '-' + data['ccode']
        reqCount.append(data['count'])
        classCodeNameList.append(classCodeName)
    df = pd.DataFrame(response)

    chart_data = pd.DataFrame(
        {
            "Prerequisite total": reqCount,
            "Class Code-Name": classCodeNameList
        }
    )

    st.bar_chart(chart_data, x='Class Code-Name', y='Prerequisite total')


def fetchMeetingWithMostSections(payload):

    response = requests.post(url = host + '/losprogramadores/most/meeting', json = payload).json()

    sectionsCount = []
    meetingCodeDaysList = []

    for data in response:
        meetingCodeDays = data['meeting_days'] + '-' + data['meeting_code']
        sectionsCount.append(data['Sections'])
        meetingCodeDaysList.append(meetingCodeDays)
    df = pd.DataFrame(response)

    chart_data = pd.DataFrame(
        {
            "Total Sections": sectionsCount,
            "Meeting Days and Code": meetingCodeDaysList
        }
    )

    st.bar_chart(chart_data, x='Meeting Days and Code', y='Total Sections')

def fetchTopThreeLeastOfferedClasses(payload):

    response = requests.post(url= host + '/losprogramadores/least/classes', json= payload).json()

    sectionCount = []
    classNameList = []
    for course in response:
        className = course['class_name'] + '-' + course['class_code']
        sectionCount.append(course['Sections'])
        classNameList.append(className)

    chart_data = pd.DataFrame(
        {

            "Class Code-Name": classNameList,
            "Times Offered": sectionCount
        }
    )

    st.bar_chart(chart_data, x = 'Class Code-Name', y='Times Offered')

render()

