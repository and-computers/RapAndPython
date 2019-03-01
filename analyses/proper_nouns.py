#!/usr/bin/env python2
"""
analysis of proper nouns usage in rap music.
"""
import os
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from music_utilities import initialize_data_objects, extract_songs_from_albums, make_reference_dictionary
from music_utilities import create_comparative_dict_from_artist_list, list_all_artists

NNP = 'NNP'
os.
artists_list = list_all_artists

count_my_shit = {}

for artist in artists_list:
    artist_album_objs = initialize_data_objects(artist)
    for album in artist_album_objs:
        lines = album.aggregate_artist_verses_on_album(r'jay')
        for line in lines:
            try:
                tokenized_line = word_tokenize(line)
                for word, pos in pos_tag(tokenized_line):
                    if pos == NNP:
                        w = word.lower()
                        if w in count_my_shit.keys():
                            count_my_shit[w] += 1
                        elif w not in count_my_shit.keys():
                            count_my_shit[w] = 1
            except UnicodeDecodeError as e:
                continue


import pdb
pdb.set_trace()
