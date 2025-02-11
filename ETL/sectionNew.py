import pandas as pd
from dao.DaoSection import DaoSection


daoSection = DaoSection()

df = pd.read_csv("files/section.csv", delimiter=",")

sections =[]
for index, row in df.iterrows():
    section = (row['sid'], row['roomid'], row['cid'], row['mid'], row['semester'], row['years'], row['capacity'])
    sections.append(section)
daoSection.insertSection(sections)

