from flask import jsonify, request
from dao.DaoMeeting import DaoMeeting
from psycopg2 import IntegrityError
from datetime import datetime, timedelta, time
import pandas as pd

class MeetingHandler:
    def mapToDict(self, tuple):
        result = {}
        result['mid'] = tuple[0]
        result['ccode'] = tuple[1]
        result['starttime'] = tuple[2].strftime("%H:%M:%S") if isinstance(tuple[2], time) else tuple[2]
        result['endtime'] = tuple[3].strftime("%H:%M:%S") if isinstance(tuple[3], time) else tuple[3]
        result['cdays'] = tuple[4]
        result['cdays'] = tuple[4]
        return result

    def getAll(self):
        result = []
        dao = DaoMeeting()
        temp = dao.getAllMeetings()
        for t in temp:
            result.append(self.mapToDict(t))
        return jsonify(result)

    def getById(self, mid):
        dao = DaoMeeting()
        result = dao.getMeetingById(mid)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return {"error": "Meeting not found"}, 404

    def insert(self, meeting_json):
        ccode = meeting_json.get("ccode")
        starttime_str = meeting_json.get("starttime")
        endtime_str = meeting_json.get("endtime")
        cdays = meeting_json.get("cdays")

        # Basic field validation
        if ccode is None:
            return {"error": "Class code field is required and cannot be null"}, 400
        if starttime_str is None:
            return {"error": "Start time field is required and cannot be null"}, 400
        if endtime_str is None:
            return {"error": "End time field is required and cannot be null"}, 400
        if cdays is None:
            return {"error": "Days field is required and cannot be null"}, 400
        if cdays not in ["MJ", "LMV"]:
            return {"error": "Invalid days field. Must be either 'MJ' or 'LMV'."}, 400

        # Convert start and end times to datetime objects
        try:
            starttime = datetime.strptime(starttime_str, "%H:%M:%S").time()
            endtime = datetime.strptime(endtime_str, "%H:%M:%S").time()
            morning_start = pd.to_datetime('07:30:00', format='%H:%M:%S').time()
            morning_end = pd.to_datetime('10:15:00', format='%H:%M:%S').time()
            afternoon_start = pd.to_datetime('12:30:00', format='%H:%M:%S').time()
            afternoon_end = pd.to_datetime('19:45:00', format='%H:%M:%S').time()
        except ValueError:
            return {"error": "Invalid time format. Use format 'HH:MM:SS'."}, 400

        # Duration validation based on cdays
        duration = (datetime.combine(datetime.today(), endtime) - datetime.combine(datetime.today(), starttime)).total_seconds() / 60  # duration in minutes
        if cdays == "MJ":
            if duration != 75:
                return {"error": "For 'MJ' days, the duration must be exactly 75 minutes."}, 400
            if (morning_end < starttime < afternoon_start) or (morning_end < endtime < afternoon_start) or (starttime < morning_end and endtime > afternoon_start):
                return {"error": "For 'MJ' days, the meeting cannot overlap the period between 10:15:00 and 12:30:00."}, 400
            if endtime > afternoon_end:
                return {"error": "For 'MJ' days, classes must not finish after 7:45 PM."}, 400
        elif cdays == "LMV" and duration != 50:
            return {"error": "For 'LMV' days, the duration must be exactly 50 minutes."}, 400

        # Insert into database
        dao = DaoMeeting()
        try:
            mid = dao.insertMeeting(ccode, starttime_str, endtime_str, cdays)
        except IntegrityError as e:
            dao.conn.rollback()
            print(f"IntegrityError: {str(e)}")
            return {"error": "Database constraint error, possibly duplicate meeting."}, 400
        except Exception as e:
            dao.conn.rollback()
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

        temp = (mid, ccode, starttime_str, endtime_str, cdays)
        return jsonify(self.mapToDict(temp)), 201

    def deleteById(self, mid):
        dao = DaoMeeting()
        temp = dao.deleteMeeting(mid)
        if temp:
            return jsonify(DeleteStatus="Correct"), 200
        else:
            return jsonify(DeleteStatus="Not Found"), 404

    def updateById(self, mid, meeting_json):
        ccode = meeting_json.get("ccode")
        starttime_str = meeting_json.get("starttime")
        endtime_str = meeting_json.get("endtime")
        cdays = meeting_json.get("cdays")

        # Basic field validation
        if ccode is None:
            return {"error": "Class code field is required and cannot be null"}, 400
        if starttime_str is None:
            return {"error": "Start time field is required and cannot be null"}, 400
        if endtime_str is None:
            return {"error": "End time field is required and cannot be null"}, 400
        if cdays is None:
            return {"error": "Days field is required and cannot be null"}, 400
        if cdays not in ["MJ", "LMV"]:
            return {"error": "Invalid days field. Must be either 'MJ' or 'LMV'."}, 400

        # Convert start and end times to datetime objects
        try:
            starttime = datetime.strptime(starttime_str, "%H:%M:%S").time()
            endtime = datetime.strptime(endtime_str, "%H:%M:%S").time()
            morning_start = pd.to_datetime('07:30:00', format='%H:%M:%S').time()
            morning_end = pd.to_datetime('10:15:00', format='%H:%M:%S').time()
            afternoon_start = pd.to_datetime('12:30:00', format='%H:%M:%S').time()
            afternoon_end = pd.to_datetime('19:45:00', format='%H:%M:%S').time()
        except ValueError:
            return {"error": "Invalid time format. Use format 'HH:MM:SS'."}, 400

        # Duration validation based on cdays
        duration = (datetime.combine(datetime.today(), endtime) - datetime.combine(datetime.today(),
                                                                                   starttime)).total_seconds() / 60  # duration in minutes
        if cdays == "MJ":
            if duration != 75:
                return {"error": "For 'MJ' days, the duration must be exactly 75 minutes."}, 400
            if (morning_end < starttime < afternoon_start) or (morning_end < endtime < afternoon_start) or (
                    starttime < morning_end and endtime > afternoon_start):
                return {
                    "error": "For 'MJ' days, the meeting cannot overlap the period between 10:15:00 and 12:30:00."}, 400
            if endtime > afternoon_end:
                return {"error": "For 'MJ' days, classes must not finish after 7:45 PM."}, 400
        elif cdays == "LMV" and duration != 50:
            return {"error": "For 'LMV' days, the duration must be exactly 50 minutes."}, 400


        dao = DaoMeeting()
        try:
            temp = dao.updateMeeting(mid, ccode, starttime_str, endtime_str, cdays)
            if temp:
                tup = (mid, ccode, starttime_str, endtime_str, cdays)
                return jsonify(self.mapToDict(tup)), 200
            else:
                return jsonify(UpdateStatus="Not Found"), 404
        except IntegrityError as e:
            dao.conn.rollback()
            print(f"IntegrityError: {str(e)}")
            return {"error": "Database constraint error, possibly duplicate meeting."}, 400
        except Exception as e:
            dao.conn.rollback()
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

    def getTopMeetingsWithMostSections(self):
        result = []
        dao = DaoMeeting()
        temp = dao.get_top_meetings_with_most_sections()
        for t in temp:
            map = {}
            map['meeting_id'] = t[0]
            map['meeting_code'] = t[1]
            map['Sections'] = t[2]
            map['meeting_days'] = t[3]
            result.append(map)
        return jsonify(result)
