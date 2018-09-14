#!/usr/bin/env python2

import os
import re
import logging

import pandas as pd
import numpy as np

import plotly.offline as pltly
import plotly.graph_objs as go

logger = logging.getLogger('lyrics_analysis.{}'.format(__name__))
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('lyrics_analysis.log')
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

"""
Known Issues: 
featured verses are counted same way
R&B artists dont have as many words in their songs
"""


def make_reference_dict(artist_dir,regex):
	"""
	Create a dictionary of tuples specifying references in songs
	takes in the directory containing the lyric files as well
	as the regular expression to identify the references of interest
	"""

	songs_number_ref = {}
	for root,dirs,fnameslist in os.walk("scraped_data"):
		if artist_dir in root:
			for fname in fnameslist:
				with open(os.path.join(root,fname)) as lyrics:
					alltxt = lyrics.read()
					found_ref = re.findall(regex,str(alltxt))
					num_refs = len(found_ref)

					yr = re.findall(r'\nALBUM INFO\r?\n\w{0,}?:\s".{0,}"\s\(\d+\)',alltxt)
					try:
						# take the last index in case the album name has numbers in it
						yr = int(re.findall(r'\d+',yr[0])[-1])
						if yr < 1900 or yr > 2020:
							logger.warning('Year for {art}/{f} was {yr} replacing with NaN'.format(
								art=artist_dir,
								f=fname,
								yr=yr)
							)
							yr = np.nan
					except IndexError:
						logger.warning('Was unable to find year in {art}/{f}'.format(
							art=artist_dir,
							f=fname)
						)
						yr = np.nan
					songs_number_ref[fname] = (found_ref,num_refs,yr)

	return songs_number_ref


def create_references_df(dictionary_of_3_tuples):
	"""
	Move from dictionary to pandas dataframe.

	:param dictionary_of_3_tuples: dictionary of tuples, where the key 
	is the name of the song file and the values is 3-tuple. The 3-tuple
	has fields of (list of references found, num of references found, year of reference)

	:returns: dataframe with the year, song name, number of references, and the words that match the reference
	:rtype: pandas DataFrame
	"""
	raw_df = pd.DataFrame()
	# fname, num references, year
	for songname, tuple_3 in dictionary_of_3_tuples.items():
		songname = songname.replace('.txt','')
		yr = tuple_3[2]
		words_found = str(tuple_3[0]).replace('[','').replace(']','')
		num_found = tuple_3[1]
		newrow = pd.DataFrame([[songname,num_found,yr,words_found]],
			columns=['song name','number of references','year','words'])
		raw_df = raw_df.append(newrow,ignore_index=False)


	grouped_df = raw_df.groupby('year')
	summed_df = grouped_df.sum()
	counted_df = grouped_df.count()

	cumulative_df = summed_df

	cumulative_df['year'] = summed_df.index.astype(int)
	cumulative_df['number of references'] = summed_df['number of references']
	cumulative_df['num songs'] = counted_df['song name']
	cumulative_df['avg ref'] = cumulative_df['number of references']/cumulative_df['num songs']


	return raw_df,cumulative_df

