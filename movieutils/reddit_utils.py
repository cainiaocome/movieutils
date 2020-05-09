#!/usr/bin/env python

import requests
import pandas as pd

reddit_base_url = 'https://www.reddit.com'
def fill_url(url):
    return f'{reddit_base_url}{url}'

def get_top_subreddits():
    r = requests.get('https://redditmetrics.com/files/2020-05-01.csv')
    p = pathlib.Path('t.csv')
    p.write_bytes(r.content)

    df = pd.read_csv('t.csv', encoding='iso-8859-1')
    df.sort_values('subs', ascending=False, inplace=True)
    df_1m = df[df.subs>1000000]

    top_subreddits = list(df_1m.real_name)
    for s in top_subreddits:
        url = f'https://www.reddit.com/r/{s}/top/?t=week'
        print(f'{s:<20}    {url}')
    return top_subreddits
