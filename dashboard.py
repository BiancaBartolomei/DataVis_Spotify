
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine
from datetime import date as dt
import dash_table

engine = create_engine('postgres://luismalta:123@localhost:5432/spotify_db')

# engine = create_engine('postgres://biancabartolomei:19972015@localhost:5432/spotify')

df_features_track = pd.read_sql_query('select * from spotify_db.features_track',con=engine)
df_features_artist= pd.read_sql_query('select * from spotify_db.features_artist',con=engine)
df_features_playlist = pd.read_sql_query('select * from spotify_db.features_playlist',con=engine)
df_top10_track = pd.read_sql_query("select * from spotify_db.top10_tracks('2018-10-23 00:00:00.000000')",con=engine)
df_top10_artist = pd.read_sql_query("select * from spotify_db.top10_artist('2018-10-23 00:00:00.000000')",con=engine)




external_stylesheets = ['assets/material.css']
external_scripts = ['assets/material.js']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)
server = app.server

app.config.suppress_callback_exceptions = True

app.title = "SPOTIFY DASHBOARD"

def update_top10_track_dataframe(data):
    count= 0
    result = pd.DataFrame(columns=['Track','Popularidade'])
    while(count < 10):
        for i in df_top10_track['data_popularidade']:
            if data == i:
                print(i)


def update_dropdown_features_track():
    opt_track= []
    tracks = []
    for track in df_features_track['track_name']:

        if track not in tracks:
            a = {'label':track, 'value':track}
            opt_track.append(a)
            tracks.append(track)


    return sorted(opt_track, key=lambda k: k['label'])

def update_dropdown_features_artist():
    opt_artist= []
    artists = []
    for artist in df_features_artist['artist_name']:

        if artist not in artists:
            a = {'label':artist, 'value':artist}
            opt_artist.append(a)
            artists.append(artist)

    return sorted(opt_artist, key=lambda k: k['label'])

def update_dropdown_features_playlist():
    opt_playlist= []
    playlists = []
    for playlist in df_features_playlist['playlist_name']:

        if playlist not in playlists:
            a = {'label':playlist, 'value':playlist}
            opt_playlist.append(a)
            playlists.append(playlist)


    return sorted(opt_playlist, key=lambda k: k['label'])

# ----------------------------------------------------------------------------------------------------------------------
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Header([
        html.Div([
            html.Span(['Spotify Dashboard'], className='mdl-layout-title'),
            html.Div([], className='mdl-layout-spacer')
        ], className='mdl-layout__header-row')
    ], className='mdl-layout__header mdl-layout__header--scroll'),

    html.Div([
        html.Span(['Menu'], className='mdl-layout-title'),
        html.Nav([
            dcc.Link('Top 10', href='/top-10', className='mdl-navigation__link'),
            dcc.Link('Análise de grupos', href='page-grupos', className='mdl-navigation__link'),
            dcc.Link('Análise de Features', href='page-features', className='mdl-navigation__link'),
            dcc.Link('Análise de popularidade', href='/page-popularidade', className='mdl-navigation__link'),
        ], className='mdl-navigation')
    ], className='mdl-layout__drawer'),

    # --------- Main --------------
    html.Main([
        html.Div(id='page-main', className='page-content'),
    ], className='mdl-layout__content'),

], className='mdl-layout mdl-js-layout')


# PAGE FEATURES

