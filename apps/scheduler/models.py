from apps.base import Query

class SchedulerTable(Query):

    def __init__(self):
        self.table=''
        self.columns = [('',)]
        Query.__init__(self, self.table, self.columns)
