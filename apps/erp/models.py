from apps.base import Query

class EmployeeTable(Query):

    def __init__(self):
        self.table = 'ee_master'
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
        ]
        Query.__init__(self, self.table, self.columns)

class EmployeeUpdatesTable(EmployeeTable):

    def __init__(self):
        super().__init__()
        self.table = 'ee_updates'
        Query.__init__(self, self.table, self.columns)


class EmployeeLoggerTable(EmployeeTable):

    def __init__(self):
        super().__init__()
        self.table = 'ee_logger'
        self.columns.extend([
            ('date', 'VARCHAR(20)'),
            ('log', 'VARCHAR'),
            ('UNIQUE (id, date)', '')
        ])
        Query.__init__(self, self.table, self.columns)

class EmployeeDivisionTable(Query):

    def __init__(self):
        self.table = 'ee_divisions'
        self.columns = [
            ('id', 'INT PRIMARY KEY'),
            ('division', 'VARCHAR(30)'),
        ]
        Query.__init__(self, self.table, self.columns)

class EmployeeMessagesTable(Query):

    def __init__(self):
        self.table = 'ee_messages'
        self.columns = [
            ('id', 'BIGINT PRIMARY KEY'),
            ('date', 'VARCHAR(30)'),
        ]
        Query.__init__(self, self.table, self.columns)

# class EmployeeTable(Query):
    
#     def __init__(self):
#         self.table = 'employee_table'
#         self.columns = [
#             ('id', 'INT PRIMARY KEY'),
#             ('first', 'VARCHAR(30)'),
#             ('middle1', 'VARCHAR(30)'),
#             ('middle2', 'VARCHAR(30)'),
#             ('last', 'VARCHAR(30)'),
#             ('security', 'INT'),
#             ('division', 'INT REFERENCES division_table(id) ON DELETE NO ACTION'),
#             ('status', 'VARCHAR(30)'),
#             ('property_type', 'INT'),
#             ('device_control', 'VARCHAR(50)'),
#         ]
#         Query.__init__(self, self.table, self.columns)

#     def fetch(self):
#         command = """
#         SELECT EMP.EMPLOYEENO, 
#         REPLACE(TRIM(EMP.FIRSTNAME25), '''', ''),
#         REPLACE(TRIM(EMP.MIDDLENAME1), '''', ''),
#         REPLACE(TRIM(EMP.MIDDLENAME2), '''', ''),
#         REPLACE(TRIM(EMP.LASTNAME25), '''', ''),
#         CAST(EMP.LVLCODE AS INTEGER), 
#             CASE WHEN LENGTH(TRIM(EMP.DEPTNO)) = 1 THEN '98'
#             WHEN LENGTH(TRIM(EMP.DEPTNO)) = 2 THEN LEFT(EMP.DEPTNO, 1)
#             WHEN CAST(TRIM(EMP.DEPTNO) AS INTEGER) > 150 THEN '99'
#             WHEN LENGTH(TRIM(EMP.DEPTNO)) = 3 THEN LEFT(EMP.DEPTNO, 2) END
#         AS DIVISION, EMP.STATUSCODE, CAST(CPR.PROPERTYNO AS INTEGER), TRIM(CPR.CONTROLNO)
#         FROM CMSFIL.HRTEMP AS EMP
#         JOIN CMSFIL.HRTCPR AS CPR 
#             ON EMP.HRTEMPID = CPR.HRTEMPID
#         WHERE EMP.COMPANYNO = 1 
#         AND EMP.EMPLOYEENO > 0 
#         AND CPR.PROPERTYNO IN (2,4,5,9)
#         AND CPR.RTNDATE IS NULL 
#         AND CPR.EXPDATE IS NULL
#         """
#         conn = ErpApiConn()
#         conn.erp_cur.execute(command)
#         records = conn.erp_cur.fetchall()
#         conn.close()
#         return list(records)

#     def store(self):
#         records = self.fetch()
#         self.insert_many(self.cols, records)

#     def upsert_employees(self, values):
#         command = f"""
#         INSERT INTO {self.table} ({self.column_names_to_string()})
#         VALUES {values}
#         ON CONFLICT (id) DO UPDATE SET 
#             first = EXCLUDED.first,
#             middle1 = EXCLUDED.middle1,
#             middle2 = EXCLUDED.middle2,
#             last = EXCLUDED.last,
#             security = EXCLUDED.security,
#             division = EXCLUDED.division,
#             status = EXCLUDED.status,
#             property_type = EXCLUDED.property_type,
#             device_control = EXCLUDED.device_control;
#         """
#         self.execute(command)


# class EmployeeChangesTable(Query):

#     def __init__(self):
#         self.table = 'employee_changes_table'
#         self.columns = [
#             ('id', 'INT PRIMARY KEY'),
#             ('first', 'VARCHAR(30)'),
#             ('middle1', 'VARCHAR(30)'),
#             ('middle2', 'VARCHAR(30)'),
#             ('last', 'VARCHAR(30)'),
#             ('security', 'INT'),
#             ('division', 'INT REFERENCES division_table(id) ON DELETE NO ACTION'),
#             ('status', 'VARCHAR(30)'),
#             ('property_type', 'INT'),
#             ('device_control', 'VARCHAR(50)'),
#         ]
#         Query.__init__(self, self.table, self.columns)

