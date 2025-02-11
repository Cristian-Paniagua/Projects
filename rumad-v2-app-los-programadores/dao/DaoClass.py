from .DatabaseConnection import DBConnection
import psycopg2
from psycopg2 import IntegrityError

dbConnection = DBConnection()

class DaoClass:
    def __init__(self):
        self.dbConnection = dbConnection
        self.conn = self.dbConnection.getConnection()

    def getIdByCode(self, name, code):
        cur =self.conn.cursor()
        query = "Select cid from class where cname= %s and ccode=%s"
        cur.execute(query, (name,code))
        result = cur.fetchone()
        return result


    def insertCourse(self, course):
        cur = self.conn.cursor()
        query = ("Insert into class(cid, cname, ccode, cdesc, term, years, cred, csyllabus) values (%s, %s, %s, %s, %s, %s, %s, %s)")
        cur.execute(query, course)
        cur.connection.commit()
        return True

    def getAllClasses(self):
        cur = self.conn.cursor()
        query = "SELECT cid, cname, ccode, cdesc, term, years, cred, csyllabus FROM class"
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        return result
    def getAllClassesDesc(self):
        cur = self.conn.cursor()
        query = "SELECT cid, cname, ccode, cdesc FROM class"
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        return result
    def getClassById(self,cid):
        cur = self.conn.cursor()
        query= "SELECT cid, cname, ccode, cdesc, term, years, cred, csyllabus FROM class where cid = %s"
        cur.execute(query, (cid,))
        result = cur.fetchone()
        return result

    def getCourseById(self, cid):
        cur = self.conn.cursor()
        query = "SELECT cid, cname, ccode, cdesc, term, years, cred, csyllabus FROM class WHERE cid = %s"
        cur.execute(query, (cid,))
        result = cur.fetchone()
        if result is None:
            return []
        return result

    def getIdByName(self, name):
        cur = self.conn.cursor()
        query = "select cid from class where cdesc = %s"
        cur.execute(query, (name,))
        result = cur.fetchone()
        if result is None:
            return []
        return result

    def insertClass(self, cname, ccode, cdesc, term, years, cred, csyllabus):
        cur = self.conn.cursor()
        query = "INSERT INTO class (cname, ccode, cdesc, term, years, cred, csyllabus) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING cid"
        cur.execute(query, (cname, ccode, cdesc, term, years, cred, csyllabus))
        cid = cur.fetchone()[0]
        self.conn.commit()
        return cid

    def deleteClassById(self, cid):
        cur = self.conn.cursor()
        query = "DELETE FROM class WHERE cid = %s"
        cur.execute(query, (cid,))
        rowcount = cur.rowcount
        self.conn.commit()
        return rowcount == 1

    def updateClassById(self, cid, cname, ccode, cdesc, term, years, cred, csyllabus):
        cur = self.conn.cursor()
        query = "UPDATE class SET cname = %s, ccode = %s, cdesc = %s, term = %s, years = %s, cred = %s, csyllabus = %s WHERE cid = %s"
        cur.execute(query, (cname, ccode, cdesc, term, years, cred, csyllabus, cid))
        rowcount = cur.rowcount
        self.conn.commit()
        return rowcount == 1

    def getTopCoursesByCredits(self, limit=3):
        cur = self.conn.cursor()
        query = "SELECT cid, cname, ccode, cdesc, term, years, cred, csyllabus FROM class ORDER BY cred DESC LIMIT %s"
        cur.execute(query, (limit,))
        result = []
        for row in cur:
            result.append(row)
        return result

    def closeConnection(self):
        if self.conn:
            self.conn.close()



