#/usr/bin/env python

import pathlib
import shutil
import shlex
import subprocess
import time
from datetime import datetime


def run(cmd):
    subprocess.run(cmd, shell=True)

def rmdir(d):
    shutil.rmtree(d, ignore_errors=True) 

ffsend_urls = []
def ffsend(filepath):
    cmd = f'ffsend upload --no-interact --expiry-time 1d {filepath}'.split()
    while True:
        try:
            output = subprocess.check_output(cmd)
            url = output.decode('utf8').strip()
            ffsend_urls.append(url)
            return url
        except:
            print(f'ffsend upload {filepath} failed')
            time.sleep(30)

def ffsend_and_delete(filepath):
    fp = str(filepath)
    url = ffsend(filepath)
    p = pathlib.Path(filepath)
    p.unlink()
    return url

today = f'{datetime.now().date()}'
