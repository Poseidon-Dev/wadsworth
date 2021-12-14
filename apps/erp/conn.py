import pyodbc
import core.config

class ErpApiConn:

    def __init__(self):
        self.erp_conn = pyodbc.connect(f'DSN={core.config.ERP_HOST}; UID={core.config.ERP_UID}; PWD={core.config.ERP_PWD}')
        self.erp_cur = self.erp_conn.cursor()


    def erp_commmand(self, command):
        try:
            self.erp_cur.execute(command)
            records = self.erp_cur.fetchall()
            self.close()
            return list(records)
        except Exception as e:
            print(e)


    def close(self):
        self.erp_cur.close()
        self.erp_conn.close()