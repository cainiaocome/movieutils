#/usr/bin/env python

import shlex
import subprocess


def run(cmd):
    subprocess.run(cmd, shell=True)
