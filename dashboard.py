
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine
from datetime import date as dt



engine = create_engine('postgres://luismalta:123@localhost:5432/spotify_db')

df_features_track = pd.read_sql_query('select * from spotify_db.features_track',con=engine)
df_features_artist= pd.read_sql_query('select * from spotify_db.features_artist',con=engine)
df_features_playlist = pd.read_sql_query('select * from spotify_db.features_playlist',con=engine)



external_stylesheets = ['assets/material.css']
external_scripts = ['assets/material.js']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)
server = app.server

app.config.suppress_callback_exceptions = True

app.title = "SPOTIFY POPULARITY DATABASE"

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
app.layout = html.Div(children=[

    dcc.Location(id='url', refresh=False),
# ------------ Header --------------------
    html.Div(children=[
        html.Header([
            html.Div([
                html.Span(children='Spotify Dashboard', className='mdl-layout-title'),

                html.Div([

                ],className='mdl-layout-spacer'),

                html.Nav([

                ], className='mdl-navigation mdl-layout--large-screen-only')

            ], className='mdl-layout__header-row')
        ], className='mdl-layout__header'),

        html.Div([
            html.Span(children='Menu', className='mdl-layout-title'),

            html.Nav([
                dcc.Link('Top 10', href='/top-10', className='mdl-navigation__link'),
                dcc.Link('Análise de grupos', href='page-grupos', className='mdl-navigation__link'),
                dcc.Link('Análise de Features', href='page-features', className='mdl-navigation__link'),
                dcc.Link('Análise de popularidade', href='/page-popularidade', className='mdl-navigation__link'),
            ], className="mdl-navigation")
        ], className='mdl-layout__drawer')
    ], className='mdl-layout mdl-js-layout mdl-layout--fixed-header'),


    # --------- Main --------------
    html.Main([
        html.Div(id='page-main',className='page-content'),
    ]),

])

# ----------------------------------------------------------------------------------------------------------------------
# PAGE FEATURES

