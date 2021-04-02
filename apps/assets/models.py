from apps.base import Database

class AssetTable(Database):
    
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

class CategoryTable(Database):

    def __init__(self):
        super(CategoryTable, self).__init__()
        self.table = 'category_table'
        self.columns = '(id, category)'
        self.key = 'category'

    def create_table(self):
        """
        Creates the category_table in the wadsworth db
        """
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            id              INT               PRIMARY KEY,
            category        VARCHAR(30)
        );
        """
        self.execute(command)

    def run(self):
        self.create_table()
        self.insert_single_record("1, 'iphone'")
        self.insert_single_record("2, 'ipad'")
        self.insert_single_record("3, 'Laptop'")
        self.insert_single_record("4, 'Desktop'")
        self.insert_single_record("5, 'Misc Device'")
        self.insert_single_record("6, 'Email'")
        self.insert_single_record("7, 'Software'")


class StatusTable(Database):
    def __init__(self):
        super(StatusTable, self).__init__()
        self.table = 'status_table'
        self.columns = '(id, status)'
        self.key = 'status'

    def create_table(self):
        """
        Creates the status_table in the wadsworth db
        """
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            id              INT               PRIMARY KEY,
            status          VARCHAR(30)
        );
        """
        self.execute(command)

    def run(self):
        self.create_table()
        self.insert_single_record("1, 'Active'")
        self.insert_single_record("2, 'Inactive'")
        self.insert_single_record("3, 'Broken'")
        self.insert_single_record("4, 'Returned'")
