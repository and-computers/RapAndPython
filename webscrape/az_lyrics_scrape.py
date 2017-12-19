"""
managedkaos/azlyrics.py
https://gist.github.com/managedkaos/e3262b80154129cc9a976ee6ee943da3
"""

# Requests is a library that allows you to programmatically send out http requests 
import requests
# os is a library for doing operating system things, like looking through file directories
import os
# BeautifulSoupp is a library made to allow developers to parse through the contents of a webpage
from bs4 import BeautifulSoup
url = "https://www.azlyrics.com/o/outkast.html"


# act like a mac when requesting url
headers = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.112 Safari/534.30"}

# make a request for the data
r = requests.get(url, headers=headers)

# convert the response text to soup
soup = BeautifulSoup(r.text, "lxml")

# get the songs and links to the lyrics
lyrics_map = {}
for song_link in soup.find_all("a", href=True):
    if len(song_link.text) == 0:
    	continue
    lyrics_map[song_link.text] = song_link['href']
    lyric_url = song_link['href']
    if ".." in lyric_url:
	    lyric_url = "https://www.azlyrics.com"+lyric_url[2:]
	    print lyric_url
	    response = requests.get(lyric_url, headers=headers)
	    new_soup = BeautifulSoup(response.text,"lxml")
	    filename = song_link.text.replace(' ','_').replace("'",'')
	    filename += ".txt"
	    filename = "scraped_data" + os.sep + filename
	    print filename
	    f = open(filename,"w+")
	    for lyric in new_soup.find_all("div",{"class":None}):
	    	print lyric.text
	    	f = open(filename,"a")
	    	f.write(lyric.text)
	    f.close()


