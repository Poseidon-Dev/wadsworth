from apps.base import Query
from datetime import datetime

from core import config

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
            ('status', 'BOOLEAN'),
            ('creator', 'VARCHAR')
            ]
        Query.__init__(self, self.table, self.columns)

class SchedulerUserTable(Query):
    def __init__(self):
        self.table='scheulder_user_table'
        self.columns = [
            ('id', 'SERIAL PRIMARY KEY'),
            ('schedule_id', 'INT REFERENCES scheduler_table(id) ON DELETE NO ACTION'),
            ('participant_id', 'VARCHAR'),
            ('status', 'BOOLEAN'),
            ]
        Query.__init__(self, self.table, self.columns)

class Participant:
    def __init__(self, participant_id):
        self.participant_id = participant_id
        self._my_events = None

    @property
    def my_events(self):
        self._my_events = SchedulerUserTable().filter('participant_id', self.participant_id).query()
        return self._my_events

    def __str__(self):
        return f'{self.participant_id}'

class ScheduleCalender:
    def __init__(self):
        self._current_events = None
        self._closed_events = None
    
    @property
    def current_events(self):
        self._current_events = SchedulerTable().filter('status', 'True').query()
        return self._current_events

    @property
    def closed_events(self):
        self._closed_events = SchedulerTable().filter('status', 'False').query()
        return self._closed_events

    @staticmethod
    def create_event(channel, title, body, date, creator, type='Task', status='True'):
        print('made it here')
        SchedulerTable().insert([
            ('channel_id', channel),
            ('type', type),
            ('title', title),
            ('body', body),
            ('status', status),
            ('datetime', date),
            ('creator', creator)
        ])
        print('should have inserted')
        
class Schedule:
    def __init__(self, id):
        self.id = id
        self.schedule = SchedulerTable().filter('id', self.id).query()[0]
        self.channel_id = self.schedule[1]
        self.message_id = self.schedule[2]
        self.type = self.schedule[3]
        self.body = self.schedule[4]
        self.date = self.schedule[5]
        self.status = self.schedule[6]
        self._participants = None
        self._accepted_participants = None
        self._declined_participants = None
        self._unanswered_participants = None
        self._channel = None

    @property
    def channel(self):
        self._channel = config.BOT.get_channel(self.channel_id)
        return self._channel

    @property
    def participants(self):
        self._participants = [
            Participant(participant_id) 
            for participant_id in SchedulerUserTable().filter('schedule_id', self.id).query()]
        return self._participants

    @property
    def accepted_participants(self):
        participants = [participant for participant in self.participants]
        return participants

    @property
    def declined_participants(self):
        return [participant for participant in self.participants() if participant[3] == False ]

    @property
    def unanswered_participants(self):
        return [participant for participant in self.participants() if participant[3] == None ]
    