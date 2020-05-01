#!/usr/bin/env python

import glob
import shlex
import subprocess
import pathlib

# 如果链接失效怎么处理
# 也许把youtube-dl作为库来用可以解决
def download(key):
    base_url = 'https://www.youtube.com/watch?v='
    url = f'{base_url}{key}'
    cmds = [
        f'youtube-dl --no-part --output ./videos/{key}.%(ext)s {url}',
        f'youtube-dl --no-part --skip-download --all-subs --convert-subs ass --output ./subs/{key}.%(ext)s {url}',
        f'youtube-dl --no-part --skip-download --write-auto-sub --all-subs --convert-subs ass --output ./autosubs/{key}.%(ext)s {url}',
    ]
    for cmd in cmds:
        print(cmd)
        subprocess.run(cmd, shell=True)
    

def load_key_sub_dict(language):
    sub_l = glob.glob(f'subs/*.{language}.ass')
    key_l = [f.name.split('.')[0] for f in sub_l]
    return dict(zip(key_l, sub_l))


def load_key_autosub_dict(language):
    sub_l = glob.glob(f'autosubs/*.{language}.ass')
    key_l = [f.name.split('.')[0] for f in sub_l]
    return dict(zip(key_l, sub_l))

def get_best_subtitle(key, language):
    key_sub_dict = load_key_sub_dict(language)
    key_autosub_dict = load_key_autosub_dict(language)
    sub = key_sub_dict.get(key, None)
    if sub:
        return sub
    autosub = key_autosub_dict.get(key, None)
    if autosub:
        return autosub
    return None

def get_best_subtitle_or_en(key, language):
    sub = get_best_subtitle(key, language)
    if sub:
        return sub
    # default: english subtitle
    return get_best_subtitle(key, 'en')


def load_key_video_dict():
    video_dir = pathlib.Path('videos')
    video_l = list(video_dir.iterdir())
    video_key = [f.stem for f in video_l]
    return dict(zip(video_key, video_l))
