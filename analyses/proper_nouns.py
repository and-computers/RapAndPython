#!/usr/bin/env python2
"""
analysis of proper nouns usage in rap music.
"""
import operator
import os
import pickle
import time

from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

from music_utilities import initialize_data_objects, extract_songs_from_albums, make_reference_dictionary
from music_utilities import create_comparative_dict_from_artist_list, list_all_artists, get_artist_metadata

non_nnp_filter = ['got', 'nigga', 'hook', 'verse', 'chorus', 'intro', 'outro', 'gettin',
                  'niggas', 'niggaz', 'verse', 'fuck', 'got', 'young',
                  'cause', 'shit', 'yea', 'shawty', 'bitch', 'money', 'homie',
                  'couple', 'cuz', 'monday', "i'mma", 'girl', 'rock', 'damn',
                  'talking', 'talkin', 'told', 'had', 'black', 'bridge', 'hey',
                  'wan', 'check', 'seen', 'glow', 'glowin', 'dem', 'same', 'dream',
                  'ah', 'pop', 'sippen', 'ap', 'black', 'baby', 'poppin', 'booty',
                  'god', 'lord', 'lil', 'say', 'tryna', 'yo', 'tell', 'ooh', 'uh', 'ya',
                  'bought', 'was', 'did', 'oh', 'ride', 'cash', 'heard', 'make', "i'ma", 'bad',
                  'them', 'i\xc3\xa2\xc2\x80\xc2\x99m', 'grind', 'y', 'ugh', 'da', 'said',
                  'i\xc3\xa2\xc2\x80\xc2\x99ma', 'my', 'me', 'ca', 'fly', 'fuckin', 'dj',
                  'dey', 'pull', 'know', 'lot', 'woo', 'uhh', 'ha', 'be', 'im', 'ma', 'bitches'
                  ]
NNP = 'NNP'
REGIONS = ['West', 'Midwest', 'East', 'South']


def process_artists_nnp_counts(artists=None, load_file=None, save_file=False, save_fname=None):

    if load_file:
        with open(load_file, 'r') as f_l:
            file_data = pickle.load(f_l)
        return file_data

    if not artists:
        artists_list = list_all_artists()
    else:
        artists_list = artists

    count_my_shit = {}

    for artist in artists_list:
        artist_album_objs = initialize_data_objects(artist)
        for album in artist_album_objs:
            print(album)
            this_year = album.year
            lines = album.aggregate_lines()
            for line in lines:
                try:
                    tokenized_line = word_tokenize(line)
                    for word, pos in pos_tag(tokenized_line):
                        if pos == NNP:
                            w = word.lower()
                            if w not in non_nnp_filter and len(w) > 1:
                                if w in count_my_shit.keys():
                                    count_my_shit[w] += 1
                                elif w not in count_my_shit.keys():
                                    count_my_shit[w] = 1
                except UnicodeDecodeError as e:
                    continue

    sorted_counts = sorted(count_my_shit.items(), key=operator.itemgetter(1))
    if save_file:
        time_sec = int(time.time())
        filename = 'counts_{}.pickle'.format(time_sec)
        if save_fname:
            filename = '{}_counts_{}.pickle'.format(save_fname, time_sec)
        with open(filename, 'w+') as f_w:
            pickle.dump(sorted_counts, f_w)

    return sorted_counts

all_artists = list_all_artists()

artist_df = get_artist_metadata()
# get all the artists from each region

for region in REGIONS:
    region_rows = artist_df[artist_df['region'] == region]
    region_artists = list(region_rows.artist)
    all_counts = process_artists_nnp_counts(artists=region_artists, save_file=True, save_fname=region)
    print(region)
    print(all_counts)
