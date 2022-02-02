import pyodbc
import core.config

class ErpApiConn:

    connection_string = f'DSN={core.config.ECMS_HOST}; UID={core.config.ECMS_UID}; PWD={core.config.ECMS_PWD}'

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

    