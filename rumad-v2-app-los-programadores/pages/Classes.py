import streamlit as st
import pandas as pd
import requests
from auth import require_login

host = 'http://databasephase1-e3daa06311f4.herokuapp.com'
local = 'http://localhost:8501'

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



def fetchAllClasses():
    st.write("All Classes")
    require_login()

    response = requests.get(host + '/losprogramadores/class').json()

    df = pd.DataFrame(response)

    if 'cid' in df.columns:
        df = df.drop(columns=['cid'])

    df.columns = ['Code', 'Description', 'Name', 'Credits', 'Syllabus', 'Term', 'Years']

    df['Code_Name'] = df['Name'] + ' - ' + df['Code']

    columns = ['Code_Name'] + [col for col in df.columns if col != 'Code_Name']
    df = df[columns]

    df = df.drop(columns=['Code', 'Name'])

    def filter_dataframe(dataframe, query):
        filtered_rows = []
        query_lower = query.lower()

        for _, row in dataframe.iterrows():
            if any(query_lower in str(value).lower() for value in row):
                filtered_rows.append(row)

        return pd.DataFrame(filtered_rows, columns=dataframe.columns)

    col1, col2 = st.columns(2, vertical_alignment='bottom')
    with col1:
        search_query = st.text_input("Search")
    with col2:
        search_button = st.button("🔍")

    if search_query:
        df = filter_dataframe(df, search_query)

    def make_clickable_code_name(code_name):
        name, code = code_name.split(' - ')
        url = f"{local}/Sections/?show=True&Code={code}&Name={name}"
        return f'<a href="{url}" target="_blank">{code_name}</a>'

    df['Code_Name'] = df['Code_Name'].apply(make_clickable_code_name)

    html_table = df.to_html(escape=False, index=False)

    full_table = f"""
        <div style="
            width: 100%;  /* Make the table take the full width */
            max-width: 1000px;  /* Optional: Restrict the maximum width for large screens */
            border: 1px solid #ccc;
            padding: 10px;
            font-size: 14px;
            ">
            {html_table}
        </div>
        """

    st.markdown(full_table, unsafe_allow_html=True)




fetchAllClasses()