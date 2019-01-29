import pdb
import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# import pandas as pd

with open('spotify_api/creds.txt') as f_h:
    creds = f_h.read()

sp = spotipy.Spotify(
    auth=creds)

results = sp.search(q='soulja boy', limit=10)

colnames = ['song_name', 'id', 'duration_ms', 'time_signature', 'danceability',
            'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
            'release_date']


songs_dicts = []
for i, t in enumerate(results['tracks']['items']):

    track_object = sp.track(t['id'])
    release_date = track_object['album']['release_date']
    # returns a list of one element
    audio_features = sp.audio_features(t['id'])[0]
    print(' ', i, t['name'], t['id'], audio_features)

    rowdict = {'release_date': release_date, 'song_name': t['name']}
    for col in colnames:
        try:
            rowdict[col] = audio_features[col]
        except KeyError as ke:
            continue

    songs_dicts.append(rowdict)

with open('spotify_api/audio_data/soulja_boy.csv', 'w+') as f_h:
    datawriter = csv.DictWriter(f_h, fieldnames=colnames)
    datawriter.writeheader()
    for x in songs_dicts:
        datawriter.writerow(x)
