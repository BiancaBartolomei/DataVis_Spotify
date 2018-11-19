# -*- coding: utf-8 -*-

import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine

import numpy as np
from datetime import date as dt
from app import app


engine = create_engine('postgres://biancabartolomei:19972015@localhost:5432/spotify')

df_artist_genre = pd.read_sql_query('select * from spotify_db.musicas_por_genero', con=engine)
df_explicit_genre = pd.read_sql_query('select * from spotify_db.explicit_genre', con=engine)
df_duration_track = pd.read_sql_query('select * from spotify_db.duration_track', con=engine)
quant_cat = engine.execute("select count(count) from (select count(playlist_category) from spotify_db.playlist group by playlist_category) a").cursor.fetchall()[0][0]
quant_albuns = engine.execute("select count(album_id) from spotify_db.album").cursor.fetchall()[0][0]
quant_art = engine.execute("select count(artist_id) from spotify_db.artist").cursor.fetchall()[0][0]
quant_track = engine.execute("select count(track_id) from spotify_db.track").cursor.fetchall()[0][0]

colors_artist_genre = ['#110014', '#220128', '#33013c', '#440250', '#550264', '#660278', '#77038c', '#8803a0',
                       '#9904b4', '#ab04c8', '#bc04dc', '#cd05f0', '#d70ffa', '#da23fb', '#de37fb', '#e040fb',
                       '#e45ffc', '#e873fc', '#eb87fd', '#ee9bfd']
color_g = ['#550264', '#660278', '#77038c', '#8803a0', '#9904b4']

group_1 = 150000 # 2:30
group_2 = 200000 # 3:20
group_3 = 240000 # 4
group_4 = 300000 # 5



def group_selection():
    group_count_1 = 0
    group_count_2 = 0
    group_count_3 = 0
    group_count_4 = 0
    group_count_5 = 0

    for t in df_duration_track['track_duration']:
        if t <= group_1:
            group_count_1 = group_count_1 + 1

        elif t <= group_2 and t > group_1:
            group_count_2 = group_count_2 + 1

        elif t <= group_3 and t > group_2:
            group_count_3 = group_count_3 + 1

        elif t > group_3 and t <= group_4:
            group_count_4 = group_count_4 + 1

        elif t > group_4:
            group_count_5 = group_count_5 + 1

    dominio = [group_count_1, group_count_2, group_count_3, group_count_4, group_count_5]

    return dominio


page_grupos = html.Div([

    # Card Ranking
    html.Div([
        html.Div([
            html.Div([

                html.H6([''],className='mdl-cell mdl-cell--12-col'),
                html.Hr([],className='mdl-cell mdl-cell--12-col'),

                # Data Picker
                html.Div([
                    html.Ul([

                        html.Li([

                            html.Span([
                                html.I([], className='material-icons mdl-list__item-avatar'),
                                html.Span([str(df_artist_genre['artist_genre'].size)]),
                                html.Span(['GÊNEROS MUSICAIS'], className='mdl-list__item-text-body'),
                            ], className='mdl-list__item-primary-content'),

                            html.Span([
                                html.A([
                                    html.I(['star'], className='material-icons2'),
                                ], className='mdl-list__item-secondary-content'),
                            ], className='mdl-list__item-secondary-content'),

                        ], className='mdl-list__item mdl-list__item--three-line'),

                        html.Li([
                            html.Span([
                                html.I([], className='mdl-list__item-avatar'),
                                html.Span([str(quant_track)]),
                                html.Span(['MÚSICAS'], className='mdl-list__item-text-body'),
                            ], className='mdl-list__item-primary-content'),
                            html.Span([
                                html.A([
                                    html.I(['star'], className='material-icons2'),
                                ], className='mdl-list__item-secondary-content'),
                            ], className='mdl-list__item-secondary-content'),
                        ], className='mdl-list__item mdl-list__item--three-line'),

                        html.Li([
                            html.Span([
                                html.I([], className='material-icons mdl-list__item-avatar'),
                                html.Span([str(quant_albuns)]),
                                html.Span(['ÁLBUNS'], className='mdl-list__item-text-body'),
                            ], className='mdl-list__item-primary-content'),
                            html.Span([
                                html.A([
                                    html.I(['star'], className='material-icons2'),
                                ], className='mdl-list__item-secondary-content'),
                            ], className='mdl-list__item-secondary-content'),
                        ], className='mdl-list__item mdl-list__item--three-line'),

                        html.Li([
                            html.Span([
                                html.I([], className='material-icons mdl-list__item-avatar'),
                                html.Span([str(quant_art)]),
                                html.Span(['ARTISTAS'], className='mdl-list__item-text-body'),
                            ], className='mdl-list__item-primary-content'),
                            html.Span([
                                html.A([
                                    html.I(['star'], className='material-icons2'),
                                ], className='mdl-list__item-secondary-content'),
                            ], className='mdl-list__item-secondary-content'),
                        ], className='mdl-list__item mdl-list__item--three-line'),

                        html.Li([
                            html.Span([
                                html.I([], className='material-icons mdl-list__item-avatar'),
                                html.Span([str(quant_cat)]),
                                html.Span(['CATEGORIAS DE PLAYLISTS'], className='mdl-list__item-text-body'),
                            ], className='mdl-list__item-primary-content'),
                            html.Span([
                                html.A([
                                    html.I(['star'], className='material-icons2'),
                                ], className='mdl-list__item-secondary-content'),
                            ], className='mdl-list__item-secondary-content'),
                        ], className='mdl-list__item mdl-list__item--three-line'),

                    ], className='demo-list-three mdl-list'),
                ], className='mdl-cell mdl-cell--4-col'),

                # Ranking Track
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
                    ], className='card'),
                ], className='mdl-cell mdl-cell--8-col'),

            ], className='mdl-grid'),
        ], className='card')
    ],className='mdl-cell mdl-cell--12-col', id ='card-ranking'),

    html.Div([
        html.Hr([])
    ], className='mdl-cell mdl-cell--12-col'),

    # ==================================================================================================================
    # Card evolucao
    html.Div([

        html.Div([

            html.Div([

                html.H6([''], className='titulo-grafico'),
                html.Hr([], className='mdl-cell mdl-cell--12-col'),

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
                                             'size': 12,
                                             'color': '#646168'}
                                }
                            }
                        ),
                    ], className='card')

                ], className='mdl-cell mdl-cell--6-col'),

                html.Div([

                    html.Div([
                        dcc.Graph(
                            id='pizza-duration-track',
                            figure={
                                'data': [go.Pie(
                                    labels=['Menor que 2:30 min', 'Entre 2:30 min e 3:20 min',
                                            'Entre 3:20 e 4 min', 'Entre 4 e 5 min', 'Maior que 5 min'],
                                    values=group_selection(),
                                    textinfo='value',
                                    hole=.4,
                                    marker=dict(colors=color_g),
                                )],
                                'layout': {
                                    'title': 'Quantidade de músicas pela média de duração',
                                    'font': {'family': 'Roboto',
                                             'size': 12,
                                             'color': '#646168'},
                                    'sort': True,
                                }
                            },
                        ),
                    ], className='card')

                ], className='mdl-cell mdl-cell--6-col'),

            ], className='mdl-grid')

        ], className='card')

    ], className='mdl-cell mdl-cell--12-col'),

    html.Div([

        html.Hr([])

    ], className='mdl-cell mdl-cell--12-col'),


            ], className='mdl-grid')
