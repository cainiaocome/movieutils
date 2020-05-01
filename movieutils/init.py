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
pip install ffmpeg-python
pip install pydub
mkdir -p tmp

wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz -O ffmpeg.tar.xz
dtrx ffmpeg.tar.xz --one here
cp ffmpeg-*-amd64-static/ffmpeg /usr/bin/ffmpeg
cp ffmpeg-*-amd64-static/ffprobe /usr/bin/ffprobe

wget https://github.com/timvisee/ffsend/releases/download/v0.2.59/ffsend-v0.2.59-linux-x64-static -O ffsend
chmod a+x ./ffsend
mv ./ffsend /usr/local/bin/

mkdir -p videos
rm -rf videos/*

mkdir -p subs
rm -rf subs/*

mkdir -p autosubs
rm -rf autosubs/*

rm -rf aisiji
git clone https://github.com/cainiaocome/aisiji.git

mkdir -p fonts/
rm -rf fonts/*
wget https://fonts.google.com/download?family=Noto%20Sans%20SC -O noto.zip
dtrx noto.zip --one here
cp noto/* fonts/

git clone https://github.com/cainiaocome/movieutils.git
'''

cmds = cmds.splitlines()
for cmd in cmds:
    print(cmd)
    run(cmd)
