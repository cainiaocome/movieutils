#/usr/bin/env python

import pathlib
import requests
import shutil
import shlex
import subprocess
import time
import uuid
import validators
import tempfile
from datetime import datetime


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

def add_prefix_and_segments_to_inputs(inputs):
    from config import video_prefix_path, video_segment_path
    r = [video_prefix_path]
    for i in inputs:
        r.append(i)
        r.append(video_segment_path)
    r.append(video_prefix_path)
    return r

today = f'{datetime.now().date()}'
run_session_id = str(uuid.uuid4())
