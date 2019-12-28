#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
spotify objects for easy access to api result data
"""

"""
{
'album': {'album_type': 'album', 'artists': [{'external_urls': {'spotify': 'https://open.spotify.com/artist/3nFkdlSjzX9mRTtwJOzDYB'}, 'href': 'https://api.spotify.com/v1/artists/3nFkdlSjzX9mRTtwJOzDYB', 'id': '3nFkdlSjzX9mRTtwJOzDYB', 'name': 'JAY-Z', 'type': 'artist', 'uri': 'spotify:artist:3nFkdlSjzX9mRTtwJOzDYB'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/5K4W6rqBFWDnAN6FQUkS6x'}, 'href': 'https://api.spotify.com/v1/artists/5K4W6rqBFWDnAN6FQUkS6x','id': '5K4W6rqBFWDnAN6FQUkS6x', 'name': 'Kanye West', 'type': 'artist', 'uri': 'spotify:artist:5K4W6rqBFWDnAN6FQUkS6x'}]

, 'available_markets': ['AD', 'AE', 'AR', 'AT', 'AU', 'BE', 'BG', 'BH', 'BO', 'BR', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GR', 'GT', 'HK', 'HN', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'KW', 'LB', 'LI', 'LT', 'LU', 'LV', 'MA', 'MC', 'MT', 'MX', 'MY', 'NI', 'NL', 'NO', 'NZ', 'OM', 'PA', 'PE', 'PH', 'PL', 'PS', 'PT', 'PY', 'QA', 'RO', 'SA', 'SE', 'SG', 'SK', 'SV', 'TH', 'TN', 'TR', 'TW', 'US', 'UY', 'VN', 'ZA'], 'external_urls': {'spotify': 'https://open.spotify.com/album/2P2Xwvh2xWXIZ1OWY9S9o5'},
'href': 'https://api.spotify.com/v1/albums/2P2Xwvh2xWXIZ1OWY9S9o5',
'id': '2P2Xwvh2xWXIZ1OWY9S9o5',
'images': [{'height': 640, 'url': 'https://i.scdn.co/image/c0df37da32cbe3212fbc95fd6863e2e9047b086f', 'width': 640}, {'height': 300, 'url': 'https://i.scdn.co/image/710773935f23bbb23ddb5386917e8808d8927e27', 'width': 300}, {'height': 64, 'url': 'https://i.scdn.co/image/9e70cdaf36271d32aa4332cc5eef31a3354632e7', 'width': 64}],
'name': 'Watch The Throne (Deluxe)',
'release_date': '2011-08-08',
'release_date_precision': 'day',
'total_tracks': 16,
'type': 'album',
'uri': 'spotify:album:2P2Xwvh2xWXIZ1OWY9S9o5'},

 'artists': [
 {'external_urls': {'spotify': 'https://open.spotify.com/artist/3nFkdlSjzX9mRTtwJOzDYB'}, 'href': 'https://api.spotify.com/v1/artists/3nFkdlSjzX9mRTtwJOzDYB', 'id': '3nFkdlSjzX9mRTtwJOzDYB', 'name': 'JAY-Z', 'type': 'artist', 'uri': 'spotify:artist:3nFkdlSjzX9mRTtwJOzDYB'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/5K4W6rqBFWDnAN6FQUkS6x'}, 'href': 'https://api.spotify.com/v1/artists/5K4W6rqBFWDnAN6FQUkS6x', 'id': '5K4W6rqBFWDnAN6FQUkS6x', 'name': 'Kanye West', 'type': 'artist', 'uri': 'spotify:artist:5K4W6rqBFWDnAN6FQUkS6x'}, {'external_urls': {'spotify': 'https://open.spotify.com/artist/60df5JBRRPcnSpsIMxxwQm'}, 'href': 'https://api.spotify.com/v1/artists/60df5JBRRPcnSpsIMxxwQm', 'id': '60df5JBRRPcnSpsIMxxwQm', 'name': 'Otis Redding', 'type': 'artist', 'uri': 'spotify:artist:60df5JBRRPcnSpsIMxxwQm'}],

  'available_markets': ['AD', 'AE', 'AR', 'AT', 'AU', 'BE', 'BG', 'BH', 'BO', 'BR', 'CA', 'CH', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DE', 'DK', 'DO', 'DZ', 'EC', 'EE', 'EG', 'ES', 'FI', 'FR', 'GB', 'GR', 'GT', 'HK', 'HN', 'HU', 'ID', 'IE', 'IL', 'IN', 'IS', 'IT', 'JO', 'KW', 'LB', 'LI', 'LT', 'LU', 'LV', 'MA', 'MC', 'MT', 'MX', 'MY', 'NI', 'NL', 'NO', 'NZ', 'OM', 'PA', 'PE', 'PH', 'PL', 'PS', 'PT', 'PY', 'QA', 'RO', 'SA', 'SE', 'SG', 'SK', 'SV', 'TH', 'TN', 'TR', 'TW', 'US', 'UY', 'VN', 'ZA'],

  'disc_number': 1,
  'duration_ms': 178213,
  'episode': False, 'explicit': True,
  'external_ids': {'isrc': 'USUM71111634'},
  'external_urls': {'spotify': 'https://open.spotify.com/track/6vegnfDS8DAEaCqWaPYGPy'},
  'href': 'https://api.spotify.com/v1/tracks/6vegnfDS8DAEaCqWaPYGPy',
  'id': '6vegnfDS8DAEaCqWaPYGPy',
  'is_local': False,
  'name': 'Otis',
  'popularity': 69,
  'preview_url': None,
  'track': True,
  'track_number': 4,
  'type':
  'track',
  'uri': 'spotify:track:6vegnfDS8DAEaCqWaPYGPy'

  }
"""


class SpotifyTrack():
    """
    class to encapsulate track informatoin
    """

    def __init__(self, raw_dict: dict):
        self.album = None
        self.id = None
        self.duration = None
        self.name = None
        self.uri = None
        self.popularity = None
        self.href = None
        self.artists = []
        self._process_raw(raw_dict)

    def _process_raw(self, raw_dict):
        """
        take the raw dictionary and
        create attributes for easy access
        """

        self.album = SpotifyAlbum(raw_dict['album'])
        self.id = raw_dict['id']
        self.duration = raw_dict['duration_ms']
        self.name = raw_dict['name']
        self.popularity = raw_dict['popularity']
        self.href = raw_dict['href']
        self.uri = raw_dict['uri']

        for artist_dict in raw_dict['artists']:
            artist = SpotifyArtist(artist_dict)
            self.artists.append(artist)


class SpotifyAlbum():
    """
    class to encapsulate album informatoin
    """

    def __init__(self, raw_dict: dict):
        self._process_raw(raw_dict)

    def _process_raw(self):
        """
        take the raw dictionary and
        create attributes for easy access
        """


class SpotifyArtist():
    """
    class to encapsulate artist informatoin
    """

    def __init__(self, raw_dict: dict):
        self._process_raw(raw_dict)

    def _process_raw(self):
        """
        take the raw dictionary and
        create attributes for easy access
        """
