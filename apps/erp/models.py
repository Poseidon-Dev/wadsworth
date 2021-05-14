from datetime import date

from core.shared.utils import Timer
from apps.base import Database, Query, TableBuilder
from apps.erp.migrations import ErpApiConn

from .utils import clean_name

class EmployeeTable(Query, ErpApiConn):

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
        ]
        Query.__init__(self, self.table)
        ErpApiConn.__init__(self)

    def build(self):
        TableBuilder(self.table, self.columns).build()

    def fetch(self):
        command = """
            SELECT 
            EMPLOYEENO, 
            REPLACE(TRIM(FIRSTNAME25), '''', ''),
            REPLACE(TRIM(MIDDLENAME1), '''', ''),
            REPLACE(TRIM(MIDDLENAME2), '''', ''),
            REPLACE(TRIM(LASTNAME25), '''', ''),
            CAST(LVLCODE AS INTEGER), 
                CASE
                    WHEN LENGTH(TRIM(DEPTNO)) = 1 THEN '98'
                    WHEN LENGTH(TRIM(DEPTNO)) = 2 THEN LEFT(DEPTNO, 1)
                    WHEN CAST(TRIM(DEPTNO) AS INTEGER) > 150 THEN '99'
                    WHEN LENGTH(TRIM(DEPTNO)) = 3 THEN LEFT(DEPTNO, 2)
                    END
                AS DIVISION, STATUSCODE
            FROM CMSFIL.HRTEMP
            WHERE COMPANYNO = 1 AND EMPLOYEENO > 0
        """
        self.erp_cur.execute(command)
        records = self.erp_cur.fetchall()
        return list(records)

    def store(self):
        records = self.fetch()
        cols = ('id, first, middle1, middle2, last, security, division, status')
        self.insert_many(cols, records)


class EmployeeChangesTable(Query, ErpApiConn):

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
        ]
        Query.__init__(self, self.table)
        ErpApiConn.__init__(self)

    def build(self):
        TableBuilder(self.table, self.columns).build()

    def fetch(self):
        command = """
            SELECT 
            EMPLOYEENO, 
            REPLACE(TRIM(FIRSTNAME25), '''', ''),
            REPLACE(TRIM(MIDDLENAME1), '''', ''),
            REPLACE(TRIM(MIDDLENAME2), '''', ''),
            REPLACE(TRIM(LASTNAME25), '''', ''),
            CAST(LVLCODE AS INTEGER), 
                CASE
                    WHEN LENGTH(TRIM(DEPTNO)) = 1 THEN '98'
                    WHEN LENGTH(TRIM(DEPTNO)) = 2 THEN LEFT(DEPTNO, 1)
                    WHEN CAST(TRIM(DEPTNO) AS INTEGER) > 150 THEN '99'
                    WHEN LENGTH(TRIM(DEPTNO)) = 3 THEN LEFT(DEPTNO, 2)
                    END
                AS DIVISION, STATUSCODE
            FROM CMSFIL.HRTEMP
            WHERE COMPANYNO = 1 AND EMPLOYEENO > 0
        """
        self.erp_cur.execute(command)
        records = self.erp_cur.fetchall()
        return list(records)

    def store(self):
        records = self.fetch()
        cols = ('id, first, middle1, middle2, last, security, division, status')
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
            ('date', 'VARCHAR(20)'),
            ('type', 'VARCHAR(2)' )
        ]
        self.cols = ('id, first, middle1, middle2, last, security, division, status')
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
            status = EXCLUDED.status
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
            status = EXCLUDED.status
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
