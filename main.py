from textstat.textstat import textstat
import os
for root,dirs,fnameslist in os.walk("webscrape/scraped_data"):
	if len(dirs) == 0:
		for fname in fnameslist:
			f = open(os.path.join(root,fname),"r")
			txt = f.read()
			print fname + " has a reading level of: "
			print textstat.flesch_reading_ease(txt)
