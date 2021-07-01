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

class EmployeePropertyTable(Query):

    def __init__(self):
        self.table = 'ee_property'
        self.columns = [
            ('id', 'SERIAL PRIMARY KEY'),
            ('employeeID', 'INT'),
            ('device_control', 'VARCHAR(50)'),
            ('property_type', 'INT'),
            ('description', 'VARCHAR'),
            ('assigned_date', 'DATE')
        ]
        Query.__init__(self, self.table, self.columns)
