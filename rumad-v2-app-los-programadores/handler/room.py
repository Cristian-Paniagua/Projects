from flask import jsonify
from dao.DaoRoom import DaoRooms
from psycopg2 import IntegrityError

class RoomHandler():
    def mapToDict(self,tuple):
        result={}
        result['rid']= tuple[0]
        result['building']= tuple[1]
        result['room_number']= tuple[2]
        result['capacity']= tuple[3]
        return result

    def getAll(self):
        result = []
        dao = DaoRooms()
        temp = dao.getAllRooms()
        
        for t in temp:
            result.append(self.mapToDict(t))
        return jsonify(result)

    def getById(self,rid):
        dao = DaoRooms()
        result = dao.getRoomById(rid)
        
        if result:
            return jsonify(self.mapToDict(result))
        else:
            return {"error": "Not Found"},404

    def insert(self, room_json):

        building = room_json.get("building")
        room_number = room_json.get("room_number")
        capacity = room_json.get("capacity")

        if building is None:
            return {"error": "Building field is required and cannot be null"},400
        if room_number is None:
            return {"error": "Room number field is required and cannot be null"},400
        if capacity is None or not isinstance(capacity, int) or capacity <= 0:
            return {"error": "Capacity must be a positive integer."}, 400

        dao = DaoRooms()
        try:
            rid = dao.insertRoom(building, room_number, capacity)
            
        except IntegrityError as e:
            dao.conn.rollback()
            print(f"IntegrityError: {str(e)}")
            return {"error": "Database constraint error, possibly duplicate room."}, 400
        except Exception as e:
            dao.conn.rollback()
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

        temp = (rid, building, room_number, capacity)

        return jsonify(self.mapToDict(temp)), 201

    def deleteById(self,rid):
        dao = DaoRooms()
        temp = dao.deleteRoomById(rid)
        
        if temp:
            return jsonify(DeleteStatus = "Correct"), 200
        else:
            return jsonify(DeleteStatus = "Not Found"), 404

    def updateById(self, rid, room_json):
        building = room_json.get("building")
        room_number = room_json.get("room_number")
        capacity = room_json.get("capacity")

        if building is None:
            return {"error": "Building field is required and cannot be null"},400
        if room_number is None:
            return {"error": "Room number field is required and cannot be null"},400
        if capacity is None or not isinstance(capacity, int) or capacity <= 0:
            return {"error": "Capacity must be a positive integer."}, 400

        dao = DaoRooms()
        try:
            temp = dao.updateRoomById(rid, building, room_number, capacity)
            if temp:
                tup = (rid, building, room_number, capacity)
                
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




    def getTopThreeCap(self, building):

        result =[]
        dao = DaoRooms()
        #building = building_json['building']
        temp = dao.getTopThreeCap(building)
        if temp==[]:
            return {"error": "Building does not exist."}, 404
        for t in temp:
            result.append(self.mapToDict(t))
        return jsonify(result)

    def getTopThreeRatio(self, building):
        result =[]

        dao = DaoRooms()
        # building = building_json['building']
        temp = dao.getTopThreeRatio(building)
        if temp == []:
            return {"error": "Building does not exist or Section in this building does not exist."}, 404

        for t in temp:
            map = {}
            map['rid'] = t[0]
            map['building'] = t[1]
            map['room_number'] = t[2]
            map['capacity'] = t[3]
            map['student_ratio']=t[4]
            result.append(map)
        return jsonify(result)

    def getTopThreeMostTaught(self, rid):
        result=[]

        dao= DaoRooms()
        temp = dao.getTopThreeMostTaught(rid)

        if temp==[]:
            return {"error": "Room id non existing"}
        for t in temp:
            map = {}
            map['class_id'] = t[0]
            map['class_name'] = t[1]
            map['class_code'] = t[2]
            map['Count'] = t[3]
            result.append(map)
        return jsonify(result)
