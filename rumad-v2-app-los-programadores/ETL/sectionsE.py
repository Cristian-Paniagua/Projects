# import pandas as pd
# from dao.DaoSection import DaoSection
# from dao.DaoClass import DaoClass
# from dao.DaoMeeting import DaoMeeting
# from dao.DaoRoom import DaoRooms
#
# daoSections = DaoSection()
# daoMeeting = DaoMeeting()
# daoRooms = DaoRooms()
# daoCourses = DaoClass()
#
# df = pd.read_csv("files/sections.csv", delimiter=",")
#
#
# to_remove = []
#
# def roomExist(rid):
#     if rid <= 0:
#         return False
#     return daoRooms.getRoomsById(rid) != []
#
# def meetingExist(mid):
#     meet = daoMeeting.getMeetingById(mid)
#     if mid <= 0:
#         return False
#     return daoMeeting.getMeetingById(mid) != []
#
# def courseExist(cid):
#     course = daoCourses.getCourseById(cid)
#     print(course[0][2])
#     if course == []:
#         return False
#     elif course[0][2] == '0000':
#         return False
#     if cid <= 0:
#         return False
#     return True
#
# def checkCapacity(sCap, rid):
#     rCap = daoRooms.getCapacity(rid)
#     if rCap == 0:
#         return False
#     else:
#         return sCap <= rCap
#
# def checkYears(cid, section):
#     if not courseExist(cid):
#         return False
#
#     cYear = daoCourses.getCourseById(cid)[0][5]
#     sYear = section[5]
#
#     checkYear = (
#             (sYear % 2 == 0 and cYear == 'Even Years') or
#             (sYear % 2 == 1 and cYear == 'Odd Years') or
#             cYear in {'Every Year', 'According to Demand'}
#     )
#     return checkYear
#
# def checkTerm(cid, section):
#     if not courseExist(cid):
#         return False
#
#     cTerm = daoCourses.getCourseById(cid)[0][4]
#     sTerm = section[4]
#     checkTerm = \
#         ('First Semester' in cTerm and sTerm == 'Fall') or \
#         ('Second Semester' in cTerm and sTerm == 'Spring') or \
#         (cTerm == 'According to Demand' and sTerm in {'V1', 'V2', 'Fall', 'Spring'})
#     return checkTerm
#
#
#
#
# df.drop_duplicates(subset='sid', keep=False, inplace=True)
#
#
#
# for index, row in df.iterrows():
#
#     section = (row['sid'], row['room_id'], row['meeting_id'], row['class_id'], row['semester'], row['year'], row['capacity'])
#     if not courseExist(section[3]):
#         to_remove.append(index)
#
#     elif not roomExist(section[1]):
#         to_remove.append(index)
#     elif not meetingExist(section[2]):
#         to_remove.append(index)
#     elif not checkCapacity(sCap=section[6], rid=section[1]):
#             to_remove.append(index)
#
#     elif not checkTerm(section[3], section):
#         to_remove.append(index)
#     elif not checkYears(section[3], section):
#         to_remove.append(index)
#
# df = df.drop(to_remove)
# to_remove =[]
#
# def checkRoomTime():
#     meetings_dict = {}
#
#     # Group meetings by their identifiers
#     for index, row in df.iterrows():
#         key = (row['meeting_id'], row['room_id'], row['semester'], row['year'])
#         if key not in meetings_dict:
#             meetings_dict[key] = []
#         meetings_dict[key].append(index)
#
#     # Check for conflicts within each group
#     for indices in meetings_dict.values():
#         if len(indices) > 1:
#             # Sort indices based on 'sid' to determine which to remove
#             sorted_indices = sorted(indices, key=lambda idx: df.at[idx, 'sid'])
#             to_remove.extend(sorted_indices[1:])  # Keep the first one, remove the others
#
# checkRoomTime()
# df=df.drop(to_remove)
#
# sections =[]
# for index, row in df.iterrows():
#
#     section = (row['sid'], row['room_id'], row['class_id'], row['meeting_id'], row['semester'], row['year'], row['capacity'])
#     print(section)
#     sections.append(section)
#
#
# daoSections.insertSection(sections)
# daoSections.closeConnection()