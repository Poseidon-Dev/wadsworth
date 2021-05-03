from apps.base import Database

class InventoryTable(Database):

    def __init__(self):
        super(InventoryTable, self).__init__()
        self.table = 'inventory_table'
        self.columns = '(id, division, desktops, laptops, monitors, auxilery, phones, ipads)'

    def create_table(self):
        """
        Creates the inventory_table in the wadsworth db
        """
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            id              SERIAL            PRIMARY KEY,
            division        VARCHAR(50),
            desktops        INT,
            laptops         INT,
            monitors        INT,
            auxilery        INT,
            phones          INT,
            ipads           INT
        );
        """
        self.execute(command)

    def update_record(self, key, column, mode):
        where = f'WHERE id = {key}'
        count = self.select_columns(columns=column, where=where)[0][0]
        if mode == 'add':
            count += 1
        elif mode == 'remove' and count:
            if count > 0:
                count -= 1        
        command = f"""
        UPDATE {self.table} set {column} = {count}
        {where}
        """
        self.execute(command)
        

    def run(self):
        self.create_table()
    
