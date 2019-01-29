import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

with open('spotify_api/creds.txt') as f_h:
    creds = f_h.read()

sp = spotipy.Spotify(
    auth=creds)

results = sp.search(q='soulja boy', limit=10)


for i, t in enumerate(results['tracks']['items']):

    audio_analysis = sp.audio_analysis(t['id'])
    audio_features = sp.audio_features(t['id'])
    print(' ', i, t['name'], t['id'], audio_features)
