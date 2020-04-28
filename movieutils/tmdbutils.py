#!/usr/bin/env python

import tmdbsimple as tmdb

def get_movie_detail(tmdb_movie_id):
    movie = tmdb.Movies(tmdb_movie_id)
    info = movie.info()
    videos = movie.videos()['results']
    info['videos'] = videos
    translations = movie.translations()['translations']
    info['translations'] = translations
    return info


# 根据条件筛选出一个列表
def get_movie_agg(d_d, pages):
    movie_agg = []
    for page in range(1, pages):
        d_d['page'] = page
        movie_l = tmdb.Discover().movie(**d_d)
        movie_l = movie_l['results']

        # 获取该列表每个元素的detail
        for movie in movie_l:
            try:
                detail = get_movie_detail(movie['id'])
                movie_agg.append(detail)
            except:
                print('-'*30)
                traceback.print_exc()
                pprint(movie)
                print('-'*30)
    return movie_agg


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
