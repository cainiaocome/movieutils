#!/usr/bin/env python

import gspread
import time
import json
import pandas as pd
from datetime import datetime
import numpy as np

gc = gspread.oauth()
sh = gc.open('rendered')
worksheets = sh.worksheets()
worksheets = [w.title for w in worksheets]

worksheet_name = f'reddit_rendered_urls'
if not worksheet_name in worksheets:
    worksheet = sh.add_worksheet(
        worksheet_name, rows=3000, cols=1000)
else:
    worksheet = sh.worksheet(worksheet_name)

def update_rendered_urls(urls):
    old = np.array(worksheet.get_all_values())
    old = set(list(old.flatten()))
    new = set(urls)
    all_urls = list(old.union(new))
    
    s = pd.Series(['' for i in range(3000*1000)])
    s[:len(all_urls)] = all_urls
    a = np.array(s)
    a = a.reshape((3000,-1))
    worksheet.update('A1', a.tolist())
    
processed_s = set()
for s in reddit.multireddit("samuraisam", "programming").top("day"):
    processed_s.add(s.id)
update_rendered_urls(processed_s)
