#!/usr/bin/env python2
"""
A series of classes to make abstraction of artists
and music and albums and lyrics easier to do for analysis
"""
import logging
import os
import re
import itertools

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
	def __init__(self,song_objects,album_name=None):
		if album_name:
			self.name = album_name
		else:
			self.name = song_objects[0].album_name
		self.year = song_objects[0].album_year
		self.num_songs = len(song_objects)
		list_of_lists_features = [x.features for x in song_objects]
		# compress list of lists into one single list
		self.features = set(list(itertools.chain.from_iterable(list_of_lists_features)))
		self.song_objects = song_objects

	def __repr__(self):
		return 'Album: {aname} ({yr})'.format(aname=self.name,yr=self.year)


	def find_references(self,regex):
		allrefs = []
		for song in self.song_objects:
			refs = song.find_references(regex=regex)
			allrefs += refs

		return allrefs


class Song(object):
	"""
	An object to hold song data and metadata
	such as features, artist, number of words, number of verses
	"""
	def __init__(self,lyric_file_txt,fname):

		self.song_name = fname.split(os.sep)[-1].replace('_',' ').replace('.txt','')

		self.lyrics,self.album_info = self._separate_lyrics(lyric_file_txt)
		self.album_name, self.album_year = self._find_album_info()
		self.features = self._find_features()

	def __repr__(self):
		return 'Song:{s},Album: {aname} ({yr})'.format(
			s=self.song_name,
			aname=self.album_name,
			yr=self.album_year
			)

	def find_references(self,regex):
		"""
		Find references in lyrics that match a certain regex formula

		:param regex: regular expression to match within lyrics
		:regex type: str

		:returns: list of the references that match regex
		:rtype: list
		"""
		all_lyrics = ''.join(self.lyrics)
		found_refs = re.findall(regex,all_lyrics)
		return found_refs


	def _separate_lyrics(self,lyrics_txt):
		"""
		seperate lyrics from the album information
		"""
		try:
			#idx_of_album_info = lyrics_txt.index('ALBUM INFO\r\n')

			idx_of_album_info = [i for i,item in enumerate(lyrics_txt) if re.search(r'ALBUM INFO\s',item)][0]

		except (ValueError,IndexError):
			idx_of_album_info = len(lyrics_txt)

		only_lyrics = lyrics_txt[:idx_of_album_info]
		album_info = lyrics_txt[idx_of_album_info:]

		return only_lyrics,album_info

	def _find_album_info(self):
		"""
		Determine informationa bout the album
		specifically the name and year of release

		If the data is not included in the song text, set them both as None
		"""

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

	def _find_features(self):
		"""
		Find all the featured artists in the song
		most of the times the lyrics are entered with each verse
		having a name before it like this

		[Jay-Z:]
		lyrics lyrics lyrics lyrics
		[Nas:]
		lyrics lyrics lyrics lyrics

		But also need some logic for getting of rid things like this

		[Intro]
		TAY KEEIITHHHHHH FFF THHEESEESE NINJAAS UPP1!!
		[Verse 1]
		yadda yadda yadda
		[Verse 2]
		yadda yadda yadda [x2]
		[Hook]
		singy songy sing song [x6]
		[Verse 3]
		bars bars bars
		[Outro]
		*jadakiss laugh*
		"""

		# first find things in between brackets
		things_in_brackets = set(re.findall(r"[^[]*\[([^]]*)\]",''.join(self.lyrics)))
		feature_names = []
		for fname in things_in_brackets:

			#get rid of Verse/Hook/Bridge etc. qualifiers
			fname = re.sub(r'(verse|hook|bridge|chorus|interlude|inaudible|ad-libs|sample)([:*\s|x|-]*\d)*','',fname.lower())
			# # remove leading dashes after breaking down feature
			# fname = re.sub(r'^-','',fname)
			fname = fname.lower().replace(":","").replace("intro","").replace("verse","").replace("interlude","").replace("hook","").replace("chorus","").replace("outro","").strip()
			# remove leading dashes again if they appear after this breakdown
			fname = re.sub(r'^-','',fname)
			

			# also split up things that are like meek mill & desiigner or meek mill (designer)
			fname = fname.replace("(","&").replace(")","").replace("and","&")
			fnames = fname.split("&")


			for split_name in fnames:
				# sometimes its unknown and filled in with question mark sometimes its repeated phrases like "x2"
				if split_name and not split_name=="?" and not re.findall(r'x\d',split_name):
					feature_names.append(split_name.strip())

		return feature_names




	@property
	def album_name(self):
		return self._album_name 

	@album_name.setter
	def album_name(self,albumname):
		self._album_name=albumname
		
