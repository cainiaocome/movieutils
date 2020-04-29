#/usr/bin/env python

import shutil
import shlex
import subprocess


def run(cmd):
    subprocess.run(cmd, shell=True)

def rmdir(d):
    shutil.rmtree(d, ignore_errors=True) 

def ffsend(filepath):
    import shlex
    import subprocess
    import time
    ffsend_basic_auth = 'cainiaocome@gmail.com:t/b+8nESha_#dG*'
    cmd = f'ffsend upload --no-interact --expiry-time 1d {filepath}'.split()
    while True:
        try:
            output = subprocess.check_output(cmd)
            url = output.decode('utf8').strip()
            return url
        except:
            print(f'ffsend upload {filepath} failed')
            time.sleep(30)
