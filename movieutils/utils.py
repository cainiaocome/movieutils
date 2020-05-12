#/usr/bin/env python

import pathlib
import shutil
import shlex
import subprocess
import time
import uuid
import validators
from datetime import datetime


def run(cmd):
    subprocess.run(cmd, shell=True)

def rmdir(d):
    shutil.rmtree(d, ignore_errors=True) 

notebook_start_time = time.time()
def no_much_time_left():
    return time.time()-notebook_start_time>7*3600

def iter_object_find_url(o):
    if type(o) is str and validators.url(o):
        yield o
    elif type(o) is dict:
        for k,v in o.items():
            for r in iter_object(v):
                yield r
    elif type(o) is list:
        for i in o:
            for r in iter_object(i):
                yield r
    else:
        yield None

today = f'{datetime.now().date()}'
run_session_id = str(uuid.uuid4())
