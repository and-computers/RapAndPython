#!/usr/bin/env python2

import os

from MusicObjects import Song, Album, Artist



toplevel = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIRNAME = 'scraped_data'
ARTISTNAME = 'meekmill'

artist_directory = os.path.join(toplevel,DIRNAME,ARTISTNAME)

song_files = [os.path.join(artist_directory,songfile) for songfile in os.listdir(artist_directory) if 'Submit_Lyrics' not in songfile]

song_objects = []


for song_file in song_files:
	with open(song_file,'r') as f:
		song_txt = f.readlines()
		song_obj = Song(song_txt,song_file)

		print(song_obj)

		song_objects.append(song_obj)




#idx_of_album_info = txt_file_lines.index('ALBUM INFO\r\n')