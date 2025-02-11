#from ETL.requisitesE import query
from .DatabaseConnection import DBConnection
import psycopg2
dbConnection = DBConnection()
class DaoSection:
    def __init__(self):
        self.dbConnection = dbConnection
        self.conn = self.dbConnection.getConnection()

    def insertSection(self, section):
        cur = self.conn.cursor()
        query = "Insert into section(sid, roomid, cid, mid, semester, years, capacity) values (%s,%s,%s,%s,%s,%s,%s)"
        cur.executemany(query, section)
        cur.connection.commit()
        return True

    def insertSectionHandler(self, roomid, cid, mid, semester, years, capacity):
        cur = self.conn.cursor()
        query = "Insert into section (roomid ,cid, mid, semester, years, capacity) values (%s,%s,%s,%s,%s,%s) returning sid"
        cur.execute(query, (roomid ,cid, mid, semester, years, capacity))
        sid = cur.fetchone()[0]
        self.conn.commit()
        return sid

    def getAllSections(self):
        cur = self.conn.cursor()
        query = "Select sid, roomid, cid, mid, semester, years, capacity from section"
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        return result

    def getSectionById(self, sid):
        cur = self.conn.cursor()
        query = "select sid, roomid, cid, mid, semester, years, capacity from section where sid=%s"
        cur.execute(query, (sid,))
        result = cur.fetchone()
        return result

    def deleteSectionById(self, sid):
        cur = self.conn.cursor()
        query = "Delete from section where sid = %s"
        cur.execute(query, (sid,))
        rowcount = cur.rowcount
        self.conn.commit()
        return rowcount == 1

    def updateSectionById(self, sid, roomid, cid, mid, semester, years, capacity):
            cur = self.conn.cursor()
            query = "Update section set roomid= %s, cid=%s, mid=%s, semester=%s, years=%s, capacity=%s where sid = %s"
            cur.execute(query, (roomid, cid, mid , semester, years, capacity, sid))
            rowcount = cur.rowcount
            self.conn.commit()
            return rowcount == 1

    def getTotalSectionsPerYear(self):
        cur=self.conn.cursor()
        query="Select years, Count(*) from section group by years order by Count(*) desc"
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        return result

    def getMostTaughtPerSemester(self,  year, semester):
        cur = self.conn.cursor()
        query= "select s.cid, s.years, Count(*), semester, c.ccode, c.cname from section as s inner join class as c on s.cid = c.cid where s.years=%s and semester=%s group by s.cid, s.years, semester, c.ccode, c.cname order by Count(*) desc limit 3"
        cur.execute(query, (year, semester))
        result = []
        for row in cur:
            result.append(row)
        return result

    def getTopThreeLeastOfferedClasses(self):
        cur = self.conn.cursor()
        query = ("Select c.cid, c.cname, c.ccode, Count(*) from section as s inner join class as c on s.cid = c.cid group by c.cid, c.cname, c.ccode \
                order by Count(*) limit 3;")
        cur.execute(query)
        result = cur.fetchall()
        return result

    def closeConnection(self):
        if self.conn:
            self.conn.close()