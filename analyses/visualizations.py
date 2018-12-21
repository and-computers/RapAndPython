#!/usr/bin/env python2

"""
functions just to help with visualization
"""
import pandas as pd
import plotly.offline as pltly
import plotly.graph_objs as go

def create_pie_chart(labels,values,colors):

	trace = go.Pie(labels=labels, values=values,
	               hoverinfo='label+percent', 
	               textfont=dict(size=20),
	               marker=dict(colors=colors, 
	                           line=dict(color='#000000', width=2)))

	pltly.plot([trace], filename='{}_pie_chart.html'.format(''.join(labels)))

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