page_features = html.Div([

                    html.Div([
                        html.Div([
                           html.H1(["Análise de features"],className='titulo-texto')
                        ],className='')

                    ],className='mdl-cell mdl-cell--12-col'),

                    # Feature Track
                    html.Div([
                        html.Div([
                            html.Div([

                                html.Div([
                                    html.H6(['Track'], className='titulo-grafico')
                                ], className='mdl-cell mdl-cell--12-col'),

                                html.Div([], className='mdl-cell mdl-cell--3-col'),

                                html.Div([
                                    dcc.Dropdown(
                                        id='dropdown-feature-track',
                                        options=update_dropdown_features_track(),
                                        multi=False,
                                        value=""
                                    ),
                                ], className='mdl-cell mdl-cell--6-col'),

                                html.Div([], className='mdl-cell mdl-cell--3-col'),

                                html.Div([
                                    dcc.Graph(
                                        id='radar-feature-track',
                                        figure={
                                            'data': [go.Scatterpolar(
                                                r=[0,0,0,0,0,0,0],
                                                theta=['Liveness', 'Speechness', 'Valence', 'Energy', 'Acousticness',
                                                       'Instrumentalness', 'Dancebility'],
                                                fill='toself',
                                                marker=dict(color='#4101c1')
                                            )],
                                            'layout': [go.Layout(
                                                polar=dict(
                                                    radialaxis=dict(
                                                        visible=True,
                                                        range=[0.0, 1.0]
                                                    )
                                                ),
                                                showlegend=True
                                            )]

                                        }
                                    ),
                                ], className='mdl-cell mdl-cell--12-col'),

                            ], className='mdl-grid')
                        ], className='card'),

                    ], className='mdl-cell mdl-cell--4-col'),

                    # Feature Artist
                    html.Div([
                        html.Div([
                            html.Div([

                                html.Div([
                                    html.H6(['Artist'], className='titulo-grafico'),
                                ], className='mdl-cell mdl-cell--12-col'),


                                html.Div([], className='mdl-cell mdl-cell--3-col'),

                                html.Div([
                                    dcc.Dropdown(
                                        id='dropdown-feature-artist',
                                        options=update_dropdown_features_artist(),
                                        multi=False,
                                        value=""
                                    ),
                                ], className='mdl-cell mdl-cell--6-col'),

                                html.Div([], className='mdl-cell mdl-cell--3-col'),

                                html.Div([
                                    dcc.Graph(
                                        id='radar-feature-artist',
                                        figure={
                                            'data': [go.Scatterpolar(
                                                r=[0,0,0,0,0,0,0],
                                                theta=['Liveness', 'Speechness', 'Valence', 'Energy', 'Acousticness',
                                                       'Instrumentalness', 'Dancebility'],
                                                fill='toself',
                                                marker=dict(color='#4101c1')
                                            )],
                                            'layout': [go.Layout(
                                                polar=dict(
                                                    radialaxis=dict(
                                                        visible=True,
                                                        range=[0, 1]
                                                    )
                                                ),
                                                showlegend=True
                                            )]

                                        }
                                    ),
                                ], className='mdl-cell mdl-cell--12-col'),


                            ], className='mdl-grid')
                        ], className='card'),
                    ],className='mdl-cell mdl-cell--4-col'),

                        # Feature Playlist
                        html.Div([
                            html.Div([
                                html.Div([

                                    html.Div([
                                        html.H6(['Playlist'], className='titulo-grafico')
                                    ], className='mdl-cell mdl-cell--12-col'),

                                    html.Div([], className='mdl-cell mdl-cell--3-col'),

                                    html.Div([
                                        dcc.Dropdown(
                                            id='dropdown-feature-playlist',
                                            options=update_dropdown_features_playlist(),
                                            multi=False,
                                            value="",
                                        ),
                                    ], className='mdl-cell mdl-cell--6-col'),

                                    html.Div([], className='mdl-cell mdl-cell--3-col'),

                                    html.Div([
                                        dcc.Graph(
                                            id='radar-feature-playlist',
                                            figure={
                                                'data': [go.Scatterpolar(
                                                    r=[0,0,0,0,0,0,0],
                                                    theta=['Liveness', 'Speechness', 'Valence', 'Energy',
                                                           'Acousticness',
                                                           'Instrumentalness', 'Dancebility'],
                                                    fill='toself',
                                                    marker=dict(color='#4101c1')
                                                )],
                                                'layout': [go.Layout(
                                                    polar=dict(
                                                        radialaxis=dict(
                                                            visible=True,
                                                            range=[0, 1]
                                                        )
                                                    ),
                                                    showlegend=True
                                                )]

                                            }
                                        ),
                                    ],className='mdl-cell mdl-cell--12-col'),


                                ], className='mdl-grid')

                            ], className='card'),

                    ], className='mdl-cell mdl-cell--4-col'),

            ], className= 'mdl-grid')

@app.callback(dash.dependencies.Output('radar-feature-track', 'figure'),
              [dash.dependencies.Input('dropdown-feature-track', 'value')])
