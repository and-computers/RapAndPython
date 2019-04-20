#!/usr/bin/env python3

import os
import gzip
import gensim


from music_utilities import initialize_data_objects, extract_songs_from_albums, make_reference_dictionary
from music_utilities import create_comparative_dict_from_artist_list, list_all_artists, get_artist_metadata

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

    filename = '{}_rap_lines.txt'.format(save_fname)

    with open(filename, 'w+') as f:

        for artist in artists_list:
            artist_album_objs = initialize_data_objects(artist)
            for album in artist_album_objs:
                print(album)
                this_year = album.year
                lines = album.aggregate_lines()
                for line in lines:
                    f.write(line)


# import pdb
# pdb.set_trace()
all_artists = list_all_artists()

artist_df = get_artist_metadata()
# get all the artists from each region

for region in REGIONS:
    region_rows = artist_df[artist_df['region'] == region]
    region_artists = list(region_rows.artist)
    all_counts = process_artists_nnp_counts(
        artists=region_artists, save_file=True, save_fname=region)
    print(region)
    print(all_counts)
