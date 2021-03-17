import sqlite3, os, sys
from datetime import date

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

class DB:

    def __init__(self):
        self.connection = sqlite3.connect(config.DB_LOCATION)
        self.cursor = self.connection.cursor()
        self.table = ''
        self.columns = tuple()

    def execute(self, command):
        print(command)
        self.cursor.execute(command)
        result = self.cursor.fetchall()
        self.connection.commit()
        return result

    # General Select Queries
    def select_all(self, table=None, where=''):
        if not table:
            table = self.table
        command = f"""
        SELECT * FROM {table}
        {where}
        """
        return self.execute(command)

    def select_columns(self, columns=None, table=None, where='',):
        if not table:
            table = self.table
        if not columns:
            columns = self.columns
            columns = str(columns).replace('(', '')
            columns = str(columns).replace(')', '')
            columns = str(columns).replace("'", '')
        command = f"""
        SELECT {columns} FROM {table}
        {where}
        """
        return self.execute(command)

    def select_row_by_key(self, table, key):
        command = f"""
        SELECT * FROM {table}
        WHERE ID = {key}
        """
        return self.execute(command)

    def select_top_row(self, columns, values):
        command = f"""
        SELECT * FROM {self.table}
        WHERE {columns} = {values}
        ORDER BY available DESC
        LIMIT 1
        """
        return self.execute(command)

    def count_records(self, where=''):
        command = f"""
        SELECT COUNT (*) FROM {self.table}
        {where}
        """
        return self.execute(command)

    # General Delete Queries
    def delete_row_by_key(self, key, table=None):
        if not table:
            table = self.table
        command = f"""
        DELETE FROM {table}
        WHERE ID = {key}
        """
        print(command)
        return self.execute(command)

    def clear_table(self, table=None):
        if not table:
            table = self.table
        command = f"""
        DELETE FROM {table}
        """
        self.execute(command)

    def drop_table(self, table):
        command = f"""
        DROP TABLE IF EXISTS {table}
        """
        self.execute(command)

    # General Insert Queries
    def insert_or_replace(self, values, columns=None):
        if not columns:
            columns = self.columns
        command = f"""
        INSERT OR REPLACE INTO {self.table} {columns}
        VALUES {values}
        """
        self.execute(command)

    # Update Queries
    def update_record(self, key, values, columns=None):
        if not columns:
            columns = self.columns
    
        detail = ', '.join(f"{c} = '{v}'" for c,v in zip(columns, values))
        command = f"""
        UPDATE {self.table} 
        SET {detail}
        WHERE 
        ID = {key}
        """
        return self.execute(command)

    # Misc Queries
    def query(self, command):
        self.execute(command)
