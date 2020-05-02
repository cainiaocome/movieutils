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
from urllib3.util.timeout import Timeout
from concurrent.futures import ThreadPoolExecutor
from minio import Minio
from minio.error import ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists

urllib3.disable_warnings()


class MyMinio():
    def __init__(self, access_key, secret_key):
        self.access_key = access_key
        self.secret_key = secret_key
        self.upload_bucket = 'upload'

    def get_client(self):
        httpClient = urllib3.PoolManager(
            timeout=Timeout(7),
            cert_reqs='CERT_NONE',
            maxsize=64,
        )
        minioClient = Minio('jlzduck.duckdns.org:9000',
                            access_key=self.access_key,
                            secret_key=self.secret_key,
                            secure=True,
                            http_client=httpClient
                            )
        return minioClient
        

    def upload_chunk(self, chunk):
        minioClient = self.get_client()
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
                break
            except:
                traceback.print_exc()


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
