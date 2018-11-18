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

colors_artist_genre = ['#110014', '#220128', '#33013c', '#440250', '#550264', '#660278', '#77038c', '#8803a0',
                       '#9904b4', '#ab04c8', '#bc04dc', '#cd05f0', '#d70ffa', '#da23fb', '#de37fb', '#e040fb',
                       '#e45ffc', '#e873fc', '#eb87fd', '#ee9bfd']


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

    # Card Ranking
    html.Div([
        html.Div([
            html.Div([

                html.H6(['Ranking'],className='mdl-cell mdl-cell--12-col'),
                html.Hr([],className='mdl-cell mdl-cell--12-col'),

                # Data Picker
                html.Div([
                    html.Ul([
                        html.Li([
                            html.Span([
                                html.I([], className='material-icons mdl-list__item-avatar'),
                                html.Span(['100']),
                                html.Span(['Generos musicais diferentes'], className='mdl-list__item-text-body'),
                            ], className='mdl-list__item-primary-content'),
                            html.Span([
                                html.A([
                                    html.I(['star'], className='material-icons'),
                                ], className='mdl-list__item-secondary-content'),
                            ], className='mdl-list__item-secondary-content'),
                        ], className='mdl-list__item mdl-list__item--three-line'),

                        html.Li([
                            html.Span([
                                html.I([], className='mdl-list__item-avatar'),
                                html.Span(['200']),
                                html.Span(['Quantidade de artistas'], className='mdl-list__item-text-body'),
                            ], className='mdl-list__item-primary-content'),
                            html.Span([
                                html.A([
                                    html.I(['star'], className='material-icons'),
                                ], className='mdl-list__item-secondary-content'),
                            ], className='mdl-list__item-secondary-content'),
                        ], className='mdl-list__item mdl-list__item--three-line'),

                        html.Li([
                            html.Span([
                                html.I([], className='material-icons mdl-list__item-avatar'),
                                html.Span(['200']),
                                html.Span(['albuns'], className='mdl-list__item-text-body'),
                            ], className='mdl-list__item-primary-content'),
                            html.Span([
                                html.A([
                                    html.I(['star'], className='material-icons'),
                                ], className='mdl-list__item-secondary-content'),
                            ], className='mdl-list__item-secondary-content'),
                        ], className='mdl-list__item mdl-list__item--three-line'),

                        html.Li([
                            html.Span([
                                html.I([], className='material-icons mdl-list__item-avatar'),
                                html.Span(['4']),
                                html.Span(['categorias'], className='mdl-list__item-text-body'),
                            ], className='mdl-list__item-primary-content'),
                            html.Span([
                                html.A([
                                    html.I(['star'], className='material-icons'),
                                ], className='mdl-list__item-secondary-content'),
                            ], className='mdl-list__item-secondary-content'),
                        ], className='mdl-list__item mdl-list__item--three-line'),

                        html.Li([
                            html.Span([
                                html.I([], className='material-icons mdl-list__item-avatar'),
                                html.Span(['10']),
                                html.Span(['playlists'], className='mdl-list__item-text-body'),
                            ], className='mdl-list__item-primary-content'),
                            html.Span([
                                html.A([
                                    html.I(['star'], className='material-icons'),
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

                html.H6(['Downgrade e Upgrade'], className='titulo-grafico'),
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
                                             'size': 15,
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

                ], className='mdl-cell mdl-cell--6-col'),

            ], className='mdl-grid')

        ], className='card')

    ], className='mdl-cell mdl-cell--12-col'),

    html.Div([

        html.Hr([])

    ], className='mdl-cell mdl-cell--12-col'),


            ], className='mdl-grid')
