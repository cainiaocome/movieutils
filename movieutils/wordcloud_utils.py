#!/usr/bin/env python

import sys
import glob
import pathlib
import subprocess
import random
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from fontTools.ttLib import TTFont


colormaps = '''Accent, Accent_r, Blues, Blues_r, BrBG, BrBG_r, BuGn, BuGn_r, BuPu, BuPu_r, CMRmap, CMRmap_r, Dark2, Dark2_r, GnBu, GnBu_r, Greens, Greens_r, Greys, Greys_r, OrRd, OrRd_r, Oranges, Oranges_r, PRGn, PRGn_r, Paired, Paired_r, Pastel1, Pastel1_r, Pastel2, Pastel2_r, PiYG, PiYG_r, PuBu, PuBuGn, PuBuGn_r, PuBu_r, PuOr, PuOr_r, PuRd, PuRd_r, Purples, Purples_r, RdBu, RdBu_r, RdGy, RdGy_r, RdPu, RdPu_r, RdYlBu, RdYlBu_r, RdYlGn, RdYlGn_r, Reds, Reds_r, Set1, Set1_r, Set2, Set2_r, Set3, Set3_r, Spectral, Spectral_r, Wistia, Wistia_r, YlGn, YlGnBu, YlGnBu_r, YlGn_r, YlOrBr, YlOrBr_r, YlOrRd, YlOrRd_r, afmhot, afmhot_r, autumn, autumn_r, binary, binary_r, bone, bone_r, brg, brg_r, bwr, bwr_r, cividis, cividis_r, cool, cool_r, coolwarm, coolwarm_r, copper, copper_r, cubehelix, cubehelix_r, flag, flag_r, gist_earth, gist_earth_r, gist_gray, gist_gray_r, gist_heat, gist_heat_r, gist_ncar, gist_ncar_r, gist_rainbow, gist_rainbow_r, gist_stern, gist_stern_r, gist_yarg, gist_yarg_r, gnuplot, gnuplot2, gnuplot2_r, gnuplot_r, gray, gray_r, hot, hot_r, hsv, hsv_r, inferno, inferno_r, jet, jet_r, magma, magma_r, nipy_spectral, nipy_spectral_r, ocean, ocean_r, pink, pink_r, plasma, plasma_r, prism, prism_r, rainbow, rainbow_r, seismic, seismic_r, spring, spring_r, summer, summer_r, tab10, tab10_r, tab20, tab20_r, tab20b, tab20b_r, tab20c, tab20c_r, terrain, terrain_r, twilight, twilight_r, twilight_shifted, twilight_shifted_r, viridis, viridis_r, winter, winter_r'''.split(
    ',')
colormaps = list(map(lambda c: c.strip(), colormaps))


def load_font(fontpath):
    fp = pathlib.Path(fontpath)
    if fp.suffix in ['.ttf', '.otf']:
        font = TTFont(fontpath)
    elif fp.suffix == '.ttc':
        font = TTFont(fontpath, fontNumber=0)
    else:  # not yet
        raise Exception('unkonw suffix')
    return font


def text_supported_by_font(text, fontpath):
    font = load_font(fontpath)

    def char_in_font(char, font):
        for cmap in font['cmap'].tables:
            if ord(char) in cmap.cmap:
                return True
        return False
    r = [char_in_font(char, font) for char in text]
    return all(r)


def make_wordcloud(text, font_path, colormap, outputfilepath):
    wordcloud = WordCloud(
        width=1920,
        height=1080,
        max_words=3000,
        max_font_size=80,
        min_font_size=40,
        colormap=colormap,
        prefer_horizontal=0.3,
        font_path=font_path,
        repeat=True
    )
    r = wordcloud.generate(text)
    r.to_file(outputfilepath)


def simple_make_wordcloud(text, outputfilepath, fonts_dir='fonts/'):
    all_supported_fonts = list(find_all_supported_fonts(text, fonts_dir))
    fontpath = random.choice(all_supported_fonts)
    colormap = random.choice(colormaps)
    _ = make_wordcloud(text, fontpath, colormap, outputfilepath)


def find_all_supported_fonts(text, fonts_dir):
    for f in glob.glob(f'{fonts_dir}/**', recursive=True):
        fp = pathlib.Path(f)
        if fp.is_dir():
            continue
        if text_supported_by_font(text, f):
            yield f
