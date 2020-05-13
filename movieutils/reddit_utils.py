#!/usr/bin/env python

import uuid
import pathlib
import ffmpeg
import requests
import numpy as np
import pandas as pd
from PIL import Image
from .wordcloud_utils import simple_make_wordcloud

reddit_base_url = 'https://www.reddit.com'


def fill_url(url):
    return f'{reddit_base_url}{url}'


def get_top_subreddits():
    r = requests.get('https://redditmetrics.com/files/2020-05-01.csv')
    p = pathlib.Path('t.csv')
    p.write_bytes(r.content)

    df = pd.read_csv('t.csv', encoding='iso-8859-1')
    df.sort_values('subs', ascending=False, inplace=True)
    df_1m = df[df.subs > 1000000]

    top_subreddits = list(df_1m.real_name)
    for s in top_subreddits:
        url = f'https://www.reddit.com/r/{s}/top/?t=week'
        print(f'{s:<30}    {url}')
    return top_subreddits


def group_videos(videos, max_duration=180, max_videos=7):
    i = 0
    while i < len(videos):
        start = i
        addup_duration = 0
        while addup_duration < 180 and i < len(videos):
            video = videos[i]
            probe_result = ffmpeg.probe(video)
            duration = float(probe_result['format']['duration'])
            addup_duration += duration
            i += 1
        end = i
        yield start, end


def scale_to_1080p(video):
    stream_0 = ffmpeg.probe(video)['streams'][0]  # stream 0 must be video
    width, height = stream_0['width'], stream_0['height']
    for factor in np.arange(0, 4, 0.001):
        if width*factor >= 1920 or height*factor >= 1080:
            break
    factor = factor - 0.001
    return int(width*factor), int(height*factor)


def make_bg(bg_text, bg_file):
    make_black_bg(bg_file)  # disable wordcloud background for now
    return

    p = pathlib.Path(bg_file)
    if p.exists():
        p.unlink()
    simple_make_wordcloud(bg_text, p)

def make_black_bg(bg_file):
    img = Image.new('RGB', (1920,1080), (0,0,0))
    img.save(bg_file)
         
def copy_bg(bg_file):
    bg_file = pathlib.Path(bg_file)
    bg_file_data = bg_file.read_bytes()
    copied_bg_file = pathlib.Path(f'/tmp/{uuid.uuid4()}{bg_file.suffix}')
    copied_bg_file.write_bytes(bg_file_data)
    return copied_bg_file
