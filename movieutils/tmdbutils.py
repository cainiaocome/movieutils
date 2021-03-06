#!/usr/bin/env python

import traceback
import tmdbsimple as tmdb
from pprint import pprint
from .youtube_dl_utils import download, load_key_video_dict, get_best_subtitle_or_en

def get_movie_detail(tmdb_movie_id):
    movie = tmdb.Movies(tmdb_movie_id)
    movie_detail = movie.info()

    translations = movie.translations()['translations']
    movie_detail['translations'] = translations
    translation = is_translation_available(movie_detail)
    if not translation:
        return None
    movie_detail['title'] = translation['data']['title']

    videos = movie.videos()['results']
    movie_detail['videos'] = videos
    best_video = get_best_video(movie_detail)
    if not bool(best_video):
        return None
    key = best_video['key']
    download(key)
    key_video_dict = load_key_video_dict()
    video_input = key_video_dict.get(key, '')
    if not video_input:
        return None
    movie_detail['video_input'] = video_input
    movie_detail['subtitle'] = get_best_subtitle_or_en(key, 'zh-Hans')

    return movie_detail


# 根据条件筛选出一个列表
def get_movie_agg(d_d, pages, max=10):
    movie_agg = []
    for page in range(1, pages):
        d_d['page'] = page
        movie_l = tmdb.Discover().movie(**d_d)
        movie_l = movie_l['results']

        # 获取该列表每个元素的detail
        for movie in movie_l:
            try:
                detail = get_movie_detail(movie['id'])
                if detail:
                    movie_agg.append(detail)
                if len(movie_agg)>=max:
                    return sorted(movie_agg, key=lambda movie:bool(movie['subtitle']), reverse=True)
            except:
                print('-'*30)
                traceback.print_exc()
                pprint(movie)
                print('-'*30)
    return sorted(movie_agg, key=lambda movie:bool(movie['subtitle']), reverse=True)


# 过滤video信息，只选择Trailer, Teaser, Clip, 并且youtube 720P以上的video
def get_best_video(movie):
    videos = movie['videos']
    videos = filter(lambda video:video['site']=='YouTube', videos)
    videos = filter(lambda video:video['type'] in ['Trailer', 'Teaser', 'Clip'], videos)
    best_video = {}
    for video in videos:
        if video['size'] == 1080: # prefer 1080
            return video
        if video['size']>=best_video.get('size', 720):
            best_video = video
    return best_video


def is_translation_available(movie, iso_639_1='zh', iso_3166_1='CN'):
    translations = movie['translations']
    for translation in translations:
        if translation['iso_639_1']==iso_639_1 and translation['iso_3166_1']==iso_3166_1:
            return translation
    else:
        return False