def display_page(track_selected):
    temp = df_features_track
    traces = []
    layout_trace = []

    if track_selected:
        temp = df_features_track.loc[df_features_track['track_name']==track_selected]

        traces.append(go.Scatterpolar(
            r=[temp['track_liveness'].values[0], temp['track_speechness'].values[0],
               temp['track_valence'].values[0], temp['track_energy'].values[0],
               temp['track_acousticness'].values[0],
               temp['track_instrumentalness'].values[0],
               temp['track_dancebility'].values[0]],
            theta=['Liveness', 'Speechness', 'Valence', 'Energy', 'Acousticness',
                   'Instrumentalness', 'Dancebility'],
            fill='toself',
            marker=dict(color='#4101c1'),

        ))

        layout_trace.append(
            go.Layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0.0, 1.0]
                    )
                ),
                showlegend=True
            )
        )
    else:
        traces.append(go.Scatterpolar(
            r=[0,0,0,0,0,0,0],
            theta=['Liveness', 'Speechness', 'Valence', 'Energy', 'Acousticness',
                   'Instrumentalness', 'Dancebility'],
            fill='toself',
            marker=dict(color='#4101c1'),

        ))

        layout_trace.append(
            go.Layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0.0, 1.0]
                    )
                ),
                showlegend=True
            )
        )

    return {
        'data': traces,
        'layout': layout_trace
    }

@app.callback(dash.dependencies.Output('radar-feature-artist', 'figure'),
              [dash.dependencies.Input('dropdown-feature-artist', 'value')])
def display_page(artist_selected):
    temp = df_features_artist

    traces = []
    layout_trace = []

    if artist_selected:

        temp = df_features_artist.loc[df_features_artist['artist_name']==artist_selected]




        traces.append(go.Scatterpolar(
            r=[temp['track_liveness'].values[0], temp['track_speechness'].values[0],
               temp['track_valence'].values[0], temp['track_energy'].values[0],
               temp['track_acousticness'].values[0],
               temp['track_instrumentalness'].values[0],
               temp['track_dancebility'].values[0]],
            theta=['Liveness', 'Speechness', 'Valence', 'Energy', 'Acousticness',
                   'Instrumentalness', 'Dancebility'],
            fill='toself',
            marker=dict(color='#4101c1')
        ))

        layout_trace.append(
            go.Layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0.0, 1.0]
                    )
                ),
                showlegend=True
            )
        )

    else :
        traces.append(go.Scatterpolar(
            r=[0,0,0,0,0,0,0],
            theta=['Liveness', 'Speechness', 'Valence', 'Energy', 'Acousticness',
                   'Instrumentalness', 'Dancebility'],
            fill='toself',
            marker=dict(color='#4101c1')
        ))

        layout_trace.append(
            go.Layout(
                polar=dict(
                    radialaxis=dict(
                        visible=False,
                        range=[0, 1]
                    )
                ),
                showlegend=True
            )
        )

    return {
        'data': traces,
        'layout': layout_trace
    }

@app.callback(dash.dependencies.Output('radar-feature-playlist', 'figure'),
              [dash.dependencies.Input('dropdown-feature-playlist', 'value')])
def display_page(playlist_selected):
    temp = df_features_playlist
    traces = []
    layout_trace = []

    if playlist_selected:
        temp = df_features_playlist.loc[df_features_playlist['playlist_name']==playlist_selected]





        traces.append(go.Scatterpolar(
            r=[temp['track_liveness'].values[0], temp['track_speechness'].values[0],
               temp['track_valence'].values[0], temp['track_energy'].values[0],
               temp['track_acousticness'].values[0],
               temp['track_instrumentalness'].values[0],
               temp['track_dancebility'].values[0]],
            theta=['Liveness', 'Speechness', 'Valence', 'Energy', 'Acousticness',
                   'Instrumentalness', 'Dancebility'],
            fill='toself',
            marker=dict(color='#4101c1')
        ))

        layout_trace.append(
            go.Layout(
                polar=dict(
                    radialaxis=dict(
                        visible=False,
                        range=[0, 1]
                    )
                ),
                showlegend=True
            )
        )

    else:
        traces.append(go.Scatterpolar(
            r=[0,0,0,0,0,0,0],
            theta=['Liveness', 'Speechness', 'Valence', 'Energy', 'Acousticness',
                   'Instrumentalness', 'Dancebility'],
            fill='toself',
            marker=dict(color='#4101c1')
        ))

        layout_trace.append(
            go.Layout(
                polar=dict(
                    radialaxis=dict(
                        visible=False,
                        range=[0, 1]
                    )
                ),
                showlegend=True
            )
        )

    return {
        'data': traces,
        'layout': layout_trace
    }


