#!/usr/bin/env python2
"""
A series of classes to make abstraction of artists
and music and albums and lyrics easier to do for analysis
"""
import logging
import os
import re

logger = logging.getLogger('lyrics_analysis.{}'.format(__name__))
logger.setLevel(logging.DEBUG)

class Artist(object):
	"""
	An artist object holds data about the artist
	including album object and regional data.
	"""
	def __init__(self):
		pass

class Album(object):
	"""
	An object to hold album data and metadata
	"""
	def __init__(self,song_objects):
		self.name = song_objects[0].album_name
		self.year = song_objects[0].year
		self.artist = song_objects[0].artist
		self.num_songs = len(song_objects)
		self.features = [x.features for x in song_objects]

class Song(object):
	"""
	An object to hold song data and metadata
	such as features, artist, number of words, number of verses
	"""
	def __init__(self,lyric_file_txt,fname):

		self.song_name = fname.split(os.sep)[-1].replace('_',' ').replace('.txt','')
		self.lyrics,self.album_info = self.separate_lyrics(lyric_file_txt)
		self.album_name, self.album_year = self.find_album_info()

	def __repr__(self):
		return 'Song:{s},Album: {aname} ({yr})'.format(
			s=self.song_name,
			aname=self.album_name,
			yr=self.album_year
			)


	def separate_lyrics(self,lyrics_txt):
		try:
			idx_of_album_info = lyrics_txt.index('ALBUM INFO\r\n')

		except ValueError:
			idx_of_album_info = len(lyrics_txt)

		only_lyrics = lyrics_txt[:idx_of_album_info]
		album_info = lyrics_txt[idx_of_album_info:]

		return only_lyrics,album_info

	def find_album_info(self):

		if self.album_info:

			alltxt_str = ''.join(self.album_info)


			yr = re.findall(r'\n?ALBUM INFO\r?\n\w{0,}?:\s".{0,}"\s\(\d+\)',alltxt_str)

			try:
				# take the last index in case the album name has numbers in it
				yr = int(re.findall(r'\d+',yr[0])[-1])
				if yr < 1900 or yr > 2020:
					logger.warning('Year was {yr} replacing with NaN'.format(
						yr=yr)
					)

					yr = None
			except IndexError:
				logger.warning('Was unable to find year')
				yr = None

			name = re.findall(r'"([^"]*)"', self.album_info[1])[0]
			return name,yr

		else:
			return None,None




	@property
	def album_name(self):
		return self._album_name 

	@album_name.setter
	def album_name(self,albumname):
		self._album_name=albumname
		
