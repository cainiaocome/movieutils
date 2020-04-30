#!/usr/bin/env python

import os
import time
import json
import base64
import pathlib
import hashlib
import requests
import queue
import uuid
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor

try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    print('urllib3 disable_warnings except')


def upload(inputfile, saddr, password, crt='client.crt', key='client.key'):
    def job_executor(job):
        s = requests.session()
        s.cert = (crt, key)
        while True:
            try:
                r = s.post(saddr, json=job, timeout=7, verify=False)
                r = r.json()
                if r['status'] == True:
                    break
            except:
                traceback.print_exc()

    job_id = str(uuid.uuid4())
    p = pathlib.Path(inputfile)
    outputfile = p.name
    p = p.read_bytes()
    md5 = hashlib.md5(p).hexdigest()
    chunks = [p[i:i+4096] for i in range(0, len(p), 4096)]
    print(f'{inputfile} len of chunks:', len(chunks))
    jobs = []
    for index, chunk in enumerate(chunks):
        job = {
            'job_id': job_id,
            'password': password,
            'md5':md5,
            'filepath':outputfile,
            'index':index,
            'index_count':len(chunks),
            'this_content':base64.b64encode(chunk).decode('ascii'),
        }
        jobs.append(job)
    with ThreadPoolExecutor(32) as pool:
        r = list(pool.map(job_executor, jobs))
    
if __name__=='__main__':
    import fire
    fire.Fire(upload)
