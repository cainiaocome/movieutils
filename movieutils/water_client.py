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
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    print('urllib3 disable_warnings except')

def download_and_upload(url):
    for try_index in range(3):
        try:
            r = requests.get(url)
            r.raise_for_status()
            filename = pathlib.Path(urlparse(url).path).name
            filepath = pathlib.Path(filename)
            print(f'download finished {filepath}')
            filepath.write_bytes(r.content)
            simple_water_upload(filepath)
            print(f'upload finished {filepath}')
            return
        except:
            pass

def simple_water_upload(filepath):
    water_saddr = 'https://jlzduck.duckdns.org:1314/file'
    upload(filepath, water_saddr)


def simple_water_upload_and_delete(filepath):
    simple_water_upload(filepath)
    p = pathlib.Path(filepath)
    p.unlink()


def upload(inputfile, saddr):
    password = os.environ['water_password']
    def job_executor(job):
        while True:
            try:
                s = requests.session()
                r = s.post(saddr, json=job, timeout=7, verify=False)
                r = r.json()
                if r['status'] == True:
                    break
            except:
                pass
                #traceback.print_exc()

    job_id = str(uuid.uuid4())
    p = pathlib.Path(inputfile)
    outputfile = p.name
    p = p.read_bytes()
    md5 = hashlib.md5(p).hexdigest()
    chunk_len = 2**10*32
    chunks = [p[i:i+chunk_len] for i in range(0, len(p), chunk_len)]
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
