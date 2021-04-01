from apps.base import Database
from datetime import date

class OfficeTable(Database):

    def __init__(self):
        super().__init__()
        self.columns = ('office_keys', 'available', 'computer_name', 'email', 'date')
        self.table = 'office_table'

    def create_table(self):
        """
        Creates the office_table in the wadsworth db
        """
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            id              SERIAL          PRIMARY KEY ,
            office_keys     VARCHAR(30),
            available       BOOLEAN,
            computer_name   VARCHAR(50),
            email           VARCHAR(50),
            date            VARCHAR(20)
        )
        """
        self.execute(command)
    
    def insert_key(self, key):
        """
        Inserts a new office key into db
        """
        key = f"('{key}', '1')"
        self.insert_or_replace(columns='(office_keys, available)', values=key)

    def retrieve_and_log_key(self, computer, email):
        """
        Retrieves and returns an available key, logs computer and email. Then changes status
        to unavailable with current date
        """
        row = self.select_top_row('available','true', order='ORDER BY available DESC')
        try:
            self.update_record(row[0], (0, computer, email, date.today()),('available', 'computer_name', 'email', 'date'))
            return row
        except Exception as e:
            return e
    
    def count_keys(self):
        """
        Returns a count of available keys 
        """
        return self.count_records(table='office_table', where="WHERE available=True")

    def select_all_active(self):
        """
        Returns a list of available keys
        """
        return self.select_all(table='office_table', where="WHERE available=True")

    def select_all_inactive(self):
        """
        Returns a list of unavailable keys
        """
        return self.select_all('WHERE available=0')
        
    def run(self):
        self.create_table()
        