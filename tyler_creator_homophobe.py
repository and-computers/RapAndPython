#!/usr/bin/env python2

import os
import re

import pandas as pd
import numpy as np

import plotly.offline as pltly
import plotly.graph_objs as go

songs_number_ref = {}
for root,dirs,fnameslist in os.walk("webscrape/scraped_data"):
	if 'tyler_the_creator' in root:
		for fname in fnameslist:
			with open(os.path.join(root,fname)) as lyrics:
				alltxt = lyrics.readlines()
				found_homo = re.findall(r'fa[g]+', str(alltxt))
				found_nig = re.findall(r'ga[y]+', str(alltxt))
				found_bitch = re.findall(r'[b]+[i]+[t]+[c]+[h]+', str(alltxt))
				# print fname
				# print found_homo
				# print found_nig
				# print found_bitch
				num_homo = len(found_homo)
				songs_number_ref[fname] = (found_homo,num_homo)

print songs_number_ref




traceFag = go.Scatter(x=df['PER'],y=df['Guaranteed'],mode='line',name='Fag',
	text=df['Player'],
	marker=dict(
        size=16,
        color = df['Win Percentage'], #set color equal to a variable
        colorbar=dict(title='Team Win Percentage (%)'),
        colorscale='Viridis',
        showscale=True
    ))
traceFaggot = go.Scatter(x=df['BPM'],y=df['Guaranteed'],mode='line',name='Faggot',
		text=df['Player'],
	marker=dict(
        size=16,
        color = df['Win Percentage'], #set color equal to a variable
        colorbar=dict(title='Team Win Percentage (%)'),
        colorscale='Viridis',
        showscale=True
    ))


layout = go.Layout(
    title='Tyler The Creator and His Slurs Over The Years',
    xaxis=dict(
        title='Year',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),
    yaxis=dict(
        title='Homophobic (?) References',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
fig = go.Figure(data=[traceFag,traceFaggot], layout=layout)


# data = [tracePER]

pltly.plot(fig)