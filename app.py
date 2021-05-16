# -*- coding: utf-8 -*-


# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import plotly.express as px
from datetime import datetime

from pybaseball import statcast
from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup
from pybaseball import playerid_reverse_lookup
from pybaseball import pitching_stats

import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Saving statcast dataframe 
#statcast_df = statcast(start_dt = '2008-01-01', end_dt = '2021-05-31')
#statcast_df.to_csv(r'/Users/bryankim/Desktop/Spring2021/stat430/final/statcast_df.csv', index = False, header = True)
statcast_df = pd.read_csv('statcast_df.csv')

# change 'game_date' column to datetime format
statcast_df['game_date'] = pd.to_datetime(statcast_df['game_date'], format="%Y-%m-%d")

###########################################
yr = ([i for i in range (2008, 2022)])
change_dict = {'SL' : 'Slider', 'CH' : 'Changeup', 'SI' : 'Sinker', 'PO' : 'Put Out','FF' : 'Four-Seam Fastball', 'FC' : 'Cutter', 'CU' : 'Curveball','KC' : 'Knuckle-curve', 'FS' : 'Splitter', 'EP' : 'Eephus', 'FA' : 'Four-Seam Fastball', 'CS' : 'Slow Curve', 'KN' : 'Knuckleball', 'SC' : 'Screwball', 'FT' : 'Two-Seam Fastball'}


app.layout = html.Div([

	html.H1(children='Pitch Arsenal'),

	html.Div(children='''
        Author: Jae Hyeon Kim, jkim554
    '''),

	html.Div(children='''
        A web application to view pitch-type signatures, by frequency, speed, and break. 
        Only showing pitchers with around 100 pitches.
    '''),

    html.Hr(),

    html.Label("SEASON"),
    dcc.Dropdown(
        id='season_column',
        options=[{'label': i, 'value': i} for i in yr],
        style=dict( width='48%'),
        value='2008'
    ),

    html.Hr(),

    html.Label("RHP"),
    dcc.Dropdown(
        id='rhp_name',
        # options=[ ],
        style=dict(width='48%'),
    ),

    html.Hr(),

    html.Label("LHP"),
    dcc.Dropdown(
        id='lhp_name',
        # options=[ ],
        value = 'Affeldt, Jeremy',
        style=dict(width='48%'),
    ),

    html.Hr(),

    # html.Div(id = "output-name"),

    dcc.Graph(id="bar-chart"),

    dcc.Graph(id="box-plot"),

    dcc.Graph(id="scatter-plot")

])

###########################################
@app.callback(
    Output('rhp_name', 'options'),
    Input('season_column', 'value')
    )

def update_rhp(yr_val):
    star_dt = str(yr_val) + '-01-01'
    en_dt = str(yr_val)  + '-12-31'
    df_1 = pitching_stats(yr_val, qual = 10)
    idfg = df_1['IDfg'].tolist()
    playername = playerid_reverse_lookup(idfg, key_type='fangraphs')
    statid = playername['key_mlbam'].tolist()
    df = statcast_df.loc[(statcast_df['game_date'] >= star_dt) & (statcast_df['game_date'] <= en_dt)]
    df = statcast_df.loc[(statcast_df['pitcher'].isin(statid)) & (statcast_df['p_throws'] == 'R')]
    df = df['player_name'].unique()
    dff = sorted(df)
    return [{'label': i, 'value': i} for i in dff]


@app.callback(
    Output('lhp_name', 'options'),
    Input('season_column', 'value')
    )

def update_lhp(yr_val):
    star_dt = str(yr_val) + '-01-01'
    en_dt = str(yr_val) + '-12-31'
    df_1 = pitching_stats(yr_val, qual = 10)
    idfg = df_1['IDfg'].tolist()
    playername = playerid_reverse_lookup(idfg, key_type='fangraphs')
    statid = playername['key_mlbam'].tolist()
    df = statcast_df.loc[(statcast_df['game_date'] >= star_dt) & (statcast_df['game_date'] <= en_dt)]
    df = statcast_df.loc[(statcast_df['pitcher'].isin(statid)) & (statcast_df['p_throws'] == 'L')]
    df = df['player_name'].unique()
    dff1 = sorted(df)
    return [{'label': i, 'value': i} for i in dff1]

@app.callback(
	Output('rhp_name', 'value'),
	Output('lhp_name', 'value'),
	Input('rhp_name', 'value'),
	Input('lhp_name', 'value'),
	Input('season_column', 'value'),
	Input('lhp_name', 'options')
	)

