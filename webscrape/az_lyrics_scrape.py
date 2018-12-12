"""
managedkaos/azlyrics.py
https://gist.github.com/managedkaos/e3262b80154129cc9a976ee6ee943da3
"""

# Requests is a library that allows you to programmatically send out http requests 
import requests
# os is a library for doing operating system things, like looking through file directories
import os
import time
import logging
import random

# BeautifulSoupp is a library made to allow developers to parse through the contents of a webpage
from bs4 import BeautifulSoup
import pandas as pd



logger = logging.getLogger('rap_webscraper.{}'.format(__name__))

logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('rap_webscrape.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

SLEEP_TIME = 15.212
NOISE = (-8.438,10.173)
#NOISE = (0,5)

# TODO: create from scrape_config.csv


# act like a mac when requesting url
headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) \
AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30"}

scrape_config = os.path.join("webscrape","scrape_config.csv")

df = pd.read_csv(scrape_config)

artists_and_urls = zip(df.to_dict()['artist'].values(),df.to_dict()['url'].values())

for artist_name,url in artists_and_urls:
	"""
	sleep before request
	you could check if the artists directory exists and skip first
	but if a previous scrape session ended midway you wouldnt check for any missed songs
	if the url lists gets too long you may get blocked just from the initial request to artist pages
	"""
	logger.info('Requesting songs from: {}'.format(url))
	pre_request_sleep = SLEEP_TIME+random.uniform(NOISE[0],NOISE[1])
	logger.info('Sleeping: {}'.format(pre_request_sleep))
	time.sleep(pre_request_sleep)
	# make a request for the data
	r = requests.get(url, headers=headers)

	# convert the response text to soup
	soup = BeautifulSoup(r.text, "lxml")

	# get the songs and links to the lyrics
	lyrics_map = {}
	artists_file_directory = url.split('/')[-1].replace('.html','')
	artists_file_directory = artist_name
	for song_link in soup.find_all("a", href=True):
		if len(song_link.text) == 0:
			continue
		lyrics_map[song_link.text] = song_link['href']
		lyric_url = song_link['href']

		if ".." in lyric_url:
			lyric_url = "https://www.azlyrics.com"+lyric_url[2:]
			logger.info("Looking @ Lyrics for {}".format(lyric_url))

			filename = song_link.text.replace(' ','_').replace("'",'').replace('/','')
			filename += ".txt"
			filename = os.path.join("scraped_data",artists_file_directory,filename)
			filename = filename.encode('utf-8')

			"""
			a lot of the unspecified excepts are just to catch annoying character encoding bs
			that comes with webscraping
			"""
			if os.path.exists(filename):
				try:
					logger.info('File {} already exists, skipping web request'.format(filename.encode('utf-8')))
				except:
					continue
				continue
			try:
				logger.debug('Requesting: {}'.format(lyric_url))
			except:
				pass
			"""
			sleep for some time (in seconds) so you arent banned from sites..
			add some random noise to the sleep so it don't look like a robot
			"""
			this_sleep = SLEEP_TIME+random.uniform(NOISE[0],NOISE[1])
			logger.info('Sleeping: {}'.format(this_sleep))
			time.sleep(this_sleep)
			response = requests.get(lyric_url, headers=headers)
			new_soup = BeautifulSoup(response.text,"lxml")

			try:
				logger.debug('Will Write to: {}'.format(filename))
			except:
				pass
			
			# https://stackoverflow.com/questions/12517451/automatically-creating-directories-with-file-output
			if not os.path.exists(os.path.dirname(filename)):
				try:
					os.makedirs(os.path.dirname(filename))
				except OSError as exc: # Guard against race condition
					if exc.errno != errno.EEXIST:
						raise

			f = open(filename,"w+")

			# loop through the no clas divs. they contain the lyrics
			for lyric in new_soup.find_all("div",{"class":None}):
				try:
					f = open(filename,"a")
				except IOError:
					logger.warning('IOError could not write filename: {}'.format(filename))
					continue
				try:
					f.write(lyric.text.encode('utf-8'))
				except UnicodeError:
					logger.warning('UnicodeError, Skipping: {}'.format(filename))
					f.close()
					continue

			# the song panel div has the album name and the year
			for song_panel_div in new_soup.find_all("div",{"class":"panel songlist-panel noprint"}):
				try:
					f.write('ALBUM INFO')
					f.write(song_panel_div.text.encode('utf-8'))
				except UnicodeError:
					logger.warning('UnicodeError, Skipping')
					f.close()
					continue

			f.close()


