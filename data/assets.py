import os, sys
from datetime import date

if not os.path.isfile('config.py'):
    sys.exit("'config.py' not found. Please check your directory and try again")
else:
    import config

from data import DB

class AssetTable(DB):
    
    def __init__(self):
        super(AssetTable, self).__init__()
        self.table = 'asset_table'
        self.columns = '(id, empid, item, category, brand, model, serial, identifier, status, issuedate, returndate, backupdate, backedup)'

    def create_table(self):
        """
        Creates the asset_table in the wadsworth db
        """
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            id              INT            PRIMARY KEY,
            empid           INT            NOT NULL     REFERENCES employee_table(id) ON DELETE CASCADE,
            item            VARCHAR(50),
            category        INT            NOT NULL     REFERENCES category_table(id) ON DELETE CASCADE,
            brand           VARCHAR(50),
            model           VARCHAR(50),
            serial          VARCHAR(50),
            identifier      VARCHAR(50),
            status          INT            NOT NULL     REFERENCES status_table(id) ON DELETE CASCADE, 
            issuedate       VARCHAR(50),
            returndate      VARCHAR(50),
            backupdate      VARCHAR(50),
            backedup        BOOLEAN
        );
        """
        self.execute(command)

    def return_asset_minified(self, key):
        response = self.select_columns('category, brand, model, serial, status', 'asset_table', where=f'WHERE empid={key}')
        return response



    def run(self):
        self.create_table()