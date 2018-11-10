
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine
from datetime import date as dt



engine = create_engine('postgres://luismalta:Lo3355199731@localhost:5432/spotify_db')

df_features_track = pd.read_sql_query('select * from spotify_db.features_track',con=engine)
df_features_artist= pd.read_sql_query('select * from spotify_db.features_artist',con=engine)
df_features_playlist = pd.read_sql_query('select * from spotify_db.features_playlist',con=engine)



external_stylesheets = ['assets/material.css']
external_scripts = ['assets/material.js']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)
server = app.server

app.config.suppress_callback_exceptions = True

app.title = "SPOTIFY POPULARITY DATABASE"

def update_dropdown_features_music():
    opt_music= []
    musics = []
    for music in df_features_track['track_name']:

        if music not in musics:
            a = {'label':music, 'value':music}
            opt_music.append(a)
            musics.append(music)

    opt_music.sort
    return opt_music

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
                    dcc.Graph(
                        id='radar-feature-musica',
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
                ], className='mdl-cell mdl-cell--12-col'),

                html.Div([
                    dcc.Dropdown(
                        id='dropdown-feature-music',
                        options=update_dropdown_features_music(),
                        multi=False,
                        value=""
                    ),
                ], className='mdl-cell mdl-cell--6-col'),

            ], className= 'mdl-grid'),
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