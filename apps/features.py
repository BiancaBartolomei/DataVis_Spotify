# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine
import dash

from app import app

# engine = create_engine('postgres://luismalta:123@localhost:5432/spotify_db')
engine = create_engine('postgres://biancabartolomei:19972015@localhost:5432/spotify')

df_features_track = pd.read_sql_query('select * from spotify_db.features_track',con=engine)
df_features_artist= pd.read_sql_query('select * from spotify_db.features_artist',con=engine)
df_features_playlist = pd.read_sql_query('select * from spotify_db.features_playlist',con=engine)


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


page_features = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.H6(['Análise de features'], className='mdl-cell mdl-cell--12-col'),
                html.Hr([], className='mdl-cell mdl-cell--12-col'),
                html.Div([], className='mdl-cell mdl-cell--12-col'),
                    # html.Div([
                    #     html.Div([
                    #        html.H1(["Análise de features"], className='titulo-texto')
                    #     ], className='')
                    # ], className='mdl-cell mdl-cell--12-col'),

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
                                                r=[0, 0, 0, 0, 0, 0, 0],
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
                    ], className='mdl-cell mdl-cell--4-col'),

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
                                                r=[0, 0, 0, 0, 0, 0, 0],
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
        ], className='card')
    ], className='mdl-cell mdl-cell--12-col', id='card-ranking'),
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