#     def fetch(self):
#         command = """
#         SELECT EMP.EMPLOYEENO, 
#         REPLACE(TRIM(EMP.FIRSTNAME25), '''', ''),
#         REPLACE(TRIM(EMP.MIDDLENAME1), '''', ''),
#         REPLACE(TRIM(EMP.MIDDLENAME2), '''', ''),
#         REPLACE(TRIM(EMP.LASTNAME25), '''', ''),
#         CAST(EMP.LVLCODE AS INTEGER), 
#             CASE WHEN LENGTH(TRIM(EMP.DEPTNO)) = 1 THEN '98'
#             WHEN LENGTH(TRIM(EMP.DEPTNO)) = 2 THEN LEFT(EMP.DEPTNO, 1)
#             WHEN CAST(TRIM(EMP.DEPTNO) AS INTEGER) > 150 THEN '99'
#             WHEN LENGTH(TRIM(EMP.DEPTNO)) = 3 THEN LEFT(EMP.DEPTNO, 2) END
#         AS DIVISION, EMP.STATUSCODE, CAST(CPR.PROPERTYNO AS INTEGER), TRIM(CPR.CONTROLNO)
#         FROM CMSFIL.HRTEMP AS EMP
#         JOIN CMSFIL.HRTCPR AS CPR 
#             ON EMP.HRTEMPID = CPR.HRTEMPID
#         WHERE EMP.COMPANYNO = 1 
#         AND EMP.EMPLOYEENO > 0 
#         AND CPR.PROPERTYNO IN (2,4,5,9)
#         AND CPR.RTNDATE IS NULL 
#         AND CPR.EXPDATE IS NULL
#         """
#         conn = ErpApiConn()
#         conn.erp_cur.execute(command)
#         records = conn.erp_cur.fetchall()
#         conn.close()
#         return list(records)

#     def store(self):
#         records = self.fetch()
#         cols = ('id, first, middle1, middle2, last, security, division, status, property_type, device_control')
#         self.insert_many(cols, records)

#     def db_refresh(self):
#         command = f"""
#         DELETE FROM {self.table}
#         """
#         self.execute(command)
#         self.store()
#         return True

# class EmployeeLogger(Query):

#     def __init__(self):
#         self.table = 'employee_logger'
#         self.columns = [
#             ('id', 'SERIAL PRIMARY KEY'),
#             ('empid', 'INT'),
#             ('first', 'VARCHAR(30)'),
#             ('middle1', 'VARCHAR(30)'),
#             ('middle2', 'VARCHAR(30)'),
#             ('last', 'VARCHAR(30)'),
#             ('security', 'INT'),
#             ('division', 'INT REFERENCES division_table(id) ON DELETE NO ACTION'),
#             ('status', 'VARCHAR(30)'),
#             ('property_type', 'INT'),
#             ('device_control', 'VARCHAR(50)'),
#             ('date', 'VARCHAR(20)'),
#             ('log', 'VARCHAR')
#         ]
#         self.cols = ('id, first, middle1, middle2, last, security, division, status, property_type, device_control')
#         Query.__init__(self, self.table, self.columns)
#         ErpApiConn.__init__(self)

#     def changes(self, t_one='employee_table', t_two='employee_changes_table'):
#         command = f"""
#         SELECT * FROM {t_two}
#         EXCEPT
#         SELECT * FROM {t_one};
#         """
#         data = self.execute(command)
#         return data

#     def upsert_logger(self, cols, vals):
#         command = f"""
#         INSERT INTO {self.table} ({cols})
#         VALUES {vals}
#         ON CONFLICT (idx_id_date) DO UPDATE SET
#             first = EXCLUDED.first,
#             middle1 = EXCLUDED.middle1,
#             middle2 = EXCLUDED.middle2,
#             last = EXCLUDED.last,
#             security = EXCLUDED.security,
#             division = EXCLUDED.division,
#             status = EXCLUDED.status,
#             property_type = EXCLUDED.property_type,
#             device_control = EXCLUDED.device_control;
#         """
#         self.execute(command)

#     def upsert_employees(self, values):
#         command = f"""
#         INSERT INTO employee_table ({self.cols})
#         VALUES {values}
#         ON CONFLICT (id) DO UPDATE SET 
#             first = EXCLUDED.first,
#             middle1 = EXCLUDED.middle1,
#             middle2 = EXCLUDED.middle2,
#             last = EXCLUDED.last,
#             security = EXCLUDED.security,
#             division = EXCLUDED.division,
#             status = EXCLUDED.status,
#             property_type = EXCLUDED.property_type,
#             device_control = EXCLUDED.device_control;
#         """
#         self.execute(command)

# class DivisionTable(Query):

#     def __init__(self):
#         self.table = 'division_table'
#         self.columns = [
#             ('id', 'INT PRIMARY KEY'),
#             ('division', 'VARCHAR(30)'),
#         ]
#         Query.__init__(self, self.table, self.columns)

# class Messages(Query):

#     def __init__(self):
#         self.table = 'messages'
#         self.columns = [
#             ('id', 'BIGINT PRIMARY KEY'),
#             ('date', 'VARCHAR(30)'),
#         ]
#         Query.__init__(self, self.table, self.columns)


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

