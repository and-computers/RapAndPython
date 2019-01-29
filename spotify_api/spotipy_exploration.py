import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

with open('spotify_api/creds.txt') as f_h:
    creds = f_h.read()
#client_credentials_manager = SpotifyClientCredentials(creds)

print(creds)

sp = spotipy.Spotify(
    auth=creds)

results = sp.search(q='weezer', limit=10)
for i, t in enumerate(results['tracks']['items']):
    print(' ', i, t['name'])