def circular_callback(rhp_val, lhp_val, yr_val, lhp_option):
	ctx = dash.callback_context
	input_id = ctx.triggered[0]["prop_id"].split(".")[0]
	if input_id == 'season_column':
		return None, lhp_option[0]['value']
	if input_id == 'rhp_name':
		lhp_val = None
	else:
		rhp_val = None
	return rhp_val, lhp_val


@app.callback(
    Output("bar-chart", "figure"),
    Output("box-plot", "figure"),
    Output("scatter-plot", "figure"),
    Input("lhp_name", "value"),
    Input("rhp_name", "value"),
    Input("season_column", "value"))

def update_bar_chart(lhp_pitcher,rhp_pitcher,yr_val):
	if lhp_pitcher is None and rhp_pitcher is None:
		raise PreventUpdate
	if rhp_pitcher is None:
		name = lhp_pitcher
	else:
		name = rhp_pitcher
	star_dt = str(yr_val) + '-01-01'
	en_dt = str(yr_val) + '-12-31'
	df = statcast_df.loc[(statcast_df['game_date'] >= star_dt) & (statcast_df['game_date'] <= en_dt)]
	id_num = df.loc[df['player_name'] == name]['pitcher'].unique()
	pitcher_df = statcast_pitcher(star_dt,en_dt, id_num[0])
	pitcher_df.replace({'pitch_type' : change_dict}, inplace = True)
	
	grouped1 = pitcher_df.groupby(['pitch_name']).agg({'game_date' : 'count'})
	grouped1['Pitch Type Frequency %'] = round((grouped1['game_date'] / sum(grouped1['game_date']) * 100))
	grouped1 = grouped1.sort_values(by = 'Pitch Type Frequency %', ascending = False)
	grouped1 = grouped1.reset_index()

	grouped2 = pitcher_df.groupby(['pitch_name','release_speed']).agg({
		'pitch_type': 'count'
		})
	grouped2 = grouped2.sort_values(by = 'pitch_type', ascending = False)
	grouped2 = grouped2.reset_index()


	grouped3 = pitcher_df.groupby(['pitch_name']).agg({
		'pfx_x': np.mean,
		'pfx_z': np.mean,
		'pitch_type': 'count'
		})
	grouped3 = grouped3.sort_values(by = 'pitch_type', ascending = False)
	grouped3 = grouped3.reset_index()


	fig1 = px.bar(grouped1, x = 'pitch_name', y = 'Pitch Type Frequency %',
		color = 'pitch_name',
		title = "Pitch Type Frequency vs. Type of Pitch Thrown",
		labels = {
			"pitch_name" : "Type of Pitch Thrown",
		}
		)

	fig2 = px.box(grouped2, x = 'pitch_name', y = 'release_speed', 
		color = 'pitch_name', 
		category_orders={'pitch_name': list(grouped1['pitch_name'])},
		title = "Release Speed vs. Type of Pitch Thrown",
		labels = {
			"pitch_name" : "Type of Pitch Thrown",
			"release_speed" : "Release Speed (mph)"
			}
		)

	fig3 = px.scatter(x = grouped3['pfx_x']*12, y=grouped3['pfx_z']*12,
		color = grouped3['pitch_name'],
		category_orders={'pitch_name': list(grouped1['pitch_name'])},
		size = grouped3['pitch_type'], size_max = 50,
		labels = {
			"x" : "Horizontal Break (inches)",
			"y" : "Downward Vertical Break (inches)"
		},
		title = "Downward Vertical Break vs. Horizontal Break of Pitch"
		)
	fig3.update_layout(
		xaxis = dict(
			tickmode = 'array',
			tickvals = list(range(-30,31,6)),
			ticktext = ["{:01d}\"".format(x) for x in (list(range(-30,31,6)))],
			dtick = 6,
			nticks = 11,
			zeroline = False,
			showgrid = False
			),
		yaxis = dict(
			tickmode = 'linear',
			zeroline = False,
			showgrid = False,
			dtick = 6
			))
	
	fig3.update_yaxes(
		scaleanchor = "x",
		scaleratio = 1,
		range=[-30,30],  # sets the range of xaxis
		constrain="domain",  # meanwhile compresses the xaxis by decreasing its "
  )
	fig3.update_xaxes(
		range=[-30,30],  # sets the range of xaxis
		constrain="domain",  # meanwhile compresses the xaxis by decreasing its "domain"
)
	return fig1, fig2, fig3


if __name__ == '__main__':
    app.run_server(debug=True)