import sqlite3
from datetime import date

from data.base import DB

class EquipmentsTable(DB):
    
    def __init__(self):
        super(EquipmentsTable, self).__init__()
        self.columns = ('employeeID', 'device_type', 'serial', 'make', 'model', 'status')
        self.table = 'equipment_table'

    def create_table(self):
        """
        Creates the office_table in the wadsworth db
        """
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            ID              INTEGER          PRIMARY KEY,
            employeeID      INTEGER,
            device_type     INTEGER,
            serial          VARCHAR(50),
            make            VARCHAR(50),
            model           VARCHAR(50),
            status          BOOLEAN
        )
        """
        self.execute(command)

    def insert_record(self, employeeID, device_type, serial, make, model):
        """
        Inserts into the database if a particular record does not exist
        """
        values = f"{employeeID}, {device_type}, '{serial}', '{make}', '{model}', 1"
        self.insert_or_replace(values, self.columns)
    

    def run(self):
        self.create_table()

class EmailTable(DB):

    def __init__(self):
        super(EmailTable, self).__init__()
        self.columns = ('employeeID', 'email', 'password')
        self.table = 'email_table'

    def create_table(self):
        """
        Creates the office_table in the wadsworth db
        """
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            ID              INTEGER          PRIMARY KEY,
            employeeID      INTEGER,
            email           VARCHAR(50),
            password        VARCHAR(100)
        )
        """
        self.execute(command)

    def run(self):
        self.create_table()



