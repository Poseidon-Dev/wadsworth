from apps.base import Query

class TicketTable(Query):

    def __init__(self):
        self.table = 'ticket_table'
        self.columns = [
            ('id', 'INT PRIMARY KEY'),
            ('tech', 'VARCHAR(100)'),
            ('submitter', 'VARCHAR(100)'),
            ('subject', 'VARCHAR'),
            ('status', 'VARCHAR(100)'),
            ('body', 'TEXT'),
        ]
        Query.__init__(self, self.table, self.columns)

class TicketCommentTable(Query):

    def __init__(self):
        self.table = 'ticket_comments'
        self.columns = [
            ('id', 'INT PRIMARY KEY'),
            ('ticket_id', 'INT REFERENCES ticket_table(ID) ON DELETE CASCADE'),
            ('ticket_user', 'VARCHAR(100)'),
            ('type', 'BOOLEAN'),
            ('body', 'TEXT'),
        ]
        Query.__init__(self, self.table, self.columns)

    
