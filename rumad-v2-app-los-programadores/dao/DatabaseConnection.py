from config.dbconfig import pg_heroku, pg_config
import psycopg2
class DBConnection:
    def __init__(self):
        url = "dbname = %s password= %s host = %s port=%s user= %s"% \
             (pg_heroku['database'],
            pg_heroku['password'],
            pg_heroku['host'],
            pg_heroku['port'],
            pg_heroku['user'])


        self.conn = psycopg2.connect(url)
    def getConnection(self):
        return self.conn

    def closeConnection(self):
        if self.conn:
            self.conn.close()