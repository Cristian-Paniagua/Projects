import psycopg2
from .DatabaseConnection import DBConnection

dbConnection = DBConnection()

class UserLoginDao:
    def __init__(self):
        self.dbConnection = dbConnection
        self.conn = self.dbConnection.getConnection()

    def getUserByUsername(self, username):
        cur = self.conn.cursor()
        query = "SELECT id, username, password FROM users WHERE username = %s"
        cur.execute(query, (username,))
        user = cur.fetchone()
        return user

    def create_user(self, username, password):
        cur = self.conn.cursor()
        query = "INSERT INTO users (username, password) VALUES (%s, %s) returning id"
        cur.execute(query, (username, password))
        id = cur.fetchone()[0]
        self.conn.commit()
        return id


    def deleteUserById(self, user_id):
        cur = self.conn.cursor()
        query = "DELETE FROM users WHERE id = %s"
        cur.execute(query, (user_id,))
        rowcount = cur.rowcount
        self.conn.commit()
        return rowcount == 1

    def closeConnection(self):
        if self.conn:
            self.conn.close()
