#!/usr/bin/env python2
"""
analysis of proper nouns usage in rap music.
"""
import operator
import os
import pickle
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from music_utilities import initialize_data_objects, extract_songs_from_albums, make_reference_dictionary
from music_utilities import create_comparative_dict_from_artist_list, list_all_artists

NNP = 'NNP'


def process_artists_nnp_counts(artist=None, load_file=None):

    if load_file:
        with open(load_file, 'r') as f:
            file_data = pickle.load(f)
        return file_data

    if not artist:
        artists_list = list_all_artists()
    else:
        artists_list = [artist]

    count_my_shit = {}

    for artist in artists_list:
        artist_album_objs = initialize_data_objects(artist)
        for album in artist_album_objs:
            lines = album.aggregate_lines()
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

    sorted_counts = sorted(count_my_shit.items(), key=operator.itemgetter(1))
    return sorted_counts

all_counts = process_artists_nnp_counts(load_file='noun_counts.pickle')

print(all_counts)
