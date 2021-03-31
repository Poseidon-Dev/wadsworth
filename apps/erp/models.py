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
