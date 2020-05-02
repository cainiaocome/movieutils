#!/usr/bin/env python

import io
import urllib3
import json
import time
import pickle
import traceback
import pathlib
import hashlib
import uuid
from concurrent.futures import ThreadPoolExecutor
from minio import Minio
from minio.error import ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists

urllib3.disable_warnings()

httpClient = urllib3.PoolManager(
    timeout=urllib3.Timeout.DEFAULT_TIMEOUT,
    cert_reqs='CERT_NONE',
    retries=urllib3.Retry(
        total=5,
        backoff_factor=0.2,
        status_forcelist=[500, 502, 503, 504]
    ),
)


class MyMinio():
    def __init__(self, access_key, secret_key):
        self.minioClient = Minio('jlzduck.duckdns.org:9000',
                            access_key=access_key,
                            secret_key=secret_key,
                            secure=True,
                            http_client=httpClient
                            )
        self.upload_bucket = 'upload'


    def upload_chunk(self, chunk):
        minioClient = self.minioClient
        filename = chunk['filename']
        index = chunk['index']
        s = pickle.dumps(chunk)
        while True:
            try:
                etag = minioClient.put_object(
                    self.upload_bucket,
                    f'{filename}/{index}',
                    io.BytesIO(s),
                    len(s),
                    part_size=2**30,
                )
            except:
                traceback.print_exc()
                time.sleep(1)


    def upload(self, filepath):
        filepath = pathlib.Path(filepath)
        p = filepath.read_bytes()
        md5 = hashlib.md5(p).hexdigest()
        chunk_len = 2**10*32 # 32KB
        chunks = [p[i:i+chunk_len] for i in range(0, len(p), chunk_len)]
        jobs = []
        for index, chunk in enumerate(chunks):
            job = {
                'md5':md5,
                'filename':filepath.name,
                'index':index,
                'index_count':len(chunks),
                'chunk':chunk,
            }
            jobs.append(job)
        with ThreadPoolExecutor(32) as pool:
            r = list(pool.map(self.upload_chunk, jobs))


    def upload_and_delete(self, filepath):
        self.upload(filepath)
        filepath = pathlib.Path(filepath)
        filepath.unlink()


    def download(self):
        minioClient = self.minioClient
        try:
            http_resp = minioClient.get_object(
                'maylogs',
                'pumaserver_debug.log',
            )
            returned_data = http_resp.read()
            print(returned_data)
        except ResponseError as err:
            print(err)
        except:
            print('unkown err')
