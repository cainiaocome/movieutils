#!/usr/bin/env python

from .config import videos_dir, video_prefix_path, video_segment_path, fontfile

def concat(video_inputs, text_l, output_file):
    '''
    video_inputs: video file path list
    text_l: subtitle list for each video
    '''
    import pathlib
    import shlex
    import ffmpeg
    from pprint import pprint

    duration = 35
    n = len(video_inputs)

    # prefix
    video_prefix = ffmpeg.input(video_prefix_path)
    in_file_l = [video_prefix.video, video_prefix.audio]
    
    # segments
    for f,subtitle in zip(video_inputs, text_l):
        in_file = ffmpeg.input(f)
        in_file_l.append(in_file.video
                         .filter('scale', width=1920, height=-2)
                         .filter('pad', width=1920, height=1080, x='(ow-iw)/2', y='(oh-ih)/2')
                         .filter('trim', duration=duration)
                         .drawtext(subtitle, fontfile=str(fontfile), fontsize=32, fontcolor='LightGrey'))
        in_file_l.append(in_file.audio.filter('atrim', duration=duration))
        
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
    import ffmpeg
    import subprocess
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
