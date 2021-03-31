from apps.base import Database

class TicketTable(Database):
    """
    Retrieves ticket data from JitBit API for a local store
    """
    
    def __init__(self):
        super(TicketTable, self).__init__()
        self.columns = '(tech, submitter, subject, status, body)'
        self.table = 'ticket_table'

    def create_table(self):
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            id                  INT             PRIMARY KEY,
            tech                VARCHAR(100),
            submitter           VARCHAR(100),
            subject             VARCHAR(256),
            status              VARCHAR(30),
            body                TEXT
        );
        """
        self.execute(command)

    def run(self):
        if not self.check_table_exists():
            self.create_table()


class TicketCommentTable(Database):

    def __init__(self):
        super(TicketCommentTable, self).__init__()
        self.columns = ('ticket_id','user','type','body')
        self.table = 'ticket_comments'

    def create_table(self):
        command = f"""
        CREATE TABLE IF NOT EXISTS
        {self.table}(
            id                 INT             PRIMARY KEY,
            ticket_id          INT,
            ticket_user        VARCHAR(100),
            type               BOOLEAN,
            body               TEXT,
            CONSTRAINT fk_ticket_table
                FOREIGN KEY(ticket_id) 
                REFERENCES ticket_table(ID)
                ON DELETE CASCADE
        );
        """
        self.execute(command)

    def run(self):
        if not self.check_table_exists():
            self.create_table()