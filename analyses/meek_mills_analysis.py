#!/usr/bin/env python2

import os

from MusicObjects import Song, Album, Artist
from visualizations import create_references_df, simple_bar_from_df, comparative_bar_from_df, create_pie_chart

from ml_stats import markov_gen

"""
Initialize data objects to allow music analysis
"""

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

	artist_directory = os.path.join(toplevel,DIRNAME,ARTISTNAME)

	song_files = [os.path.join(artist_directory,songfile) for songfile in os.listdir(artist_directory) if 'Submit_Lyrics' not in songfile]

	song_objects = []


	for song_file in song_files:
		with open(song_file,'r') as f:
			song_txt = f.readlines()
			song_obj = Song(song_txt,song_file)

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
	for album_name, song_list in album_dict.iteritems():
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

def make_reference_dictionary(list_of_songs,regex):
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

		ref_d[song.song_name] = (refs,len(refs),song.album_year)

	return ref_d


def create_comparative_dict_from_artist_list(list_of_artists,regex):
	"""
	create comparative dictionary that can be used as an input into the
	comparative bar chart plotting functionality. 
	regex is the matching expression to run through the lyrics of each artists songs
	"""
	comparative_dict = {}

	for artist in list_of_artists:
		album_objects = initialize_data_objects(artist)
		artists_songs = extract_songs_from_albums(album_objects)
		referential_dict = make_reference_dictionary(artists_songs,regex)
		_,grouped_df = create_references_df(referential_dict)

		comparative_dict[artist] = grouped_df

	return comparative_dict


"""
Analysis
"""

#regex expressions
homo_regex= r'f[a]*g\w{0,}'
gay_regex = r'g[a]*y\w{0,}'
bitch_regex = r'b[i]*tch\w{0,}|\sho[es]*\s'
rape_regex = r'rap[ie]\w{0,}'
nigga_regex = r'nigg[a]\w{0,}'

jail_regex = r'jail\w{0,}|prison\w{0,}|cell\w{0,1}\s|polic\w{0,}|cop[s]*|locked\sup|incarcerat\w{0,}|penitenti\w{0,}'
mother_regex = r'\smother[s]|\smomm\w{0,}|\smom[s]*|mama'


"""
Make grouped bar DF for Meek Mill and all the other artists
"""

artist_list = ['yg','meekmill','jayz','common','blueface','kendricklamar','drake','lupefiasco','lilwayne']

# d = create_comparative_dict_from_artist_list(artist_list,jail_regex)
# comparative_bar_from_df(
# 	d,
# 	graph_title='Jail References Across Artists',
# 	x_data='year',
# 	y_data='avg ref',
# 	x_title='Year',
# 	y_title='Jail References per Song'
# 	)

"""
Make pie chart for What's Free Verse Distribution
"""

# words per verse
# labels = ['JAY-Z','Meek Mill','Rick Ross']

# values = [422,263,210]
# value_sum = sum(values)
# import numpy as np
# values_raw = 100.*(np.array(values)/float(value_sum))
# values = []
# for v in values_raw:
# 	values.append(round(v,2))

# colors = ['#FEBFB3', '#E1396C', '#96D38C', '#D0F9B1']

# create_pie_chart(labels,values,colors)

"""
Make bar DF for Meek Mill
"""

# artist2analyze = 'meekmill'
# artist_album_objects = initialize_data_objects(artist2analyze)
# allsongs = extract_songs_from_albums(artist_album_objects)
# mm_ref_dict = make_reference_dictionary(allsongs,jail_regex)
# _,mm_grouped_df = create_references_df(mm_ref_dict)
# simple_bar_from_df(
# 	mm_grouped_df,
# 	graph_title='{}\'s Jail References: An Exploration'.format(artist2analyze),
# 	x_data='year',
# 	y_data='avg ref',
# 	x_title='Year',
# 	y_title='Average # of Jail References Per Song'
# 	)


"""
Markov Verse generation
"""
artist2analyze = 'meekmill'
artist_album_objects = initialize_data_objects(artist2analyze)

championship_corpus = []
everything_else_corpus = []
for x in artist_album_objects:
	if x.name == "Championships":

		lines = x.aggregate_artist_verses_on_album(r'meek')
		championship_corpus += lines

	else:
		lines = x.aggregate_artist_verses_on_album(r'meek')
		everything_else_corpus += lines

old_markov_verse = markov_gen(
	train_text=everything_else_corpus,
	state_size=2,
	output_size=16,
	)

print(old_markov_verse)


championship_markov_verse = markov_gen(
	train_text=championship_corpus,
	state_size=2,
	output_size=16,
	)

print(championship_markov_verse)











