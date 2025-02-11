from flask import jsonify
from dao.DaoSection import DaoSection
from dao.DaoRoom import DaoRooms
from dao.DaoClass import DaoClass
from psycopg2 import IntegrityError


class SectionHandler():
    def mapToDict(self, tuple):
        result = {}
        result['sid'] = tuple[0]
        result['room_id'] = tuple[1]
        result['class_id'] = tuple[2]
        result['meeting_id'] = tuple[3]
        result['semester'] = tuple[4]
        result['years'] = tuple[5]
        result['capacity'] = tuple[6]
        return result

    def getAll(self):
        result = []
        dao = DaoSection()
        temp = dao.getAllSections()
        for t in temp:
            result.append(self.mapToDict(t))
        return jsonify(result)

    def getById(self, sid):
        dao = DaoSection()
        result = dao.getSectionById(sid)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return {"error": "Not Found"}, 404

    def insert(self, section_json):

        roomid = section_json.get('room_id')
        classid = section_json.get('class_id')
        meetingid = section_json.get('meeting_id')
        semester = section_json.get('semester')
        years = section_json.get('years')
        capacity = section_json.get('capacity')

        if roomid is None or classid is None or meetingid is None or semester is None or years is None:
            return {"error": "Field is required and cannot be null"}, 400
        if capacity is None or not isinstance(capacity, int) or capacity <= 0:
            return {"error": "Capacity must be a positive integer."}, 400
        daoR = DaoRooms()

        if daoR.getCapacity(roomid) < capacity:
            return {"error": "Capacity must be less than or equal to fit in the room"}, 400

        termMap={
            'First Semester':['Fall'],
            'Second Semester':['Spring'],
            'First Semester, Second Semester':['Fall', 'Spring'],
            'According to Demand':['Fall', 'Spring', 'V1','V2']
        }
        daoC = DaoClass()
        if semester not in termMap[daoC.getClassById(classid)[4]]:
            return {"error": "Semester did not meet the requirements for the class"}, 400

        cyears = daoC.getClassById(classid)[5]
        syears = int(years)
        if cyears == "Even Years" and not syears%2 ==0:
            return {"error": "Year must be even"}, 400
        elif cyears == "Odd Years" and not syears%2 ==1:
            return {"error": "Year must be odd"}, 400

        dao = DaoSection()
        try:
            sid = dao.insertSectionHandler(roomid, classid, meetingid, semester, years, capacity)
        except IntegrityError as e:
            dao.conn.rollback()
            print(f"IntegrityError: {str(e)}")
            return {"error": "Database constraint error, possibly duplicate room."}, 400
        except Exception as e:
            dao.conn.rollback()
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

        temp = (sid, roomid, classid, meetingid, semester, years, capacity)

        return jsonify(self.mapToDict(temp)), 201

    def deleteById(self, sid):
        dao = DaoSection()
        temp = dao.deleteSectionById(sid)
        if temp:
            return jsonify(DeleteStatus="Correct"), 200
        else:
            return jsonify(DeleteStatus="Not Found"), 404

    def updateById(self, sid, section_json):

        roomid = section_json.get('room_id')
        classid = section_json.get('class_id')
        meetingid = section_json.get('meeting_id')
        semester = section_json.get('semester')
        years = section_json.get('years')
        capacity = section_json.get('capacity')

        if not roomid or not classid or not meetingid or not semester or not years:
            return {"error": "Field is required and cannot be null"}, 400
        if capacity is None or not isinstance(capacity, int) or capacity <= 0:
            return {"error": "Capacity must be a positive integer."}, 400
        daoR = DaoRooms()

        if daoR.getCapacity(roomid) < capacity:
            return {"error": "Capacity must be less than or equal to fit in the room"}, 400

        termMap = {
            'First Semester': ['Fall'],
            'Second Semester': ['Spring'],
            'First Semester, Second Semester': ['Fall', 'Spring'],
            'According to Demand': ['Fall', 'Spring', 'V1', 'V2']
        }
        daoC = DaoClass()
        if semester not in termMap[daoC.getClassById(classid)[4]]:
            return {"error": "Semester did not meet the requirements for the class"}, 400

        cyears = daoC.getClassById(classid)[5]
        syears = int(years)
        if cyears == "Even Years" and not syears % 2 == 0:
            return {"error": "Year must be even"}, 400
        elif cyears == "Odd Years" and not syears % 2 == 1:
            return {"error": "Year must be odd"}, 400

        dao = DaoSection()
        try:
            temp = dao.updateSectionById(sid,roomid, classid, meetingid, semester, years, capacity)
            if temp:
                tup = (sid,roomid, classid, meetingid, semester, years, capacity)
                return jsonify(self.mapToDict(tup)), 200
            else:
                return jsonify(UpdateStatus="Not Found"), 404
        except IntegrityError as e:
                # Rollback on IntegrityError
            dao.conn.rollback()
            print(f"IntegrityError: {str(e)}")
            return jsonify(error="Database constraint error, possibly duplicate room."), 400

        except Exception as e:
            dao.conn.rollback()
            print(f"Unexpected error: {str(e)}")
            return jsonify(error=f"An unexpected error occurred: {str(e)}"), 500

    def getTotalSectionsPerYear(self):
        result =[]

        dao = DaoSection()
        temp = dao.getTotalSectionsPerYear()
        for t in temp:
           map={}
           map['year'] = t[0]
           map['Count']=t[1]
           result.append(map)
        return jsonify(result), 200

    def getMostTaughtPerSemester(self, year, semester):
        result = []
        if semester not in ["Spring", "Fall", "V1", "V2"]:
            return jsonify({"error": "Semester not supported. Must be in this format: ['Spring', 'Fall', 'V1', 'V2']"}), 404

        dao = DaoSection()
        temp = dao.getMostTaughtPerSemester(year, semester)

        if not temp:
            return {"error":"There are no sections in this semester or year"}
        for t in temp:
            map = {}
            map['classid'] = t[0]
            map['year'] = t[1]
            map['Sections'] = t[2]
            map['semester'] = t[3]
            map['ccode'] = t[4]
            map['cname'] = t[5]
            result.append(map)
        return jsonify(result), 200

    def getTopThreeLeastOfferedClasses(self):
        result = []
        dao = DaoSection()
        temp = dao.getTopThreeLeastOfferedClasses()

        for t in temp:
            print(t)
            map = {}
            map['cid'] = t[0]
            map['class_name'] = t[1]
            map['class_code'] = t[2]
            map['Sections'] = t[3]
            result.append(map)

        return jsonify(result), 200

