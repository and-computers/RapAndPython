#!/usr/bin/env python2
"""
some utilities for using MusicObjects
"""
import os
import pandas as pd
from MusicObjects import Song, Album, Artist


def get_artist_metadata():
    toplevel = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DIRNAME = 'artist_data'
    path = os.path.join(toplevel, DIRNAME, 'artist_map.csv')
    artist_meta_data_df = pd.read_csv(path)

    return artist_meta_data_df


def list_all_artists():
    toplevel = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DIRNAME = 'scraped_data'

    path = os.path.join(toplevel, DIRNAME)
    artists = os.listdir(path)

    return [x for x in artists if not x.startswith('.')]


def initialize_data_objects(artistname):
    """
    :param artistname: name of the diretory that contains an artist to initialize
    :type artistname: str

    :returns: list of album objects
    :rtype: list
    """

    toplevel = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DIRNAME = 'scraped_data'
    ARTISTNAME = artistname

    artist_directory = os.path.join(toplevel, DIRNAME, ARTISTNAME)

    song_files = [os.path.join(artist_directory, songfile)
                  for songfile in os.listdir(artist_directory) if 'Submit_Lyrics' not in songfile]

    song_objects = []

    for song_file in song_files:
        with open(song_file, 'r') as f:
            song_txt = f.readlines()
            song_obj = Song(song_txt, song_file)

        song_objects.append(song_obj)

    album_dict = {}
    for song in song_objects:
        album_name = song.album_name
        if album_name:
            if album_name in album_dict.keys():
                album_dict[album_name].append(song)
            else:
                album_dict[album_name] = [song]

    album_objects = []
    for album_name, song_list in album_dict.items():
        new_album = Album(song_list)
        album_objects.append(new_album)

    return album_objects


def extract_songs_from_albums(album_objs):
    """
    return a list of songs when given a list of album objects
    """
    allsongs = []
    for album in album_objs:

        allsongs += album.song_objects

    return allsongs


def make_reference_dictionary(list_of_songs, regex):
    """
    returns a dictionary that can be used as the input into the 
    graphing functions in the visualize module

    :param list_of_songs: 
    :type list_of_songs: list


    :returns: dictionary of tuples, where the key 
    is the name of the song file and the values is 3-tuple. The 3-tuple
    has fields of (list of references found, num of references found, year of reference)
    :rtype: dictionary
    """

    ref_d = {}
    for song in list_of_songs:

        refs = song.find_references(regex)

        ref_d[song.song_name] = (refs, len(refs), song.album_year)

    return ref_d


def create_comparative_dict_from_artist_list(list_of_artists, regex):
    """
    create comparative dictionary that can be used as an input into the
    comparative bar chart plotting functionality. 
    regex is the matching expression to run through the lyrics of each artists songs
    """
    comparative_dict = {}

    for artist in list_of_artists:
        album_objects = initialize_data_objects(artist)
        artists_songs = extract_songs_from_albums(album_objects)
        referential_dict = make_reference_dictionary(artists_songs, regex)
        _, grouped_df = create_references_df(referential_dict)

        comparative_dict[artist] = grouped_df

    return comparative_dict
