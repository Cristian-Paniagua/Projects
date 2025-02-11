from .DatabaseConnection import DBConnection
import psycopg2

dbConnection = DBConnection()

class DaoMeeting:
    def __init__(self):
        self.dbConnection = dbConnection
        self.conn = self.dbConnection.getConnection()

    def insertMeeting(self, ccode, starttime, endtime, cdays):
        cur = self.conn.cursor()
        query = """
            INSERT INTO meeting (ccode, starttime, endtime, cdays) 
            VALUES (%s, %s, %s, %s) RETURNING mid
        """
        cur.execute(query, (ccode, starttime, endtime, cdays))
        self.conn.commit()
        mid = cur.fetchone()[0]
        cur.close()
        return mid

    def getAllMeetings(self):
        """Retrieve all meetings from the database."""
        cur = self.conn.cursor()
        query = "SELECT mid, ccode, starttime, endtime, cdays FROM meeting"
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        return result

    def getMeetingById(self, mid):
        """Retrieve a single meeting by ID."""
        cur = self.conn.cursor()
        query = "SELECT mid, ccode, starttime, endtime, cdays FROM meeting WHERE mid = %s"
        cur.execute(query, (mid,))
        meeting = cur.fetchone()
        cur.close()
        return meeting

    def updateMeeting(self, mid, ccode, starttime, endtime, cdays):
        """Update an existing meeting by ID."""
        cur = self.conn.cursor()
        query = """
            UPDATE meeting 
            SET ccode = %s, starttime = %s, endtime = %s, cdays = %s
            WHERE mid = %s
        """
        cur.execute(query, (ccode, starttime, endtime, cdays, mid))
        rowcount = cur.rowcount
        self.conn.commit()


        return rowcount == 1

    def deleteMeeting(self, mid):
        """Delete a meeting by ID."""
        cur = self.conn.cursor()
        query = "DELETE FROM meeting WHERE mid = %s"
        cur.execute(query, (mid,))
        self.conn.commit()
        rows_deleted = cur.rowcount
        cur.close()
        return rows_deleted > 0 

    def get_top_meetings_with_most_sections(self):
        """Retrieve the top 5 meetings with the most sections."""
        cur = self.conn.cursor()
        query = """
            SELECT m.mid, m.ccode, COUNT(*) as section_count, m.cdays
            FROM meeting as m
            INNER JOIN section as s ON m.mid = s.mid
            GROUP BY m.mid, m.ccode, m.cdays
            ORDER BY section_count DESC
            LIMIT 5;
        """
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        return result

    def closeConnection(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
