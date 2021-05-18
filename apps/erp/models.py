from datetime import date

from core.shared.utils import Timer, strip_special
from apps.base import Database, Query, TableBuilder
from apps.erp.migrations import ErpApiConn

from .utils import clean_name

class EmployeeTable(Query):

    def __init__(self):
        self.table = 'employee_table'
        self.columns = [
            ('id', 'INT PRIMARY KEY'),
            ('first', 'VARCHAR(30)'),
            ('middle1', 'VARCHAR(30)'),
            ('middle2', 'VARCHAR(30)'),
            ('last', 'VARCHAR(30)'),
            ('security', 'INT'),
            ('division', 'INT REFERENCES division_table(id) ON DELETE NO ACTION'),
            ('status', 'VARCHAR(30)'),
            ('property_type', 'INT'),
            ('device_control', 'VARCHAR(50)'),
            ('device_description', 'VARCHAR'),
        ]
        Query.__init__(self, self.table)

    def build(self):
        TableBuilder(self.table, self.columns).build()

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
        AS DIVISION, EMP.STATUSCODE, CAST(CPR.PROPERTYNO AS INTEGER), TRIM(CPR.CONTROLNO),
        REPLACE(REPLACE(TRIM(CPR.DESCRIPTION), '''', ''), CHAR(92), '')
        FROM CMSFIL.HRTEMP AS EMP
        JOIN CMSFIL.HRTCPR AS CPR 
            ON EMP.HRTEMPID = CPR.HRTEMPID
        WHERE EMP.COMPANYNO = 1 
        AND EMP.EMPLOYEENO > 0 
        AND CPR.PROPERTYNO IN (2,4,5,9)
        AND CPR.RTNDATE IS NULL 
        AND CPR.EXPDATE IS NULL
        """
        conn = ErpApiConn()
        conn.erp_cur.execute(command)
        records = conn.erp_cur.fetchall()

        conn.close()
        return list(records)

    def store(self):
        records = self.fetch()
        cols = ('id, first, middle1, middle2, last, security, division, status, property_type, device_control, device_description')
        self.insert_many(cols, records)


class EmployeeChangesTable(Query):

    def __init__(self):
        self.table = 'employee_changes_table'
        self.columns = [
            ('id', 'INT PRIMARY KEY'),
            ('first', 'VARCHAR(30)'),
            ('middle1', 'VARCHAR(30)'),
            ('middle2', 'VARCHAR(30)'),
            ('last', 'VARCHAR(30)'),
            ('security', 'INT'),
            ('division', 'INT REFERENCES division_table(id) ON DELETE NO ACTION'),
            ('status', 'VARCHAR(30)'),
            ('property_type', 'INT'),
            ('device_control', 'VARCHAR(50)'),
            ('device_description', 'VARCHAR'),
        ]
        Query.__init__(self, self.table)

    def build(self):
        TableBuilder(self.table, self.columns).build()

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
        AS DIVISION, EMP.STATUSCODE, CAST(CPR.PROPERTYNO AS INTEGER), TRIM(CPR.CONTROLNO), 
        REPLACE(REPLACE(TRIM(CPR.DESCRIPTION), '''', ''), CHAR(92), '')
        FROM CMSFIL.HRTEMP AS EMP
        JOIN CMSFIL.HRTCPR AS CPR 
            ON EMP.HRTEMPID = CPR.HRTEMPID
        WHERE EMP.COMPANYNO = 1 
        AND EMP.EMPLOYEENO > 0 
        AND CPR.PROPERTYNO IN (2,4,5,9)
        AND CPR.RTNDATE IS NULL 
        AND CPR.EXPDATE IS NULL
        """
        conn = ErpApiConn()
        conn.erp_cur.execute(command)
        records = conn.erp_cur.fetchall()
        conn.close()
        return list(records)

    def store(self):
        records = self.fetch()
        cols = ('id, first, middle1, middle2, last, security, division, status, property_type, device_control, device_description')
        self.insert_many(cols, records)

    def db_refresh(self):
        command = f"""
        DELETE FROM {self.table}
        """
        self.execute(command)
        self.store()
        return True

class EmployeeLogger(Query):

    def __init__(self):
        self.table = 'employee_logger'
        self.columns = [
            ('id', 'SERIAL PRIMARY KEY'),
            ('empid', 'INT'),
            ('first', 'VARCHAR(30)'),
            ('middle1', 'VARCHAR(30)'),
            ('middle2', 'VARCHAR(30)'),
            ('last', 'VARCHAR(30)'),
            ('security', 'INT'),
            ('division', 'INT REFERENCES division_table(id) ON DELETE NO ACTION'),
            ('status', 'VARCHAR(30)'),
            ('property_type', 'INT'),
            ('device_control', 'VARCHAR(50)'),
            ('device_description', 'VARCHAR'),
            ('date', 'VARCHAR(20)'),
            ('log', 'VARCHAR')
        ]
        self.cols = ('id, first, middle1, middle2, last, security, division, status, property_type, device_control, device_description')
        Query.__init__(self, self.table)
        ErpApiConn.__init__(self)
    
    def build(self):
        TableBuilder(self.table, self.columns).build()

    def changes(self, t_one='employee_table', t_two='employee_changes_table'):
        command = f"""
        SELECT * FROM {t_two}
        EXCEPT
        SELECT * FROM {t_one};
        """
        data = self.execute(command)
        return data

    def upsert_logger(self, cols, vals):
        command = f"""
        INSERT INTO {self.table} ({cols})
        VALUES {vals}
        ON CONFLICT (idx_id_date) DO UPDATE SET
            first = EXCLUDED.first,
            middle1 = EXCLUDED.middle1,
            middle2 = EXCLUDED.middle2,
            last = EXCLUDED.last,
            security = EXCLUDED.security,
            division = EXCLUDED.division,
            status = EXCLUDED.status,
            property_type = EXCLUDED.property_type,
            device_control = EXCLUDED.device_control,
            device_description = EXCLUDED.device_description
        """
        self.execute(command)

    def upsert_employees(self, values):
        command = f"""
        INSERT INTO employee_table ({self.cols})
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
            device_control = EXCLUDED.device_control,
            device_description = EXCLUDED.device_description
        """
        self.execute(command)

class DivisionTable(Query):

    def __init__(self):
        self.table = 'division_table'
        self.columns = [
            ('id', 'INT PRIMARY KEY'),
            ('division', 'VARCHAR(30)'),
        ]
        Query.__init__(self, self.table)

    def build(self):
        TableBuilder(self.table, self.columns).build()

class Messages(Query):

    def __init__(self):
        self.table = 'messages'
        self.columns = [
            ('id', 'BIGINT PRIMARY KEY'),
            ('date', 'VARCHAR(30)'),
        ]
        Query.__init__(self, self.table)

    def build(self):
        TableBuilder(self.table, self.columns).build()

    
# class EmployeeTable(Database):
    
#     def __init__(self):
#         super(EmployeeTable, self).__init__()
#         self.table = 'employee_table'
#         self.columns = '(id, first, middle1, middle2, last, security, division, status)'

#     def create_table(self):
#         """
#         Creates the employee_table in the wadsworth db
#         """
#         command = f"""
#         CREATE TABLE IF NOT EXISTS
#         {self.table}(
#             id              INT            PRIMARY KEY,
#             first           VARCHAR(30),
#             middle1         VARCHAR(30),
#             middle2         VARCHAR(30),
#             last            VARCHAR(30),
#             security        INT,
#             division        INT            REFERENCES division_table(id) ON DELETE NO ACTION,
#             status          VARCHAR(30)
#         );
#         """
#         self.execute(command)

#     def fetch_like_last(self, lastname):
#         command = f"""
#         SELECT * FROM {self.table}
#         WHERE last LIKE '{lastname}%'
#         ORDER BY id
#         """
#         return self.execute(command)

#     def fetch_like_first(self, firstname):
#         command = f"""
#         SELECT * FROM {self.table}
#         WHERE first LIKE '{firstname}%'
#         ORDER BY id
#         """
#         return self.execute(command)

#     def fetch_like_first_last(self, firstname, lastname):
#         command = f"""
#         SELECT * FROM {self.table}
#         WHERE first LIKE '{firstname}%'
#         AND last LIKE '{lastname}%'
#         """
#         return self.execute(command)

    # def upsert_employees(self, values):
    #     command = f"""
    #     INSERT INTO {self.table} {self.columns}
    #     VALUES {values}
    #     ON CONFLICT (id) DO UPDATE SET 
    #         first = EXCLUDED.first,
    #         middle1 = EXCLUDED.middle1,
    #         middle2 = EXCLUDED.middle2,
    #         last = EXCLUDED.last,
    #         security = EXCLUDED.security,
    #         division = EXCLUDED.division,
    #         status = EXCLUDED.status
    #     """
    #     self.execute(command)

#     def run(self):
#         self.create_table()


# class DivisionTable(Database):
#     def __init__(self):
#         super(DivisionTable, self).__init__()
#         self.table = 'division_table'
#         self.columns = '(id, division)'
#         self.key = 'division'

#     def create_table(self):
#         """
#         Creates the division_table in the wadsworth db
#         """
#         command = f"""
#         CREATE TABLE IF NOT EXISTS
#         {self.table}(
#             id              INT               PRIMARY KEY,
#             division        VARCHAR(30)
#         );
#         """
#         self.execute(command)

#     def run(self):
#         self.create_table()
#         self.insert_single_record("98, '00 - Corporate'")
#         self.insert_single_record("99, 'MISC'")
#         self.insert_single_record("1, '01 - Tuscon'")
#         self.insert_single_record("2, '02 - Phoenix'")
#         self.insert_single_record("3, '03 - Hesperia'")
#         self.insert_single_record("4, '04 - Corona'")
#         self.insert_single_record("5, '05 - Vegas'")
#         self.insert_single_record("6, '06 - Pipeline'")
#         self.insert_single_record("7, '07 - Reno'")
#         self.insert_single_record("8, '08 - Carson'")
#         self.insert_single_record("9, '09 - Pacific'")
#         self.insert_single_record("10, '10 - Bullhead'")
