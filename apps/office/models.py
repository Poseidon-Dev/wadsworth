from apps.base import Database, Query, TableBuilder
from datetime import date

class OfficeTable(Query):
    """
    An Office Keys table modeule that collects and stores office keys
    and their users based on entry date
    """
    def __init__(self):
        self.table = 'office_table'
        self.columns = [
            ('id', 'SERIAL PRIMARY KEY'),
            ('office_keys', 'VARCHAR(30) UNIQUE'),
            ('available', 'BOOLEAN'),
            ('computer_name', 'VARCHAR(50)'),
            ('email' ,'VARCHAR(50)'),
            ('date' ,'VARCHAR(20)')
        ]
        Query.__init__(self, self.table, self.columns)

    def retrieve_and_log_key(self, update):
        """ 
        Retrieves and returns the last-in available key in office table
        Updates the record with data provide as a list of tuples
        """
        record = self.available().select_first().query()
        if record:
            update.append(('date', date.today()))
            update.append(('available', 0))
            command = self.update_record(record, update)
            self.execute(command)
        return record

    def available(self):
        """ Returns available keys in office table """
        return self.filter('available', 1)

    def unavailable(self):
        """ Return unavailable keys in office table """
        return self.filter('available', 0)

    def count_available(self):
        """
        Returns a count of available keys 
        """
        return len(self.available().query())


# class OfficeTable(Database):

#     def __init__(self):
#         super().__init__()
#         self.columns = ('office_keys', 'available', 'computer_name', 'email', 'date')
#         self.table = 'office_table'

#     def create_table(self):
#         """
#         Creates the office_table in the wadsworth db
#         """
#         command = f"""
#         CREATE TABLE IF NOT EXISTS
#         {self.table}(
#             id              SERIAL          PRIMARY KEY ,
#             office_keys     VARCHAR(30)     UNIQUE,
#             available       BOOLEAN,
#             computer_name   VARCHAR(50),
#             email           VARCHAR(50),
#             date            VARCHAR(20)
#         )
#         """
#         self.execute(command)
    
#     def insert_key(self, key):
#         """
#         Inserts a new office key into db
#         """
#         values = f"('{key}', '1')"
#         return self.insert_or_replace(columns='(office_keys, available)', values=values)
       

#     def retrieve_and_log_key(self, computer, email):
#         """
#         Retrieves and returns an available key, logs computer and email. Then changes status
#         to unavailable with current date
#         """
#         row = self.select_top_row('available','true', order='ORDER BY available DESC')
#         try:
#             self.update_record(row[0], (0, computer, email, date.today()),('available', 'computer_name', 'email', 'date'))
#             return row
#         except Exception as e:
#             return e
    
#     def count_keys(self):
#         """
#         Returns a count of available keys 
#         """
#         return self.count_records(table='office_table', where="WHERE available=True")

#     def select_all_active(self):
#         """
#         Returns a list of available keys
#         """
#         return self.select_all(table='office_table', where="WHERE available=True")

#     def select_all_inactive(self):
#         """
#         Returns a list of unavailable keys
#         """
#         return self.select_all('WHERE available=0')
        
#     def run(self):
#         self.create_table()
        