# ----------------------------------------------------------------------------------------------------------------------

# PAGE TOP 10

page_top_10 =  html.Div([

    html.Div([
        dcc.DatePickerSingle(
            id='date-top10',
            date=dt(2018, 11, 1)
        )
    ], className='mdl-cell mdl-cell--12-col'),



    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3(['Track'])
                ], className='card')
            ],className='mdl-cell mdl-cell--6-col'),
            html.Div(['Artist'],className='mdl-cell mdl-cell--6-col'),

            html.Div([
                html.Table(
                    # Header
                    [html.Tr(
                        [html.Th(col, className='mdl-data-table__cell--non-numeric') for col in
                         df_top10_track.columns])] +

                    # Body
                    [html.Tr([
                        html.Td(df_top10_track.iloc[i][col], className='mdl-data-table__cell--non-numeric') for col
                        in
                        df_top10_track.columns
                    ]) for i in range(min(len(df_top10_track), 10))], className='mdl-data-table mdl-js-data-table'
                ),
            ], className='mdl-cell mdl-cell--6-col'),

            html.Div([
                html.Table(
                    # Header
                    [html.Tr(
                        [html.Th(col, className='mdl-data-table__cell--non-numeric') for col in
                         df_top10_artist.columns])] +

                    # Body
                    [html.Tr([
                        html.Td(df_top10_artist.iloc[i][col], className='mdl-data-table__cell--non-numeric') for col
                        in
                        df_top10_artist.columns
                    ]) for i in range(min(len(df_top10_artist), 10))], className='mdl-data-table mdl-js-data-table'
                ),
            ], className='mdl-cell mdl-cell--6-col'),

        ],className='mdl-grid')
    ], className='mdl-cell mdl-cell--12-col', id='top10_page')
            ], className='mdl-grid')
@app.callback(dash.dependencies.Output('top10_page', 'children'),
              [dash.dependencies.Input('date-top10', 'date')])
def display_page(data):

    query = data + ' 00:00:00.000000'
    df_top10_track = pd.read_sql_query('select * from spotify_db.top10_tracks(' + "'" + query + "'"+')',
                                       con=engine)
    df_top10_artist = pd.read_sql_query('select * from spotify_db.top10_artist(' + "'" + query + "'"+')',
                                       con=engine)

    return html.Div([

            html.Div([
                html.Div([], className='mdl-cell mdl-cell--1-col'),
                    html.Div([
                        html.H3(['Track #1: ' + df_top10_track['track'][0]], className='titulo-texto')
                    ], className='card')
                ],className='mdl-cell mdl-cell--4-col'),
            html.Div([],className='mdl-cell mdl-cell--1-col'),

            html.Div([
                html.Div([], className='mdl-cell mdl-cell--1-col'),
                    html.Div([
                        html.H3(['Artist #1: ' + df_top10_artist['artist'][0]], className='titulo-texto')
                    ], className='card')
                ], className='mdl-cell mdl-cell--4-col'),
            html.Div([], className='mdl-cell mdl-cell--1-col'),

            html.Div([
                html.Table(
                    # Header
                    [html.Tr(
                        [html.Th(col, className='mdl-data-table__cell--non-numeric') for col in
                         df_top10_track.columns])] +

                    # Body
                    [html.Tr([
                        html.Td(df_top10_track.iloc[i][col], className='mdl-data-table__cell--non-numeric') for col
                        in
                        df_top10_track.columns
                    ]) for i in range(min(len(df_top10_track), 10))], className='mdl-data-table mdl-js-data-table'
                ),
            ], className='mdl-cell mdl-cell--6-col'),

            html.Div([
                html.Table(
                    # Header
                    [html.Tr(
                        [html.Th(col, className='mdl-data-table__cell--non-numeric') for col in
                         df_top10_artist.columns])] +

                    # Body
                    [html.Tr([
                        html.Td(df_top10_artist.iloc[i][col], className='mdl-data-table__cell--non-numeric') for col
                        in
                        df_top10_artist.columns
                    ]) for i in range(min(len(df_top10_artist), 10))], className='mdl-data-table mdl-js-data-table'
                ),
            ], className='mdl-cell mdl-cell--6-col'),

        ],className='mdl-grid')


# ----------------------------------------------------------------------------------------------------------------------
 # ----------------------------------------------------------------------------------------------------------------------
# PAGE FEATURES

