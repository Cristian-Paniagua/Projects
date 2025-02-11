from flask import jsonify
from dao.DaoClass import DaoClass
from psycopg2 import IntegrityError
from datetime import datetime, timedelta, time

class ClassHandler:
    def mapToDict(self, tuple):
        result = {}
        result['cid'] = tuple[0]
        result['cname'] = tuple[1]
        result['ccode'] = tuple[2]
        result['cdesc'] = tuple[3]
        result['term']= tuple[4]
        result['years'] = tuple[5]
        result['cred']=tuple[6]
        result['csyllabus']=tuple[7]
        return result

    def getAll(self):
        result = []
        dao = DaoClass()
        temp = dao.getAllClasses()
        for t in temp:
            result.append(self.mapToDict(t))
        return jsonify(result)

    def getById(self, cid):
        dao = DaoClass()
        result = dao.getClassById(cid)
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return {"error": "Not Found"}, 404

    def insert(self, class_json):

        cname = class_json.get("cname")
        ccode = class_json.get("ccode")
        cdesc = class_json.get("cdesc")
        term = class_json.get("term")
        years = class_json.get("years")
        credits = class_json.get("cred")
        syllabus = class_json.get("csyllabus")

        if cname is None:
            return {"error": "Course name field is required and cannot be null"}, 400
        if ccode is None:
            return {"error": "Code field is required and cannot be null"}, 400
        if cdesc is None:
            return {"error": "Description field is required and cannot be null"}, 400
        if term is None:
            return {"error":  "Term field is required and cannot be null"}, 400
        if years is None:
            return {"error": "Years field is required and cannot be null"}, 400
        if credits is None or not isinstance(credits, int) or credits <= 0:
            return {"error": "Credits must be a positive integer."}, 400
        if syllabus is None:
            return {"error": "Syllabus field is required and cannot be null"}, 400

        if term not in ['First Semester', 'Second Semester', 'First Semester, Second Semester', 'According to Demand']:
            return {"error": "Term field is required to be in format ['First Semester', 'Second Semester', 'First Semester, Second Semester', 'According to Demand']"}, 400

        if years not in ['Even Years', 'Odd Years', 'Every Year', 'According to Demand']:
            return {"error": "Years field is required to be in format ['Even Years', 'Odd Years', 'Every Year', 'According to Demand']"}, 400

        dao = DaoClass()
        try:
            cid = dao.insertClass( cname, ccode , cdesc, term, years, credits, syllabus)
        except IntegrityError as e:
            dao.conn.rollback()
            print(f"IntegrityError: {str(e)}")
            return {"error": "Database constraint error, possibly duplicate class."}, 400
        except Exception as e:
            dao.conn.rollback()
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

        temp = (cid, cname, ccode , cdesc, term, years, credits, syllabus)
        return jsonify(self.mapToDict(temp)), 201

    def deleteById(self, cid):
        dao = DaoClass()
        temp = dao.deleteClassById(cid)
        if temp:
            return jsonify(DeleteStatus="Correct"), 200
        else:
            return jsonify(DeleteStatus="Not Found"), 404

    def updateById(self, cid, class_json):

        cname = class_json.get("cname")
        ccode = class_json.get("ccode")
        cdesc = class_json.get("cdesc")
        term = class_json.get("term")
        years = class_json.get("years")
        credits = class_json.get("cred")
        syllabus = class_json.get("csyllabus")

        if cname is None:
            return {"error": "Course name field is required and cannot be null"}, 400
        if ccode is None:
            return {"error": "Code field is required and cannot be null"}, 400
        if cdesc is None:
            return {"error": "Description field is required and cannot be null"}, 400
        if term is None:
            return {"error": "Term field is required and cannot be null"}, 400
        if years is None:
            return {"error": "Years field is required and cannot be null"}, 400
        if credits is None or not isinstance(credits, int) or credits <= 0:
            return {"error": "Credits must be a positive integer."}, 400
        if syllabus is None:
            return {"error": "Syllabus field is required and cannot be null"}, 400

        if term not in ['First Semester', 'Second Semester', 'First Semester, Second Semester', 'According to Demand']:
            return {
                "error": "Term field is required to be in format ['First Semester', 'Second Semester', 'First Semester, Second Semester', 'According to Demand']"}, 400

        if years not in ['Even Years', 'Odd Years', 'Every Year', 'According to Demand']:
            return {
                "error": "Years field is required to be in format ['Even Years', 'Odd Years', 'Every Year', 'According to Demand']"}, 400
        dao = DaoClass()
        try:
            temp = dao.updateClassById(cid,cname, ccode , cdesc, term, years, credits, syllabus)
            if temp:
                tup= (cid, cname, ccode , cdesc, term, years, credits, syllabus)
                return jsonify(self.mapToDict(tup)), 200
        except IntegrityError as e:
            dao.conn.rollback()
            print(f"IntegrityError: {str(e)}")
            return {"error": "Database constraint error, possibly duplicate class."}, 400
        except Exception as e:
            dao.conn.rollback()
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

    def getByCodeName(self, code, name):
        dao = DaoClass()
        temp = dao.getByCodeName(code, name)
        result = []
        if temp:

            while not result:
                cols = {}
                cols['ccode'] = temp[0]
                cols['cname'] = temp[1]
                cols['cdesc'] = temp[2]
                cols['term'] = temp[3]
                cols['years'] = temp[4]
                cols['cred'] = temp[5]
                cols['csyllabus'] = temp[6]
                result.append(cols)
            return jsonify(result)
        else:
            return {"error": "Not Found"}, 404

    def getClassSections(self, cid):
        dao = DaoClass()
        temp = dao.getClassSections(cid)
        result = []
        if temp:

            for row in temp:
                cols = {}
                cols['ccode'] = row[0]
                cols['capacity'] = row[1]
                cols['starttime'] = row[2].strftime("%H:%M:%S") if isinstance(row[2], time) else row[2]
                cols['endtime'] = row[3].strftime("%H:%M:%S") if isinstance(row[3], time) else row[3]
                cols['cdays'] = row[4]
                cols['building'] = row[5]
                cols['room_number'] = row[6]
                cols['semester'] = row[7]
                cols['years'] = row[8]
                result.append(cols)
            return jsonify(result)
        else:
            return {"error": "Not Found"}, 404