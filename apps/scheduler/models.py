from apps.base import Query

class SchedulerTable(Query):
    def __init__(self):
        self.table='scheduler_table'
        self.columns = [
            ('id', 'SERIAL PRIMARY KEY'),
            ('channel_id', 'BIGINT'),
            ('message_id', 'BIGINT'),
            ('type', 'VARCHAR'),
            ('title', 'VARCHAR'),
            ('body', 'VARCHAR'),
            ('datetime', 'VARCHAR'),
            ]
        Query.__init__(self, self.table, self.columns)

class SchedulerUserTable(Query):
    def __init__(self):
        self.table='scheulder_user_table'
        self.columns = [
            ('id', 'SERIAL PRIMARY KEY'),
            ('schedule_id', 'INT REFERENCES scheduler_table(id) ON DELETE NO ACTION'),
            ('username', 'VARCHAR'),
            ('status', 'INT'),
            ]
        Query.__init__(self, self.table, self.columns)
