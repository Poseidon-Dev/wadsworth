import pyodbc, os, sys
from datetime import date

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

from data import DB

class EmployeeTable(DB):
    
    def __init__(self):
        super(EmployeeTable, self).__init__()
        # self.erp_conn = pyodbc.connect(f'DSN={config.ERP_HOST}; UID={config.ERP_UID}; PWD={config.ERP_PWD}')
        # self.erp_cur = self.erp_conn.cursor()
        self.table = 'employee_table'
        self.columns = '(id, first, middle1, middle2, last, security, division, status)'

    def create_table(self):
        """
        Creates the employee_table in the wadsworth db
        """
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            id              INT            PRIMARY KEY,
            first           VARCHAR(30),
            middle1         VARCHAR(30),
            middle2         VARCHAR(30),
            last            VARCHAR(30),
            security        INT,
            division        INT            REFERENCES division_table(id) ON DELETE NO ACTION,
            status          VARCHAR(30)
        );
        """
        self.execute(command)

    def gather_data(self):
        command = """SELECT 
                    EMPLOYEENO, FIRSTNAME25, MIDDLENAME1, MIDDLENAME2, LASTNAME25, LVLCODE, 
                        CASE
                            WHEN LENGTH(DEPTNO) = 1 THEN DEPTNO
                            WHEN LENGTH(DEPTNO) = 2 THEN LEFT(DEPTNO, 1)
                            WHEN LENGTH(DEPTNO) = 3 THEN LEFT(DEPTNO, 2)
                            END
                        AS DIVISION, STATUSCODE
                    FROM CMSFIL.HRTEMP
                    WHERE COMPANYNO = 1 AND STATUSCODE = 'A' AND EMPLOYEENO > 0
                    """
        self.erp_cur.execute(command)
        rows = self.erp_cur.fetchall()
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

    def insert_data(self):
        records = self.gather_data()
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
            self.insert_or_replace(values, self.columns)

    def run(self):
        self.create_table()