df_artist_genre = pd.read_sql_query('select * from spotify_db.musicas_por_genero', con=engine)
colors_artist_genre = ['#110014',                       '#220128',
                       '#33013c',
                       '#440250',
                       '#550264',
                       '#660278',
                       '#77038c',
                       '#8803a0',
                       '#9904b4',
                       '#ab04c8',
                       '#bc04dc',
                       '#cd05f0',
                       '#d70ffa',
                       '#da23fb',
                       '#de37fb',
                       '#e040fb',
                       '#e45ffc',
                       '#e873fc',
                       '#eb87fd',
                       '#ee9bfd']
df_explicit_genre = pd.read_sql_query('select * from spotify_db.explicit_genre', con=engine)
df_duration_track = pd.read_sql_query('select * from spotify_db.duration_track', con=engine)

import numpy as np
group_1 = np.percentile(df_duration_track['track_duration'], 25)
group_2 = np.percentile(df_duration_track['track_duration'], 50)
group_3 = np.percentile(df_duration_track['track_duration'], 75)


def group_selection():
    group_count_1 = 0
    group_count_2 = 0
    group_count_3 = 0
    group_count_4 = 0

    for t in df_duration_track['track_duration']:
        if t < group_1:
            group_count_1 = group_count_1 + 1

        elif t < group_2 and t > group_1:
            group_count_2 = group_count_2 + 1

        elif t < group_3 and t > group_2:
            group_count_3 = group_count_3 + 1

        elif t > group_3:
            group_count_4 = group_count_4 + 1

    return [group_count_1, group_count_2, group_count_3, group_count_4]


page_grupos = html.Div([

                # html.Div([
                # ], className='mdl-cell mdl-cell--1-col'),
                html.Div([
                    # html.Div([
                        html.H1(['Análises de Grupo'], className='titulo-grupos')
                    # ], className='titulo-grupos'),
                ], className='mdl-cell mdl-cell--3-col'),
                html.Div([
                ], className='mdl-cell mdl-cell--1-col'),

                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='pizza-artist-genre',
                            figure={
                                'data': [go.Pie(
                                    labels=df_artist_genre['artist_genre'][:20],
                                    values=df_artist_genre['quant'][:20],
                                    textinfo='value',
                                    hole=.4,
                                    marker=dict(colors=colors_artist_genre),
                                )],
                                'layout': {
                                    'title': 'Quantidade de artistas por gênero musical',
                                    'font': {'family': 'Roboto',
                                             'size': 12,
                                             'color': '#646168'},
                                }
                            },

                        ),
                    ], className='card-2'),
                ], className='mdl-cell mdl-cell--8-col'),



                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='pizza-explicit-genre',
                            figure={
                                'data': [go.Pie(
                                    labels=df_explicit_genre['artist_genre'][:20],
                                    values=df_explicit_genre['quant'][:20],
                                    textinfo='value',
                                    hole=.4,
                                    marker=dict(colors=colors_artist_genre),
                                )],
                                'layout': {
                                    'title': 'Quantidade de músicas explícitas por gênero musical',
                                    'font': {'family': 'Roboto',
                                             'size': 15,
                                             'color': '#646168'}
                                }
                            }
                        ),
                    ], className='card'),
                ], className='mdl-cell mdl-cell--7-col'),

                html.Div([
                    html.Div([
                        dcc.Graph(
                            id='pizza-duration-track',
                            figure={
                                'data': [go.Pie(
                                    labels=['0', '1', '2', '3'],
                                    values=group_selection(),
                                    textinfo='value',
                                    hole=.4,
                                    marker=dict(colors=colors_artist_genre),
                                )],
                                'layout': {
                                    'title': 'Quantidade de músicas pela média de duração',
                                    'font': {'family': 'Roboto',
                                             'size': 15,
                                             'color': '#646168'},
                                }
                            },
                        ),
                    ], className='card')
                ], className='mdl-cell mdl-cell--5-col'),



            ], className='mdl-grid')




# Callback Paginas
@app.callback(dash.dependencies.Output('page-main', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-features':
        return page_features
    elif pathname == '/page-grupos':
        return page_grupos
    # elif pathname == '/page-popularidade':
    #     return page_popularidade
    if pathname == '/page-top-10':
        return page_top_10
    else:
        return page_top_10


if __name__ == '__main__':
    app.run_server(debug=True)
