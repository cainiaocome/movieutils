#!/usr/bin/env python

import shlex
import subprocess
from pprint import pprint
def run(cmd):
    subprocess.run(cmd, shell=True)


# libraries
cmds = '''
apt install dtrx -y
pip install tmdbsimple
pip install youtube-dl
pip install fonttools
pip install ffmpeg-python
pip install pydub
pip install praw
mkdir -p tmp

wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -O ffmpeg.tar.xz
dtrx ffmpeg.tar.xz --one here
cp ffmpeg-*-amd64-static/ffmpeg /usr/bin/ffmpeg
cp ffmpeg-*-amd64-static/ffprobe /usr/bin/ffprobe

mkdir -p videos
mkdir -p subs
mkdir -p autosubs
mkdir -p bestsubs

rm -rf aisiji
git clone https://github.com/cainiaocome/aisiji.git

mkdir -p fonts/
wget https://fonts.google.com/download?family=Noto%20Sans%20SC -O noto.zip
dtrx noto.zip --one here
cp noto/*.otf fonts/

git clone https://github.com/cainiaocome/movieutils.git
'''

cmds = cmds.splitlines()
for cmd in cmds:
    print(cmd)
    run(cmd)
