#!/usr/bin/env python

import shlex
import pydub
import shutil
import tempfile
import pathlib
import ffmpeg
import subprocess

from pydub import AudioSegment
from .config import videos_dir, video_prefix_path, video_segment_path, fontfile

def concat(video_inputs, text_l, output_file):
    '''
    video_inputs: video file path list
    text_l: subtitle list for each video
    '''

    duration = 35
    n = len(video_inputs)

    # prefix
    video_prefix = ffmpeg.input(video_prefix_path)
    in_file_l = [video_prefix.video, video_prefix.audio]
    
    # segments
    for f,subtitle in zip(video_inputs, text_l):
        after_trim_start, after_trim_end = trim_head_and_tail_silence(f)
        in_file = ffmpeg.input(f)
        in_file_l.append(in_file.video
                         .filter('scale', width=1920, height=-2)
                         .filter('pad', width=1920, height=1080, x='(ow-iw)/2', y='(oh-ih)/2')
                         .filter('trim', start=after_trim_start, end=after_trim_end) 
                         .drawtext(subtitle, fontfile=str(fontfile), fontsize=32, fontcolor='LightGrey'))
        in_file_l.append(in_file.audio.filter('atrim', start=after_trim_start, end=after_trim_end))
        
        video_segment = ffmpeg.input(video_segment_path)
        in_file_l += [video_segment.video, video_segment.audio]

    # suffix
    video_suffix = ffmpeg.input(video_prefix_path)
    in_file_l += [video_suffix.video, video_suffix.audio]
    
    cmd = (
        ffmpeg
        .concat(*in_file_l, n=n, v=1, a=1)
        .output(output_file)
        .overwrite_output()
        .compile()
    )
    cmd = cmd[0:1] + '-hide_banner -analyzeduration 2147483647 -probesize 2147483647'.split() + cmd[1:]

    cmd = [f'{i}' for i in cmd]
    print(' '.join([shlex.quote(i) for i in cmd]))
    cmd = ' '.join([shlex.quote(i) for i in cmd])
    return cmd

def video_to_audio(video_input, audio_output):
    cmd = (
        ffmpeg
        .input(video_input)
        .audio
        .output(audio_output)
        .overwrite_output()
        .compile()
    )
    cmd = [f'{i}' for i in cmd]
    subprocess.run(cmd)

def trim_video(video_input, start, end, video_output):
    in_file = ffmpeg.input(video_input)
    in_file_l = [
        in_file.video.filter('trim', start=start, end=end),
        in_file.audio.filter('atrim', start=start, end=end),
    ]

    cmd = (
        ffmpeg
        .concat(*in_file_l, v=1, a=1)
        .output(video_output)
        .overwrite_output()
        .compile()
    )
    cmd = [f'{i}' for i in cmd]
    subprocess.run(cmd)
    
def trim_head_and_tail_silence(video_input):
    silence_thresh = -50
    tmpdir = pathlib.Path(tempfile.gettempdir())

    # tmp audio
    tmp_audio = tmpdir / 'tmpaudio.aac'
    # video to audio
    video_to_audio(str(video_input), str(tmp_audio))

    audio = AudioSegment.from_file(tmp_audio)
    duration = audio.duration_seconds # float in seconds

    silence_l = pydub.silence.detect_silence(audio, silence_thresh=silence_thresh)
    # head
    head_silence = list(filter(lambda x:x[0]<2, silence_l))
    if head_silence:
        head_silence = head_silence[0]
        start, end = head_silence
        start = start / 1000
        end = end / 1000
        end = min(end, 11)
        start, end = end, duration-(end-start)
    else:
        start, end = 0, duration
    # trim head

    # max 6 minutes
    end = min(end, start+360)
    return start, end
    #trim_video(str(tmp_video), start, end, str(video_output))
    # tail todo

