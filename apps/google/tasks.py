from math import floor
from tokenize import group
from discord.ext import commands, tasks
import os
import pandas as pd

from sqlalchemy import true

import core.config
from core.shared.utils import Timer
from apps.google.models import GoogleTable

from ecmsapi import SQLQuery
from ecmsapi.tables import PRTECN, PRTMST

class GoogleTasks(commands.Cog, name='google_tasks'):

    def __init__(self, bot):
        self.bot = bot
        self.google_task.start()
        self.channel = self.bot.get_channel(core.config.BOT_CHANNEL)
        self.group = 'testgroup'
        self.dist = [
            '00-Corp-Distribution',
            '01-Tucson-Distribution',
            '02-Phoenix-Distribution',
            '03-Hesperia-Distribution',
            '04-Corona-Distribution',
            '05-Vegas-Distribution',
            '06-Pipeline-Distribution',
            '07-Reno-Distribution',
            '08-Carson-Distribution',
            '09-Pacific-Distribution',
            '10-Bullhead-Distribution',
            '11-Inland-Distribution',
            '12-Drip-Distribution',
        ]

    @tasks.loop(hours=24.0)
    async def google_task(self):
        self.dump_active_email()
        t = Timer('Google Distribtion')
        t.start()
        self.update_groups()
        t.stop()
        return True

    def fetch_email_list(self):
        table = SQLQuery(PRTECN)
        query = table.select()
        query.columns(['EMPLOYEENO', 'EMAILADDR',])
        query.filters(companyno=1, statuscode='A')
        query.filter('EMPLOYEENO', 0, '>')
        query.filter('EMAILADDR', '', '<>')
        resp = query.to_df()
        resp['EMAILADDR'] = resp['EMAILADDR'].apply(lambda x: x.strip())
        return resp

    def fetch_active_employees(self):
        table = SQLQuery(PRTMST)
        query = table.select()
        query.columns(['EMPLOYEENO', 'STDDEPTNO'])
        query.filters(companyno=1, statuscode='A')
        resp = query.to_df()
        return resp

    def sort_active_employees(self):
        emps = self.fetch_active_employees()
        emps['STDDEPTNO'] = emps['STDDEPTNO'].apply(lambda x: int(floor(x/10)))
        return emps

    def dump_active_email(self):
        email_df = self.fetch_email_list()
        emps_df = self.sort_active_employees()
        email_list = emps_df.merge(email_df, how='left').dropna()
        div_dfs = [v for k,v in email_list.groupby('STDDEPTNO')]
        
        for div_df in div_dfs:
            division = int(div_df['STDDEPTNO'].unique())
            for dist in self.dist:
                dist_div = int(dist.split('-')[0])
                if dist_div == division:
                    pd.DataFrame.to_csv(div_df['EMAILADDR'],f'C:/Apps/wadsworth/dumps/sysout/{dist}.csv', index=False)

    def update_groups(self):
        path = 'C:/Apps/wadsworth/dumps/sysout/'
        files =[d for d in os.listdir(path) if d.split('.')[1] == 'csv']
        
        for f in files:
            group = f.split('.')[0]
            self.delete_group_members(group)
            self.add_group_members(group=group, csv=f'{path}{f}')

    def delete_group_members(self, group):
        os.system(f'GAM UPDATE GROUP {group} CLEAR')

    def add_group_members(self, group, csv):
        os.system(f'GAM CSV {csv} GAM UPDATE GROUP {group} ADD MEMBER ~EMAILADDR user')




    
