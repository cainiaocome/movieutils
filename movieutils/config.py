
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
video_segment_path = pathlib.Path('./aisiji/cn_1.mp4')