page_features = html.Div([

                    html.Div([
                        html.Div([
                           html.H1(["Análise de features"],className='titulo-texto')
                        ],className='titulo')

                    ],className='mdl-cell mdl-cell--12-col'),

                    # Feature Track
                    html.Div([
                        html.Div([
                            dcc.Graph(
                                id='radar-feature-track',
                                figure={
                                    'data': [go.Scatterpolar(
                                        r=[df_features_track['track_liveness'][4], df_features_track['track_speechness'][4],
                                           df_features_track['track_valence'][4], df_features_track['track_energy'][4],
                                           df_features_track['track_acousticness'][4],
                                           df_features_track['track_instrumentalness'][4],
                                           df_features_track['track_dancebility'][4]],
                                        theta=['Liveness', 'Speechness', 'Valence', 'Energy', 'Acousticness',
                                               'Instrumentalness', 'Dancebility'],
                                        fill='toself'
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

                            html.Div([
                                dcc.Dropdown(
                                    id='dropdown-feature-track',
                                    options=update_dropdown_features_track(),
                                    multi=False,
                                    value=""
                                ),
                            ]),
                        ], className='card'),

                    ], className='mdl-cell mdl-cell--4-col'),

                    # Feature Artist
                    html.Div([
                        html.Div([
                            dcc.Graph(
                                id='radar-feature-artist',
                                figure={
                                    'data': [go.Scatterpolar(
                                        r=[df_features_artist['track_liveness'][4], df_features_artist['track_speechness'][4],
                                           df_features_artist['track_valence'][4], df_features_artist['track_energy'][4],
                                           df_features_artist['track_acousticness'][4],
                                           df_features_artist['track_instrumentalness'][4],
                                           df_features_artist['track_dancebility'][4]],
                                        theta=['Liveness', 'Speechness', 'Valence', 'Energy', 'Acousticness',
                                               'Instrumentalness', 'Dancebility'],
                                        fill='toself'
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

                            html.Div([
                                dcc.Dropdown(
                                    id='dropdown-feature-artist',
                                    options=update_dropdown_features_artist(),
                                    multi=False,
                                    value=""
                                ),
                            ]),
                        ], className='card'),
                    ],className='mdl-cell mdl-cell--4-col'),

                        # Feature Playlist
                        html.Div([
                            html.Div([
                                dcc.Graph(
                                    id='radar-feature-playlist',
                                    figure={
                                        'data': [go.Scatterpolar(
                                            r=[df_features_playlist['track_liveness'][4], df_features_playlist['track_speechness'][4],
                                               df_features_playlist['track_valence'][4], df_features_playlist['track_energy'][4],
                                               df_features_playlist['track_acousticness'][4],
                                               df_features_playlist['track_instrumentalness'][4],
                                               df_features_playlist['track_dancebility'][4]],
                                            theta=['Liveness', 'Speechness', 'Valence', 'Energy', 'Acousticness',
                                                   'Instrumentalness', 'Dancebility'],
                                            fill='toself'
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

                                html.Div([
                                    dcc.Dropdown(
                                        id='dropdown-feature-playlist',
                                        options=update_dropdown_features_playlist(),
                                        multi=False,
                                        value=""
                                    ),
                                ]),
                            ], className='card'),

                    ], className='mdl-cell mdl-cell--4-col'),

            ], className= 'mdl-grid')

@app.callback(dash.dependencies.Output('radar-feature-track', 'figure'),
              [dash.dependencies.Input('dropdown-feature-track', 'value')])
def display_page(track_selected):
    temp = df_features_track
    if track_selected:
        temp = df_features_track.loc[df_features_track['track_name']==track_selected]


    traces = []
    layout_trace = []


    traces.append(go.Scatterpolar(
        r=[temp['track_liveness'].values[0], temp['track_speechness'].values[0],
           temp['track_valence'].values[0], temp['track_energy'].values[0],
           temp['track_acousticness'].values[0],
           temp['track_instrumentalness'].values[0],
           temp['track_dancebility'].values[0]],
        theta=['Liveness', 'Speechness', 'Valence', 'Energy', 'Acousticness',
               'Instrumentalness', 'Dancebility'],
        fill='toself'
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

@app.callback(dash.dependencies.Output('radar-feature-artist', 'figure'),
              [dash.dependencies.Input('dropdown-feature-artist', 'value')])
def display_page(artist_selected):
    temp = df_features_artist
    if artist_selected:
        temp = df_features_artist.loc[df_features_artist['artist_name']==artist_selected]


    traces = []
    layout_trace = []


    traces.append(go.Scatterpolar(
        r=[temp['track_liveness'].values[0], temp['track_speechness'].values[0],
           temp['track_valence'].values[0], temp['track_energy'].values[0],
           temp['track_acousticness'].values[0],
           temp['track_instrumentalness'].values[0],
           temp['track_dancebility'].values[0]],
        theta=['Liveness', 'Speechness', 'Valence', 'Energy', 'Acousticness',
               'Instrumentalness', 'Dancebility'],
        fill='toself'
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
    if playlist_selected:
        temp = df_features_playlist.loc[df_features_playlist['playlist_name']==playlist_selected]


    traces = []
    layout_trace = []


    traces.append(go.Scatterpolar(
        r=[temp['track_liveness'].values[0], temp['track_speechness'].values[0],
           temp['track_valence'].values[0], temp['track_energy'].values[0],
           temp['track_acousticness'].values[0],
           temp['track_instrumentalness'].values[0],
           temp['track_dancebility'].values[0]],
        theta=['Liveness', 'Speechness', 'Valence', 'Energy', 'Acousticness',
               'Instrumentalness', 'Dancebility'],
        fill='toself'
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
                dcc.Graph(
                    id='musicas_populares',
                    figure={
                        'data': [
                            {'x': [10,20,30], 'y': ['a','b','c'], 'type': 'bar'},
                        ],
                        'layout': {
                            'yaxis': {'title': 'Popularidade'}
                        }
                    }
                ),
            ], className='mdl-grid')
# ----------------------------------------------------------------------------------------------------------------------


# Callback Paginas
@app.callback(dash.dependencies.Output('page-main', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-features':
        return page_features
    elif pathname == '/page-grupos':
        return page_grupos
    elif pathname == '/page-popularidade':
        return page_popularidade
    if pathname == '/page-top-10':
        return page_top_10
    else:
        return page_top_10


if __name__ == '__main__':
    app.run_server(debug=True)
