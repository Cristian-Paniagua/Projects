import sqlite3
import pandas as pd
from dao.DaoRequisite import DaoRequisite
from dao.DaoClass import DaoClass



sqlite_conn = sqlite3.connect('files/requisites.db')
query = "SELECT * FROM requisites"
data = pd.read_sql(query, sqlite_conn)


data = data.astype({
    'cid': 'int',
    'requisiteid': 'int',
    'preReq': 'str'
})


sqlite_conn.close()


daoReq = DaoRequisite()

print(data)
for index, row in data.iterrows():
        code = row['cid']
        codeReq = row['requisiteid']

        daoReq.insertRequisite(code, codeReq, row['preReq'])



daoReq.closeConnection()


