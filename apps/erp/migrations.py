import re
from apps.base.queries import Query
from datetime import date
import pyodbc, os 
import core.config

from .utils import clean_name
from .models import EmployeeLoggerTable, EmployeeTable, EmployeeUpdatesTable, EmployeeDivisionTable, EmployeePropertyTable
from .conn import ErpApiConn

class EmployeeFetch:

    def fetch(self):
        command = """
            SELECT EMP.EMPLOYEENO, 
            REPLACE(TRIM(EMP.FIRSTNAME25), '''', ''),
            REPLACE(TRIM(EMP.MIDDLENAME1), '''', ''),
            REPLACE(TRIM(EMP.MIDDLENAME2), '''', ''),
            REPLACE(TRIM(EMP.LASTNAME25), '''', ''),
            CAST(EMP.LVLCODE AS INTEGER), 
                CASE WHEN LENGTH(TRIM(EMP.DEPTNO)) = 1 THEN '98'
                WHEN LENGTH(TRIM(EMP.DEPTNO)) = 2 THEN LEFT(EMP.DEPTNO, 1)
                WHEN CAST(TRIM(EMP.DEPTNO) AS INTEGER) > 150 THEN '99'
                WHEN LENGTH(TRIM(EMP.DEPTNO)) = 3 THEN LEFT(EMP.DEPTNO, 2) END
            AS DIVISION, EMP.STATUSCODE
            FROM CMSFIL.HRTEMP AS EMP
            WHERE EMP.COMPANYNO = 1 
            AND EMP.EMPLOYEENO > 0 
            """
        return ErpApiConn().erp_commmand(command)

class EmployeeMasterMigration(EmployeeTable):

    def __init__(self):
        super().__init__()

    def store(self):
        records = EmployeeFetch().fetch()
        self.insert_many(self.column_names_to_string(), records)

    def refresh(self):
        try:
            self.delete_table()
            self.store()
        except Exception as e:
            return False
        return True

    def upsert_records(self, values):
        command = f"""
        INSERT INTO {self.table} ({self.column_names_to_string()})
        VALUES {values}
        ON CONFLICT (id) DO UPDATE SET 
            first = EXCLUDED.first,
            middle1 = EXCLUDED.middle1,
            middle2 = EXCLUDED.middle2,
            last = EXCLUDED.last,
            security = EXCLUDED.security,
            division = EXCLUDED.division,
            status = EXCLUDED.status,
        """
        self.execute(command)

class EmployeeUpdatesMigration(EmployeeUpdatesTable):

    def __init__(self):
        super().__init__()

    def store(self):
        records = EmployeeFetch().fetch()
        self.insert_many(self.column_names_to_string(), records)

    def refresh(self):
        try:
            self.delete_table()
            self.store()
        except Exception as e:
            return False
        return True

class EmployeeDivisionMigration(EmployeeDivisionTable):

    def __init__(self):
        super().__init__()

    def insert_divisions(self):
        values = (
            """(1, '01-TUC'), (2, '02-PHX'), (3, '03-HES'), (4, '04-COR'), 
            (5, '05-VGS'), (6, '06-PIP'), (7, '07-NNV'), (8, '08-CAR'), 
            (9, '09-NHS'), (10, '10-BHC'), (98, '00-CRP'), (99, 'MISC')
            """
        )
        command = f"""
        INSERT INTO {self.table} ({self.column_names_to_string()})
        VALUES {values}
        ON CONFLICT (id) DO UPDATE SET
            id = EXCLUDED.id,
            division = EXCLUDED.division
        """
        self.execute(command)

class EmployeeLoggerMigrations(EmployeeLoggerTable):
    
    def __init__(self):
        super().__init__()

    def collect_changes(self):
        command = f"""
        SELECT * FROM {EmployeeUpdatesTable().table}
        EXCEPT
        SELECT * FROM {EmployeeTable().table}
        """
        return self.execute(command)

    def upsert_logger(self, vals):
        command = f"""
        INSERT INTO {self.table} ({self.column_names_to_string()})
        VALUES {vals}
        ON CONFLICT ON CONSTRAINT ee_logger_id_date_key 
        DO UPDATE SET
            first = EXCLUDED.first,
            middle1 = EXCLUDED.middle1,
            middle2 = EXCLUDED.middle2,
            last = EXCLUDED.last,
            security = EXCLUDED.security,
            division = EXCLUDED.division,
            status = EXCLUDED.status,
        """
        self.execute(command)

class EmployeePropertyMigrations(EmployeePropertyTable):
    
    def fetch(self):
        command = """
        SELECT EMP.EMPLOYEENO, TRIM(CPR.CONTROLNO), CAST(CPR.PROPERTYNO AS INTEGER),
        TRIM(CPR.DESCRIPTION), CPR.ASGDATE
        FROM CMSFIL.HRTCPR AS CPR
        JOIN CMSFIL.HRTEMP AS EMP 
            ON EMP.HRTEMPID = CPR.HRTEMPID
        WHERE EMP.COMPANYNO = 1 
        AND EMP.EMPLOYEENO > 0 
        AND CPR.PROPERTYNO IN (1,2,4,5,9,10,70,75)
        AND CPR.RETIREDDATE IS NULL 
        AND CPR.EXPDATE IS NULL
        """
        return ErpApiConn().erp_commmand(command)

    def flatten_data(self):
        records = list(self.fetch())
        for record in records:
            if not record[1]:
                record[1] = 'None'
            record[3] = record[3].replace("'", '')
            if record[4]:
                record[4]= date.strftime(record[4], '%Y-%m-%d')
            else:
                record[4] = date.strftime(date(2010, 1, 1),'%Y-%m-%d')
        return records
        
    def store(self):
        records = self.flatten_data()
        self.insert_many(self.column_names_to_string()[4:], records)

    def refresh(self):
        try:
            self.delete_table()
            self.store()
        except Exception as e:
            return False
        return True

    