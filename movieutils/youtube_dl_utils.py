#!/usr/bin/env python


import shlex
import subprocess
import pathlib


# 如果链接失效怎么处理
# 也许把youtube-dl作为库来用可以解决
def download(key):
    base_url = 'https://www.youtube.com/watch?v='
    url = f'{base_url}{key}'
    cmd = f'youtube-dl --output ./videos/{key}.%(ext)s {url}'
    cmd = shlex.split(cmd)
    print(cmd)
    subprocess.run(cmd)
    

def load_key_video_dict():
    video_dir = pathlib.Path('videos')
    video_l = list(video_dir.iterdir())
    video_key = [f.stem for f in video_l]
    return dict(zip(video_key, video_l))
