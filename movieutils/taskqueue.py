#!/usr/bin/env python

import gspread
import time
import json
import base64
import pandas as pd
from datetime import datetime

gc = gspread.oauth()
sh = gc.open('tasks sync')
worksheets = sh.worksheets()
worksheets = [w.title for w in worksheets]

now = datetime.now()
current_year = now.year
current_week = pd.to_datetime(now).weekofyear

def week_to_col(week):
    a1 = gspread.utils.rowcol_to_a1(1, week)    
    col = a1[:-1]
    return col

class TaskQueueManager:
    def __init__(self, tasktype):
        assert tasktype in ['reddit', 'movie']
        self.tasktype = tasktype
        self.worksheet_name = f'{tasktype}_{current_year}'
        if not self.worksheet_name in worksheets:
            self.worksheet = sh.add_worksheet(
                self.worksheet_name, rows=3000, cols=100)
        else:
            self.worksheet = sh.worksheet(self.worksheet_name)

    def set_week_tasks(self, week, tasks):
        col = week_to_col(week)
        tasks = [[json.dumps(task)] for task in tasks]
        self.worksheet.update(f'{col}:{col}', tasks)

    def get_week_tasks(self, week):
        tasks = self.worksheet.col_values(week)
        return [json.loads(task) for task in tasks]

    def set_current_week_tasks(self, tasks):
        self.set_week_tasks(current_week, tasks)

    def get_current_week_tasks(self):
        return self.get_week_tasks(current_week)

    def get_one_task(self):
        tasks = self.get_current_week_tasks()
        for i,task in enumerate(tasks):
            if task:
                break
        tasks[i] = ''
        self.set_current_week_tasks(tasks)
        return task

if __name__ == '__main__':
    tasks = ['s1', 's2', 's3']
    reddit_taskmanager = TaskQueueManager('reddit')
    reddit_taskmanager.set_current_week_tasks(tasks)
    while True:
        task = reddit_taskmanager.get_one_task()
        if not task:
            break
        print(task)
        time.sleep(3)
