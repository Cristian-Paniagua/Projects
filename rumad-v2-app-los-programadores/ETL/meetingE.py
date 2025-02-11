

import pandas as pd
from datetime import timedelta, time
from dao.DaoMeeting import DaoMeeting

daoMeeting = DaoMeeting()

df = pd.read_csv("files/meeting.csv", delimiter=",")
df['ccode'] = df['ccode'].astype(str).str.zfill(3)


df['start'] = pd.to_datetime(df['start'], format= '%H:%M:%S').dt.time
df['end'] = pd.to_datetime(df['end'], format= '%H:%M:%S').dt.time

morning_end = pd.to_datetime('10:15:00', format='%H:%M:%S').time()
afternoon_start = pd.to_datetime('12:30:00', format='%H:%M:%S').time()
afternoon_end = pd.to_datetime('19:45:00', format='%H:%M:%S').time()

def is_allowed(row):
    if row['day'] == 'MJ':
        return (row['start'] < morning_end) or ( afternoon_end>=row['end'] >= afternoon_start)
    return True



def inbetween(row):
    if row['day'] == 'MJ':
        return (row['start'] >= morning_end) and (morning_end < row['end'] <= afternoon_start)
    return False

def changehour(df):
    adjustment =timedelta(0)
    for index, row in df.iterrows():
        adjustment = timedelta(0)
        if row['day'] == 'MJ':
            if not (row['start'] >= afternoon_start):
                if row['start'] >= morning_end and row['end'] >= afternoon_start:
                    adjustment = timedelta(hours= afternoon_start.hour, minutes= afternoon_start.minute, seconds= afternoon_start.second) - \
                                        timedelta(hours = row['start'].hour, minutes= row['start'].minute, seconds= row['start'].second)
                    new_start_seconds = (row['start'].hour * 3600 + row['start'].minute * 60 + row[
                        'start'].second + adjustment.total_seconds())
                    new_end_seconds = (row['end'].hour * 3600 + row['end'].minute * 60 + row[
                        'end'].second + adjustment.total_seconds())


                    new_start = time(hour=int(new_start_seconds // 3600) % 24,
                                     minute=int((new_start_seconds % 3600) // 60),
                                     second=int(new_start_seconds % 60))
                    new_end = time(hour=int(new_end_seconds // 3600) % 24,
                                   minute=int((new_end_seconds % 3600) // 60),
                                   second=int(new_end_seconds % 60))

                    df.loc[index, 'start'] = new_start
                    df.loc[index, 'end'] = new_end

            for j in range(index + 1, len(df)):
                if df.loc[j, 'day'] == 'MJ':
                    next_start_seconds = df.at[j, 'start'].hour * 3600 + df.at[j, 'start'].minute * 60 + df.at[j, 'start'].second + adjustment.total_seconds()
                    next_end_seconds = df.at[j, 'end'].hour * 3600 + df.at[j, 'end'].minute * 60 + df.at[j, 'end'].second + adjustment.total_seconds()


                    next_starttime = time(hour=int(next_start_seconds // 3600) % 24,
                                 minute=int((next_start_seconds % 3600) // 60),
                                 second=int(next_start_seconds % 60))

                    next_endtime = time(hour=int(next_end_seconds // 3600) % 24,
                               minute=int((next_end_seconds % 3600) // 60),
                               second=int(next_end_seconds % 60))
                    df.loc[j, 'start'] = next_starttime
                    df.loc[j, 'end'] = next_endtime



    return df



to_remove = []


for index, row in df.iterrows():
    if inbetween(row) or not is_allowed(row):
        to_remove.append(index)


df = changehour(df)
df = df.drop(to_remove)


for index, row in df.iterrows():

    meeting = (row['mid'], row['ccode'], row['start'].strftime('%Y-%m-%d %H:%M:%S'), row['end'].strftime('%Y-%m-%d %H:%M:%S'), row['day'])
    daoMeeting.insertMeeting(meeting)


daoMeeting.closeConnection()








