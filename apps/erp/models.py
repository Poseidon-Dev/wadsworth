from apps.base import Database

class EmployeeTable(Database):
    
    def __init__(self):
        super(EmployeeTable, self).__init__()
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

    def fetch_like_last(self, lastname):
        command = f"""
        SELECT * FROM {self.table}
        WHERE last LIKE '{lastname}%'
        AND STATUS = 'A'
        ORDER BY id
        """
        return self.execute(command)

    def fetch_like_first(self, firstname):
        command = f"""
        SELECT * FROM {self.table}
        WHERE first LIKE '{firstname}%'
        AND STATUS = 'A'
        ORDER BY id
        """
        return self.execute(command)

    def fetch_like_first_last(self, firstname, lastname):
        command = f"""
        SELECT * FROM {self.table}
        WHERE first LIKE '{firstname}%'
        AND last LIKE '{lastname}%'
        AND STATUS = 'A'
        """
        return self.execute(command)

    def upsert_employees(self, values):
        command = f"""
        INSERT INTO {self.table} {self.columns}
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

    def run(self):
        self.create_table()

class DivisionTable(Database):
    def __init__(self):
        super(DivisionTable, self).__init__()
        self.table = 'division_table'
        self.columns = '(id, division)'
        self.key = 'division'

    def create_table(self):
        """
        Creates the division_table in the wadsworth db
        """
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            id              INT               PRIMARY KEY,
            division        VARCHAR(30)
        );
        """
        self.execute(command)

    def run(self):
        self.create_table()
        self.insert_single_record("98, '00 - Corporate'")
        self.insert_single_record("99, 'MISC'")
        self.insert_single_record("1, '01 - Tuscon'")
        self.insert_single_record("2, '02 - Phoenix'")
        self.insert_single_record("3, '03 - Hesperia'")
        self.insert_single_record("4, '04 - Corona'")
        self.insert_single_record("5, '05 - Vegas'")
        self.insert_single_record("6, '06 - Pipeline'")
        self.insert_single_record("7, '07 - Reno'")
        self.insert_single_record("8, '08 - Carson'")
        self.insert_single_record("9, '09 - Pacific'")
        self.insert_single_record("10, '10 - Bullhead'")
