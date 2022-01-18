from apps.base import Query
from apps.erp.conn import ErpApiConn

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
            ('division', 'INT REFERENCES ee_divisions(id) ON DELETE NO ACTION'),
            ('status', 'VARCHAR(30)'),
            ('position', 'VARCHAR(30)')
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

class Employee:
    def __init__(self, id: int=None, first: str=None, last: str=None, record=None):
        self._employee_id = id
        self._record = record
        self.id = self.record[0]
        self.first = self.record[1].capitalize()
        self.middle1 = self.record[2].capitalize()
        self.middle2 = self.record[3].capitalize()
        self.last = self.record[4].capitalize()
        self.security = self.record[5]
        self.status = self.record[7]
        self.position = self.record[8].capitalize()
        self._division = self.record[6]
        self._company_property = []
        self._fullname = ''

    @property
    def employee_id(self):
        if not self._employee_id:
            self._employee_id = self.id
        return self._employee_id

    @property
    def record(self):
        if self._record:
            return self._record      
        else:
            self._record = EmployeeTable().filter('id', self._employee_id).query()[0] 
            return self._record

    @property
    def record_query(self):
        if not self._record:
            self._record = EmployeeTable().filter('id', self.employee_id).query()[0]            
        return self._record

    @property
    def division(self):
        self._division = EmployeeDivisionTable().filter('id', self._division).query()[0][1]
        return self._division

    @property
    def company_property(self):
        self._company_property = EmployeePropertyTable().filter('employeeid', self.id).query()
        return self._company_property

    @property
    def full_name(self):
        middle = ''
        if self.middle1:
            middle = self.middle1[0]
        if self.middle2:
            middle += ' ' + self.middle2[0]
        self._fullname = f'{self.first} {middle} {self.last}'
        return self._fullname

    def __str__(self):
        return self.full_name
    
