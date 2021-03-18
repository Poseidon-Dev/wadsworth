import sqlite3
from datetime import date

from data.base import DB

class OfficeTable(DB):
    
    def __init__(self):
        super(OfficeTable, self).__init__()
        self.columns = ('office_keys', 'available', 'computer_name', 'email', 'date')
        self.table = 'office_table'

    def create_table(self):
        """
        Creates the office_table in the wadsworth db
        """
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            ID              INTEGER          PRIMARY KEY,
            office_keys     VARCHAR(30),
            available       BOOLEAN,
            computer_name   VARCHAR(50),
            email           VARCHAR(10),
            date            VARCHAR(20)
        )
        """
        self.execute(command)

    def insert_key(self, key):
        """
        Inserts a new office key into db
        """
        key = f"('{key}', 1)"
        self.insert_or_replace(columns='(office_keys, available)', values=key)

    def retrieve_and_log_key(self, computer, email):
        """
        Retrieves and returns an available key, logs computer and email. Then changes status
        to unavailable with current date
        """
        row = self.select_top_row(columns='available', values=1)
        try:
            self.update_record(row[0][0], (0, computer, email, date.today()),('available', 'computer_name', 'email', 'date'))
            return row
        except Exception as e:
            return f'There are no more keys in the table'
    
    def count_keys(self):
        """
        Returns a count of available keys 
        """
        return self.count_records("WHERE available=1")

    def select_all_active(self):
        """
        Returns a list of available keys
        """
        return self.select_all(table='office_table', where='WHERE available=1')

    def select_all_inactive(self):
        """
        Returns a list of unavailable keys
        """
        return self.select_all('WHERE available=0')
        
    def run(self):
        self.create_table()


