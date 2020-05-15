#!/usr/bin/env python

import sys
import gspread
import time
import json
import base64
import numpy as np
import pandas as pd
from itertools import product
from datetime import datetime

gc = gspread.oauth()
sh = gc.open('tasks sync')

time_filter_timedelta_map = {
    'week': pd.to_timedelta('7 days'),
    'month': pd.to_timedelta('30 days'),
    'year': pd.to_timedelta('365 days'),
}

rows = 300
cols = 100
epoch_init_time = datetime(1970,1,1)
class TaskQueueManager:
    def __init__(self, tasktype):
        assert tasktype in ['reddit', 'movie', 'test']
        self.tasktype = tasktype
        self.worksheet_name = f'{tasktype}'

        worksheets = sh.worksheets()
        worksheets = [w.title for w in worksheets]
    
        if not self.worksheet_name in worksheets:
            self.create_worksheet()
        else:
            self.worksheet = sh.worksheet(self.worksheet_name)

    def create_worksheet(self):
        self.worksheet = sh.add_worksheet(
            self.worksheet_name, rows=rows, cols=cols)

    def recreate_worksheet(self):
        sh.del_worksheet(self.worksheet)
        self.create_worksheet()
        
    def reset_tasks(self, names):
        time_filters = time_filter_timedelta_map.keys()
        tasks = []
        for name,time_filter in product(names, time_filters):
            tasks.append({'name':name, 'time_filter':time_filter, 'last':epoch_init_time})
        tasks = pd.DataFrame(tasks)
        self.recreate_worksheet()
        self.set_all(tasks)
        return tasks

    def set_all(self, tasks):
        for col in tasks.columns:
            tasks[col] = tasks[col].astype('str')
        self.worksheet.update([tasks.columns.values.tolist()] + tasks.values.tolist()) 

    def get_all(self):
        tasks = pd.DataFrame(self.worksheet.get_all_records())
        tasks['last'] = pd.to_datetime(tasks['last'])
        return tasks

    def get_one(self, time_filter):
        now = datetime.now()
        tasks = self.get_all()
        tasks = tasks[tasks.time_filter==time_filter]
        required_timedelta = time_filter_timedelta_map[time_filter]
        tasks = tasks[(now-tasks['last'])>required_timedelta]
        if tasks.shape[0]==0:
            return None
        return list(tasks.name)[0]

    def set_one(self, name, time_filter):
        tasks = self.get_all()
        now = datetime.now()
        row = tasks[(tasks.name==name)&(tasks.time_filter==time_filter)]['last']
        tasks.loc[row.index, 'last'] = pd.to_datetime(now)
        self.set_all(tasks)
        
if __name__ == '__main__':
    names = ['s1', 's2', 's3']

    reddit_taskmanager = TaskQueueManager('test')
    df = reddit_taskmanager.reset_tasks(names)

    df = reddit_taskmanager.get_all()
    print(df)
    print('-'*30)

    reddit_taskmanager.set_one('s1', 'month')
    reddit_taskmanager.set_one('s2', 'month')

    x = reddit_taskmanager.get_one('month')
    print(x)
    print('-'*30)

    reddit_taskmanager.set_one(x, 'month')

    x = reddit_taskmanager.get_one('month')
    print(x)
    print('-'*30)

    sys.exit(0)
    while True:
        task = reddit_taskmanager.get_one_task()
        if not task:
            break
        print(task)
        time.sleep(3)
