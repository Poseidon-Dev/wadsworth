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

    def run(self):
        self.create_table()

class CategoryTable(Database):

    def __init__(self):
        super(CategoryTable, self).__init__()
        self.table = 'category_table'
        self.columns = '(id, category)'
        self.key = 'category'

    def create_table(self):
        """
        Creates the category_table in the wadsworth db
        """
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            id              INT               PRIMARY KEY,
            category        VARCHAR(30)
        );
        """
        self.execute(command)

    def run(self):
        self.create_table()
        self.insert_single_record("1, 'iphone'")
        self.insert_single_record("2, 'ipad'")
        self.insert_single_record("3, 'Laptop'")
        self.insert_single_record("4, 'Desktop'")
        self.insert_single_record("5, 'Misc Device'")
        self.insert_single_record("6, 'Email'")
        self.insert_single_record("7, 'Software'")


class StatusTable(Database):
    def __init__(self):
        super(StatusTable, self).__init__()
        self.table = 'status_table'
        self.columns = '(id, status)'
        self.key = 'status'

    def create_table(self):
        """
        Creates the status_table in the wadsworth db
        """
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            id              INT               PRIMARY KEY,
            status          VARCHAR(30)
        );
        """
        self.execute(command)

    def run(self):
        self.create_table()
        self.insert_single_record("1, 'Active'")
        self.insert_single_record("2, 'Inactive'")
        self.insert_single_record("3, 'Broken'")
        self.insert_single_record("4, 'Returned'")


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

def employee_tables_setup():
    CategoryTable().run()
    StatusTable().run()
    DivisionTable().run()
    EmployeeTable().run()
