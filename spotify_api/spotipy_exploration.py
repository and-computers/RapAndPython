#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pdb
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# import pandas as pd


AUDIO_FEATURE_COLS = ['song_name', 'id', 'duration_ms', 'time_signature', 'danceability',
                      'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                      'release_date']


def get_client_id(fname='spotify_api/creds/client_id.txt'):
    """
    get spotify credentials for api access
    """

    with open(fname) as f_h:
        creds = f_h.read()

    return creds


def get_client_secret(fname='spotify_api/creds/client_secret.txt'):
    """
    get client secret
    """
    with open(fname) as f_h:
        creds = f_h.read()

    return creds


def generate_token():
    """
    Generate the token.
    """
    client_id = get_client_id()
    client_secret = get_client_secret()
    credentials = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret)
    token = credentials.get_access_token()
    return token


def read_playlist(spotify, username, playlist_id, fields='tracks,next,name'):
    """
    get the tracks from a playlist
    """
    playlist_results = spotify.user_playlist(username, playlist_id,
                                             fields=fields)
    # text_file = u'{0}.txt'.format(results['name'], ok='-_()[]{}')
    num_tracks = playlist_results['tracks']['total']
    print(f'Read {num_tracks} tracks')
    playlist_tracks = playlist_results['tracks']['items']
    # write_tracks(text_file, tracks)
    return playlist_tracks


def write_data(spotify, track_results, fname='spotify_api/audio_data/yada.csv'):
    """
    write data to a file
    """

    songs_dicts = []
    for i, t in enumerate(track_results['tracks']['items']):

        track_object = spotify.track(t['id'])
        release_date = track_object['album']['release_date']
        # returns a list of one element
        audio_features = spotify.audio_features(t['id'])[0]
        print(' ', i, t['name'], t['id'], audio_features)

        rowdict = {'release_date': release_date, 'song_name': t['name']}
        for col in AUDIO_FEATURE_COLS:
            try:
                rowdict[col] = audio_features[col]
            except KeyError as ke:
                continue

        songs_dicts.append(rowdict)

    with open(fname, 'w+') as f_h:
        datawriter = csv.DictWriter(f_h, fieldnames=AUDIO_FEATURE_COLS)
        datawriter.writeheader()
        for x in songs_dicts:
            datawriter.writerow(x)


def main():
    """
    run the functions
    """
    creds = generate_token()
    SP = spotipy.Spotify(auth=creds)

    PLAYLIST_ID = '0eCUnMZEBIlbR5tHTdnJN3'
    USERNAME = 'omo_desol'

    playlist_information = read_playlist(spotify=SP, username=USERNAME, playlist_id=PLAYLIST_ID)
    # playlist_information['items'][0]['track']['id']
    # tracks, artists = create_spotify_objects(playlist_information)
    import pdb
    pdb.set_trace()

if __name__ == "__main__":
    main()
