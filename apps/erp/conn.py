import pyodbc
import core.config

class ErpApiConn:

    connection_string = f'DSN={core.config.ERP_HOST}; UID={core.config.ERP_UID}; PWD={core.config.ERP_PWD}'

    def __init__(self):
        self.conn = pyodbc.connect(self.connection_string)
        self.cur = self.conn.cursor()

    def comm(self, command):
        try:
            self.cur.execute(command)
            records = self.cur.fetchall()
            self.close()
            return list(records)
        except Exception as e:
            print(e)


    def close(self):
        self.cur.close()
        self.conn.close()

    