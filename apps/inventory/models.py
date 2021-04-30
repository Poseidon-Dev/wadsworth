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

    def run(self):
        self.create_table()
    
