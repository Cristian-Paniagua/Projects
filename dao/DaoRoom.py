from .DatabaseConnection import DBConnection
import psycopg2
from psycopg2 import IntegrityError

dbConnection = DBConnection()
class DaoRooms:
    def __init__(self):
        self.dbConnection = dbConnection
        self.conn = self.dbConnection.getConnection()

    def getAllRooms(self):
        cur = self.conn.cursor()
        query = "select rid, building, room_number, capacity from room"
        cur.execute(query)
        result=[]
        for row in cur:
            result.append(row)
        return result


    def getRoomById(self, rid):
        cur = self.conn.cursor()
        query = "select rid, building, room_number, capacity from room where rid=%s"
        cur.execute(query, (rid,))
        result = cur.fetchone()
        return result

    def InsertRoom(self, room):
        cur = self.conn.cursor()
        query = "Insert into room (rid, building, room_number, capacity) values (%s,%s,%s,%s)"
        cur.execute(query, room)
        cur.connection.commit()
        return True

    def insertRoom(self, building, room_number, capacity):
        cur = self.conn.cursor()
        query = "Insert into room (building, room_number, capacity) values (%s,%s,%s) returning rid"
        cur.execute(query, (building, room_number, capacity))
        rid = cur.fetchone()[0]
        self.conn.commit()
        return rid


    def getCapacity(self, rid):
        cur = self.conn.cursor()
        query = "Select capacity from room where rid = %s;"
        cur.execute(query, (rid,))
        result = cur.fetchone()
        if result == None:
            return 0

        return result[0]

    def getRoomsById(self, rid):
        cur = self.conn.cursor()
        query = "Select rid, building, room_number, capacity from room where rid = %s"
        cur.execute(query, (rid,))
        cur.connection.commit()
        return cur.fetchall()

    def deleteRoomById(self, rid):
        cur = self.conn.cursor()
        query = "Delete from room where rid = %s"
        cur.execute(query, (rid,))
        rowcount = cur.rowcount
        self.conn.commit()
        return rowcount == 1

    def updateRoomById(self, rid, building, room_number, capacity):
            cur = self.conn.cursor()
            query = "Update room set building= %s, room_number=%s, capacity=%s where rid = %s"
            cur.execute(query, (building, room_number, capacity, rid))
            rowcount = cur.rowcount
            self.conn.commit()
            return rowcount == 1

    def getTopThreeCap(self, building):
        cur = self.conn.cursor()
        query = "Select rid, building, room_number, capacity from room where building = %s order by capacity desc limit 3;"
        cur.execute(query, (building,))
        result=[]
        for row in cur:
            result.append(row)
        return result

    def getTopThreeRatio(self, building):
        cur=self.conn.cursor()
        query = "Select r.rid, r.building, r.room_number, r.capacity, (AVG(s.capacity)/r.capacity) as student_ratio \
         from room as r inner join section as s on r.rid = s.roomid where r.building = %s \
         group by r.rid, r.building, r.room_number, r.capacity order by student_ratio desc limit 3;"
        cur.execute(query, (building,))
        result = []
        for row in cur:
            result.append(row)
        return result

    def getTopThreeMostTaught(self, rid):
        cur = self.conn.cursor()
        query= "Select c.cid, c.cname, c.ccode, count(*) from (class as c inner join section as s on c.cid = s.cid) \
         where s.roomid= %s\
         group by c.cid, c.cname, c.ccode order by count(*) desc limit 3;"
        cur.execute(query, (rid,))
        result = []
        for row in cur:
            result.append(row)
        return result


    def closeConnection(self):
        if self.conn:
            self.conn.close()

