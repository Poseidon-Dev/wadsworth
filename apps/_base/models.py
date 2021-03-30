import psycopg2
from datetime import date

import core.config

class Database:

    def __init__(self):
        self.conn = core.cofig.conn()
        self.cur = self.conn.cursor()
        self.table = ''
        self.columns = tuple()

    def execute(self, command):
        print(command)
        self.cur.execute(command)
        try:
            response = self.cur.fetchall()
        except:
            response = ''
        self.conn.commit()
        return response

    # Select Queries
    def select_all(self, table=None, where=''):
        if not table:
            table = self.table
        command = f"""SELECT * FROM {table} {where}"""
        return self.execute(command)

    def select_all_columns(self, columns=None, table=None, where=''):
        if not table:
            table = self.table
        if not columns:
            columns = self.columns
            columns = str(columns).replace('(', '')
            columns = str(columns).replace(')', '')
            columns = str(columns).replace("'", '')
        command = f""" SELECT {columns} FROM {table} {where} """
        return self.execute(command)

    def select_by_id(self, table=None, key):
        if not table:
            table = self.table
        command = f"""SELECT * FROM {table} WHERE ID = {key} """
        return self.execute(command)

    def select_top_row(self, table=None, where='', order=''):
        if not table:
            table = self.table
        command = f"""SELECT * FROM {table} {where} {order}"""
        print(command)
        self.cur.execute(command)
        try:
            response = self.cur.fetchone()
        except:
            response = ''
        self.conn.commit()
        return response

    def count_records(self, where=''):
        if not table:
            table = self.table
        command = f""" SELECT COUNT (*) FROM {table} {where} """
        return self.execute(command)

    # Delete Queries
    def delete_row_by_key(self, key, table=None):
        if not table:
            table = self.table
        command = f"""DELETE FROM {table} WHERE id = {key}"""
        return self.execute(command)

    def clear_table(self, table):
        command = f"""DROP TABLE IF EXISTS {table}"""
        self.execute(command)

    # Insert Queries
    def insert_or_replace(self, values, columns=None):
        if not columns:
            columns = self.columns
        command = f"""
        INSERT INTO {self.table} {columns}
        VALUES {values}
        ON CONFLICT ON CONSTRAINT {self.table}_pkey
            DO NOTHING
        """
        self.execute(command)

    def insert_single_record(self, values):
        command = f"""
        INSERT INTO {self.table} {self.columns}
        VALUES ({values})
        ON CONFLICT ON CONSTRAINT {self.table}_pkey
            DO NOTHING
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