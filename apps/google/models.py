from apps.base import Query

class GoogleTable(Query):

    def __init__(self):
        self.table='ee_email'
        self.columns = [
            ('id', 'SERIAL PRIMARY KEY' ),
            ('employeeID', 'INT'),
            ('email', 'VARCHAR(50)')
        ]
        Query.__init__(self, self.table, self.columns)
