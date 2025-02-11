from .DatabaseConnection import DBConnection
import psycopg2
from psycopg2 import IntegrityError

dbConnection = DBConnection()

class DaoRequisite:
    def __init__(self):
        self.dbConnection = dbConnection
        self.conn = self.dbConnection.getConnection()

    def getAllRequisites(self):
        cur = self.conn.cursor()
        query = "SELECT classid, reqid, prereq FROM requisite"
        cur.execute(query)
        result = [row for row in cur]
        return result

    def getRequisiteById(self, classid, reqid):
        cur = self.conn.cursor()
        query = "SELECT classid, reqid, prereq FROM requisite WHERE classid = %s AND reqid = %s"
        cur.execute(query, (classid, reqid))
        result = cur.fetchone()
        return result

    def insertRequisite(self, classid, reqid, prereq):
        cur = self.conn.cursor()
        query = "INSERT INTO requisite (classid, reqid, prereq) VALUES (%s, %s, %s)"
        cur.execute(query, (classid, reqid, prereq,))
        self.conn.commit()

    def updateRequisite(self, classid, reqid, classidnew, prereqidnew, prereq):
        cur = self.conn.cursor()
        query = "UPDATE requisite SET classid=%s, reqid=%s, prereq = %s WHERE classid = %s AND reqid = %s"
        cur.execute(query, (classidnew, prereqidnew, prereq, classid, reqid,))
        rowcount = cur.rowcount
        self.conn.commit()
        return rowcount ==1

    def deleteRequisite(self, classid, reqid):
        cur = self.conn.cursor()
        query = "DELETE FROM requisite WHERE classid = %s AND reqid = %s RETURNING reqid"
        cur.execute(query, (classid, reqid))
        deleted_id = cur.fetchone()
        self.conn.commit()
        cur.close()
        return deleted_id is not None

    def closeConnection(self):
        if self.conn:
            self.conn.close()

    def getTopThreePrerequisites(self):
        cur = self.conn.cursor()
        query = """
        select reqid as requisiteid, count(reqid) as count, ccode, cname
        from requisite inner join class c on c.cid = requisite.reqid
        where reqid = c.cid
        group by requisiteid, ccode, cname
        order by count desc
        limit 3
        """
        cur.execute(query)
        result = cur.fetchall()
        cur.close()
        return result
