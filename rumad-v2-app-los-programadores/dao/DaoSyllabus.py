from .DatabaseConnection import DBConnection
from dao.DaoClass import DaoClass
import psycopg2

class DaoSyllabus:
    def __init__(self):
        self.dbConnection = DBConnection()
        self.conn = self.dbConnection.getConnection()

    def insertSyllabus(self, syllabus):
            cursor = self.conn.cursor()
            ClassDao = DaoClass()
            cid = ClassDao.getIdByCode(syllabus[0], syllabus[1])
            query = "insert into syllabus (courseid, embedding_text, chunk) values (%s,%s,%s) returning chunkid"
            cursor.execute(query, (cid,syllabus[2],syllabus[3]))
            self.conn.commit()
            result = cursor.fetchone()
            return result

    def getSyllabus(self, emb, cid):
        cursor = self.conn.cursor()
        if cid:
            query = "select courseid, chunkid, embedding_text <=> %s as distance, chunk from syllabus where courseid = %s order by distance limit 30"
            cursor.execute(query, (emb, cid))
        else:
            query= "select courseid, chunkid, embedding_text <=> %s as distance, chunk from syllabus order by distance limit 30"
            cursor.execute(query, (emb,))
        result=[]
        for row in cursor:
            result.append(row)
        return result

    def get_course_id(self, course_code):
        cursor = self.conn.cursor()
        query = "SELECT id FROM course WHERE ccode = %s"
        cursor.execute(query, (course_code,))
        result = cursor.fetchone()
        return result[0] if result else None

    def closeConnection(self):
        self.dbConnection.closeConnection()

