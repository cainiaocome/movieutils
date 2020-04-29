#!/usr/bin/env python

from pprint import pprint
import tmdb

movie_genres = tmdb.Genres().movie_list()
movie_genres = movie_genres['genres']
