from xmlrpc.client import boolean

from flask import jsonify, request
from dao.DaoRequisite import DaoRequisite
from psycopg2 import IntegrityError

class RequisiteHandler:
    def mapToDict(self, tuple):
        return {
            'classid': tuple[0],
            'requisiteid': tuple[1],
            'preReq': tuple[2]
        }


    def getAll(self):
        dao = DaoRequisite()
        result = [self.mapToDict(t) for t in dao.getAllRequisites()]
        return jsonify(result)


    def getById(self, classid, requisiteid):
        dao = DaoRequisite()
        result = dao.getRequisiteById(classid, requisiteid)
        if result:
            return jsonify(self.mapToDict(result))
        return {"error": "Not Found"}, 404


    def insert(self, requisite_json):
        cid = requisite_json.get("classid")
        requisiteid = requisite_json.get("requisiteid")
        preReq = requisite_json.get("preReq")

        if cid is None:
            return {"error": "Class ID missing"}, 400
        if requisiteid is None:
            return {"error": "Requisite ID missing"}, 400
        if preReq is None:
            return {"error": "Specify if that class is required corequired"}, 400
        if not isinstance(cid, int) :
            return {"error": "Invalid data. 'cid' must be integers"}, 400
        if not isinstance(requisiteid, int):
            return {"error": "Invalid data. 'requisiteid' must be integers"}, 400
        if not isinstance(preReq, bool):
            return {"error": "Invalid data. 'preReq' must be a boolean"}, 400

        dao = DaoRequisite()
        try:
            dao.insertRequisite(cid, requisiteid, preReq)
        except IntegrityError:
            dao.conn.rollback()
            return {"error": "Database constraint error, possibly duplicate requisite."}, 400
        except Exception as e:
            dao.conn.rollback()
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

        temp = (cid, requisiteid, preReq)
        return jsonify(self.mapToDict(temp)), 201


    def update(self, classid, requisiteid, requisite_json):
        cid = requisite_json.get("classid")
        requisiteidnew = requisite_json.get("requisiteid")
        preReq = requisite_json.get("preReq")

        if cid is None:
            return {"error": "Class ID missing"}, 400
        if requisiteid is None:
            return {"error": "Requisite ID missing"}, 400
        if preReq is None:
            return {"error": "Specify if that class is required corequired"}, 400
        if not isinstance(cid, int):
            return {"error": "Invalid data. 'cid' must be integers"}, 400
        if not isinstance(requisiteid, int):
            return {"error": "Invalid data. 'requisiteid' must be integers"}, 400
        if not isinstance(preReq, bool):
            return {"error": "Invalid data. 'preReq' must be a boolean"}, 400

        dao = DaoRequisite()
        try:
            temp = dao.updateRequisite(classid, requisiteid, cid, requisiteidnew, preReq)
            if temp:
                return jsonify(self.mapToDict((cid, requisiteidnew, preReq))), 200
            else:
                return {"error": "Requisite not found."}, 404
        except IntegrityError:
            dao.conn.rollback()
            return {"error": "Database constraint error, possibly duplicate requisite."}, 400
        except Exception as e:
            dao.conn.rollback()
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500


    def delete(self, classid, requisiteid):
        dao = DaoRequisite()
        try:
            deleted = dao.deleteRequisite(classid, requisiteid)
            if deleted:
                dao.conn.rollback()
                return {"message": f"Requisite with cid {classid} and requisiteid {requisiteid} deleted."}, 200
            else:
                return {"error": "Requisite not found."}, 404
        except Exception as e:
            dao.conn.rollback()
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500




    def getTopThreePrerequisites(self):
        dao = DaoRequisite()
        result = dao.getTopThreePrerequisites()
        top_three = [{"courseid": row[0], "count": row[1], "ccode": row[2], "cname": row[3]} for row in result]
        return jsonify(top_three)
