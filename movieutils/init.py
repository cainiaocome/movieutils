#!/usr/bin/env python

import shlex
import subprocess
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

mkdir -p videos
rm -rf videos/*

rm -rf aisiji
git clone https://github.com/cainiaocome/aisiji.git


mkdir -p fonts/
rm -rf fonts/*
wget https://fonts.google.com/download?family=Noto%20Sans%20SC -O noto.zip
dtrx noto.zip --one here
cp noto/* fonts/
'''
def do_init_env():
    cmds = cmds.split()
    for cmd in cmds:
        print(cmd)
        run(cmd)


import pathlib
from pprint import pprint
import tmdbsimple as tmdb
    

# videos dir
videos_dir = pathlib.Path('./videos/')


# font files
fonts_dir = pathlib.Path('fonts')
fontfile = (fonts_dir / 'NotoSansSC-Medium.otf').absolute()


# prefix and segments
video_prefix_path = pathlib.Path('./aisiji/cn_0.mp4')
video_segment_path = pathlib.Path('./aisiji/9499.mp4')

