import pyodbc, os 
import core.config

from .models import EmployeeTable

class ErpApi(EmployeeTable):

    def __init__(self):
        super(ErpApi, self).__init__()
        self.erp_conn = pyodbc.connect(f'DSN={core.config.ERP_HOST}; UID={core.config.ERP_UID}; PWD={core.config.ERP_PWD}')
        self.erp_cur = self.erp_conn.cursor()

    def pull_employees(self):
        command = """SELECT 
                    EMPLOYEENO, FIRSTNAME25, MIDDLENAME1, MIDDLENAME2, LASTNAME25, LVLCODE, 
                        CASE
                            WHEN LENGTH(TRIM(DEPTNO)) = 1 THEN '98'
                            WHEN LENGTH(TRIM(DEPTNO)) = 2 THEN LEFT(DEPTNO, 1)
                            WHEN LENGTH(TRIM(DEPTNO)) = 3 THEN LEFT(DEPTNO, 2)
                            END
                        AS DIVISION, STATUSCODE
                    FROM CMSFIL.HRTEMP
                    WHERE COMPANYNO = 1 AND STATUSCODE = 'A' AND EMPLOYEENO > 0
                    """
        self.erp_cur.execute(command)
        rows = self.erp_cur.fetchall()
        # self.erp_conn.close()
        records = [
            {
            'EmployeID' : int(row[0]),
            'FirstName' : str(row[1]).strip(),
            'Middle1' : str(row[2]).strip(),
            'Middle2' : str(row[3]).strip(),
            'LastName' : str(row[4]).strip(),
            'SecurityLevel' : int(row[5]),
            'Department' : int(row[6]),
            'Status' : str(row[7]).strip(),
            }
            for row in rows
        ]
        return records

    def insert_employees(self):
        records = self.pull_employees()
        for record in records:
            eid = str(record['EmployeID']).capitalize() 
            first = str(record['FirstName']).capitalize() 
            middle1 = str(record['Middle1']).capitalize() 
            middle2 = str(record['Middle2']).capitalize() 
            last = str(record['LastName']).capitalize() 
            security = str(record['SecurityLevel'])
            division = str(record['Department']).capitalize()
            status = str(record['Status']).capitalize()
            values = (eid, first, middle1, middle2, last, security, division, status)
            self.upsert_employees(values)

    def run(self):
        self.insert_employees()
