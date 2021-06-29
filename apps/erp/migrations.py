from apps.base.queries import Query
import pyodbc, os 
import core.config

from .utils import clean_name
from .models import EmployeeLoggerTable, EmployeeTable, EmployeeUpdatesTable, EmployeeDivisionTable
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
            AS DIVISION, EMP.STATUSCODE, CAST(CPR.PROPERTYNO AS INTEGER), TRIM(CPR.CONTROLNO)
            FROM CMSFIL.HRTEMP AS EMP
            JOIN CMSFIL.HRTCPR AS CPR 
                ON EMP.HRTEMPID = CPR.HRTEMPID
            WHERE EMP.COMPANYNO = 1 
            AND EMP.EMPLOYEENO > 0 
            AND CPR.PROPERTYNO IN (2,4,5,9)
            AND CPR.RTNDATE IS NULL 
            AND CPR.EXPDATE IS NULL
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
            property_type = EXCLUDED.property_type,
            device_control = EXCLUDED.device_control;
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
            """(1, '01-Tuc'), (2, '02-Phx'), (3, '03-Hes'), (4, '04-Cor'), 
            (5, '05-Vgs'), (6, '06-Pip'), (7, '07-Nnv'), (8, '08-Car'), 
            (9, '09-Nhs'), (10, '10-bhc'), (98, '00-Corp'), (99, 'Misc')
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
            property_type = EXCLUDED.property_type,
            device_control = EXCLUDED.device_control;
        """
        self.execute(command)


    