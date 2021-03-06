#/usr/bin/env python

import json
import pathlib
import requests
import shutil
import shlex
import subprocess
import time
import uuid
import validators
import tempfile
import pandas as pd
from datetime import datetime

now = datetime.now()
current_year = now.year
current_month = now.month
current_week = pd.to_datetime(now).weekofyear

today = f'{datetime.now().date()}'
run_session_id = str(uuid.uuid4())

def run(cmd):
    subprocess.run(cmd, shell=True)

def rmdir(d):
    shutil.rmtree(d, ignore_errors=True) 

notebook_start_time = time.time()
def no_much_time_left():
    return time.time()-notebook_start_time>7*3600

import validators
def iter_object_find_urls(o):
    def do_iter_object(o):
        if type(o) is str and validators.url(o):
            yield o
        elif type(o) is dict:
            for k,v in o.items():
                for r in iter_object_find_urls(v):
                    yield r
        elif type(o) is list:
            for i in o:
                for r in iter_object_find_urls(i):
                    yield r
        else:
            yield None
    all_urls = list(do_iter_object(o))
    return list(filter(lambda x:x, all_urls))

def safe_get_with_timeout(url, timeout=7):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r
    except:
        return requests.Response()

def new_temp_file(suffix):
    tempdir = pathlib.Path(tempfile.gettempdir())
    return tempdir / f'{uuid.uuid4()}{suffix}'

def copy_file(filepath):
    filepath = pathlib.Path(filepath)
    filedata = filepath.read_bytes()
    copied_file = new_temp_file(filepath.suffix)
    copied_file.write_bytes(filedata)
    return copied_file

def add_prefix_and_segments_to_inputs(inputs):
    from .config import video_prefix_path, video_segment_path
    r = [copy_file(video_prefix_path)]
    for i in inputs:
        r.append(i)
        r.append(copy_file(video_segment_path))
    r.append(copy_file(video_prefix_path))
    return r

def load_file_lines(filepath):
    p = pathlib.Path(filepath)
    s = p.read_text()
    lines = s.splitlines()
    lines = [line.strip() for line in lines]
    return list(filter(lambda line:line, lines))

def load_json(filepath):
    p = pathlib.Path(filepath)
    s = p.read_text()
    return json.loads(s)

def dump_json(data, filepath):
    p = pathlib.Path(filepath)
    p.write_text(json.dumps(data))