def simple_bar_from_df(df,graph_title,x_data,y_data,x_title=None,y_title=None):
	"""
	Function to generate a simple bar graph from a dataframe
	"""

	trace = go.Bar(x=df[x_data],y=df[y_data])

	layout = go.Layout(
	    title=graph_title,
	    xaxis=dict(
	    	# make the title the title if it exists, otherwise use x_data label
	        title=x_title if x_title else x_data,
	        titlefont=dict(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    ),
	    yaxis=dict(
	        title=y_title if y_title else y_data,
	        titlefont=dict(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    )
	)
	fig = go.Figure(data=[trace], layout=layout)
	pltly.plot(fig,filename=graph_title+'.html')

	return


def comparative_bar_from_df(df_d,graph_title,x_data,y_data,x_title=None,y_title=None):
	"""
	Function to generate a grouped bar graph from a dictionary of dataframes
	"""

	traces = []
	for name,df in df_d.items():
		trace = go.Bar(x=df[x_data],y=df[y_data],name=name)
		traces.append(trace)

	layout = go.Layout(
	    title=graph_title,
	    barmode='group',
	    xaxis=dict(
	    	# make the title the title if it exists, otherwise use x_data label
	        title=x_title if x_title else x_data,
	        titlefont=dict(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    ),
	    yaxis=dict(
	        title=y_title if y_title else y_data,
	        titlefont=dict(
	            family='Courier New, monospace',
	            size=18,
	            color='#7f7f7f'
	        )
	    )
	)
	fig = go.Figure(data=traces, layout=layout)
	pltly.plot(fig,filename=graph_title+'.html')

	return


#regex expressions
homo_regex= r'f[a]*g\w{0,}'
gay_regex = r'g[a]*y\w{0,}'
bitch_regex = r'b[i]*tch\w{0,}|\sho[es]*\s'
rape_regex = r'rap[ie]\w{0,}'
nigga_regex = r'nigg[a]\w{0,}'

songs_number_ref = make_reference_dict('tylerthecreator',regex=homo_regex)
ref_df,ttc_homo_grouped_df = create_references_df(songs_number_ref)
simple_bar_from_df(
	ttc_homo_grouped_df,
	graph_title='Tyler The Creator and His Slurs Over The Years',
	x_data='year',
	y_data='avg ref',
	x_title='Year',
	y_title='# of Homophobic References per Song'
	)



songs_number_ref = make_reference_dict('drake',regex=bitch_regex)
ref_df,drake_grouped_df = create_references_df(songs_number_ref)
# simple_bar_from_df(
# 	drake_grouped_df,
# 	graph_title='Drakes Misogony: An Explorations',
# 	x_data='year',
# 	y_data='avg ref',
# 	x_title='Year',
# 	y_title='Average # of Bitch or Ho[e] References'
# 	)



songs_number_ref = make_reference_dict('jcole',regex=bitch_regex)
ref_df,cole_grouped_df = create_references_df(songs_number_ref)
# simple_bar_from_df(
# 	cole_grouped_df,
# 	graph_title='J. Cole\'s Misogony: An Explorations',
# 	x_data='year',
# 	y_data='avg ref',
# 	x_title='Year',
# 	y_title='Average # of Bitch or Ho[e] References'
# 	)

songs_number_ref = make_reference_dict('tylerthecreator',regex=bitch_regex)
ref_df,ttc_grouped_df = create_references_df(songs_number_ref)
# simple_bar_from_df(
# 	ttc_grouped_df,
# 	graph_title='Tyler\'s Misogony: An Explorations',
# 	x_data='year',
# 	y_data='avg ref',
# 	x_title='Year',
# 	y_title='Average # of Bitch or Ho[e] References'
# 	)

# songs_number_ref = make_reference_dict('cardi-b',regex=bitch_regex)
# ref_df,cardi_grouped_df = create_references_df(songs_number_ref)

# comp_dfs = {}
# comp_dfs['Tyler The Creator'] = ttc_grouped_df
# comp_dfs['J. Cole'] = cole_grouped_df
# comp_dfs['Drake'] = drake_grouped_df
# comp_dfs['Cardi B.'] = cardi_grouped_df

# comparative_bar_from_df(
# 	comp_dfs,
# 	graph_title='Bitches & Hoes',
# 	x_data='year',
# 	y_data='avg ref',
# 	x_title='Year',
# 	y_title='Bitch/Hoe References per Song'
# 	)


# songs_number_ref = make_reference_dict('logic',regex=nigga_regex)
# ref_df,logic_nig_grouped_df = create_references_df(songs_number_ref)

# songs_number_ref = make_reference_dict('jcole',regex=nigga_regex)
# ref_df,cole_nig_grouped_df = create_references_df(songs_number_ref)

# songs_number_ref = make_reference_dict('kendricklamar',regex=nigga_regex)
# ref_df,kdot_nig_grouped_df = create_references_df(songs_number_ref)

# songs_number_ref = make_reference_dict('kehlani',regex=nigga_regex)
# ref_df,kehlani_nig_grouped_df = create_references_df(songs_number_ref)

# songs_number_ref = make_reference_dict('drake',regex=nigga_regex)
# ref_df,drake_nig_grouped_df = create_references_df(songs_number_ref)

# songs_number_ref = make_reference_dict('tylerthecreator',regex=nigga_regex)
# ref_df,ttc_nig_grouped_df = create_references_df(songs_number_ref)

# songs_number_ref = make_reference_dict('cardi-b',regex=nigga_regex)
# ref_df,cardi_nig_grouped_df = create_references_df(songs_number_ref)

# songs_number_ref = make_reference_dict('fatjoe',regex=nigga_regex)
# ref_df,fatjoe_nig_grouped_df = create_references_df(songs_number_ref)

# comp_nig_dfs = {}
# comp_nig_dfs['Logic'] = logic_nig_grouped_df
# comp_nig_dfs['J. Cole'] = cole_nig_grouped_df
# comp_nig_dfs['Drake'] = drake_nig_grouped_df

# comp_nig_dfs['Tyler The Creator'] = ttc_nig_grouped_df
# comp_nig_dfs['Kehlani'] = kehlani_nig_grouped_df
# comp_nig_dfs['Kendrick Lamar'] = kdot_nig_grouped_df
# comp_nig_dfs['Cardi B.'] = cardi_nig_grouped_df
# comp_nig_dfs['Fat Joe'] = fatjoe_nig_grouped_df

# comparative_bar_from_df(
# 	comp_nig_dfs,
# 	graph_title='Nigga What Nigga Who',
# 	x_data='year',
# 	y_data='avg ref',
# 	x_title='Year',
# 	y_title='Nigga References per Song'
# 	)

