# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine
from datetime import date as dt



from app import app

engine = create_engine('postgres://luismalta:123@localhost:5432/spotify_db')
df_top10_track = pd.read_sql_query("select * from spotify_db.top10_tracks('2018-10-23 00:00:00.000000')",con=engine)
df_top10_artist = pd.read_sql_query("select * from spotify_db.top10_artist('2018-10-23 00:00:00.000000')",con=engine)

# ======================================================================================================================
page_top_10 =  html.Div([

    # Card Ranking
    html.Div([
        html.Div([
            html.Div([

                html.H6(['Ranking'],className='mdl-cell mdl-cell--12-col'),
                html.Hr([],className='mdl-cell mdl-cell--12-col'),

                # Ranking Track
                html.Div([
                    html.Div([

                    ], className='card'),
                ], className='mdl-cell mdl-cell--5-col'),

                # Data Picker
                html.Div([
                    dcc.DatePickerSingle(
                        id='date-ranking',
                        date=dt(2018, 11, 1)
                    )
                ], className='mdl-cell mdl-cell--2-col'),

                # Ranking Artist
                html.Div([
                    html.Div([

                    ], className='card'),
                ], className='mdl-cell mdl-cell--5-col'),

            ], className='mdl-grid'),
        ], className='card')
    ],className='mdl-cell mdl-cell--12-col', id ='card-ranking'),

    html.Div([
        html.Hr([])
    ], className='mdl-cell mdl-cell--12-col'),

    #===================================================================================================================
    # Card Comparação
    html.Div([

        html.Div([

            html.Div([

                html.H6(['Comparação'], className='titulo-grafico'),
                html.Hr([], className='mdl-cell mdl-cell--12-col'),

                # Grafico comparação
                html.Div([

                ], className='mdl-cell mdl-cell--8-col'),

                # Card Dropdowns
                html.Div([
                    html.H6(['Track 1']),

                    dcc.Dropdown(
                        id='dropdown-feature-track',
                        options=['teste'],
                        multi=False,
                        value=""
                    ),

                    html.H6(['Track 2']),

                    dcc.Dropdown(
                        id='dropdown-feature-track',
                        options=['teste'],
                        multi=False,
                        value=""
                    ),

                ], className='mdl-cell mdl-cell--4-col'),

            ], className='mdl-grid')

        ], className='card')

    ], className='mdl-cell mdl-cell--12-col'),

    html.Div([
        html.Hr([])
    ], className='mdl-cell mdl-cell--12-col'),

    # ===================================================================================================================
    # Card evolucao
    html.Div([

        html.Div([

            html.Div([

                html.H6(['Downgrade e Upgrade'], className='titulo-grafico'),
                html.Hr([], className='mdl-cell mdl-cell--12-col'),

                html.Div([

                    html.Div([

                    ], className='card')

                ], className='mdl-cell mdl-cell--6-col'),

                html.Div([

                    html.Div([

                    ], className='card')

                ], className='mdl-cell mdl-cell--6-col'),

            ], className='mdl-grid')

        ], className='card')

    ], className='mdl-cell mdl-cell--12-col'),

    html.Div([

        html.Hr([])

    ], className='mdl-cell mdl-cell--12-col'),


            ], className='mdl-grid')


# ======================================================================================================================
@app.callback(dash.dependencies.Output('card-ranking', 'children'),
              [dash.dependencies.Input('date-ranking', 'date')])
def display_page(data):

    query = data + ' 00:00:00.000000'
    df_top10_track = pd.read_sql_query('select * from spotify_db.top10_tracks(' + "'" + query + "'"+')',
                                       con=engine)
    df_top10_artist = pd.read_sql_query('select * from spotify_db.top10_artist(' + "'" + query + "'"+')',
                                       con=engine)

    return  html.Div([
            html.Div([

                html.H6(['Ranking'], className='titulo-grafico'),
                html.Hr([], className='mdl-cell mdl-cell--12-col'),

                # Ranking Track

                html.Div([],className='mdl-cell mdl-cell--2-col'),

                html.Div([

                    html.Table(
                        # Header
                        [html.Tr(
                            [html.Th(col, className='mdl-data-table__cell--non-numeric') for col in
                             df_top10_track.columns])] +

                        # Body
                        [html.Tr([
                            html.Td(df_top10_track.iloc[i][col], className='mdl-data-table__cell--non-numeric') for
                            col
                            in
                            df_top10_track.columns
                        ]) for i in range(min(len(df_top10_track), 10))],
                        className='mdl-data-table mdl-js-data-table'
                    ),

                ], className='mdl-cell mdl-cell--3-col'),

                # Data Picker
                html.Div([
                    dcc.DatePickerSingle(
                        id='date-top10',
                        date=dt(2018, 11, 1)
                    )
                ], className='mdl-cell mdl-cell--2-col'),

                # Ranking Artist
                html.Div([

                    html.Table(
                        # Header
                        [html.Tr(
                            [html.Th(col, className='mdl-data-table__cell--non-numeric') for col in
                             df_top10_track.columns])] +

                        # Body
                        [html.Tr([
                            html.Td(df_top10_track.iloc[i][col], className='mdl-data-table__cell--non-numeric') for
                            col
                            in
                            df_top10_track.columns
                        ]) for i in range(min(len(df_top10_track), 10))],
                        className='mdl-data-table mdl-js-data-table'
                    ),

                ], className='mdl-cell mdl-cell--3-col'),

                html.Div([], className='mdl-cell mdl-cell--2-col'),

            ], className='mdl-grid'),
        ], className='card')






























#
# html.Div([
#         dcc.DatePickerSingle(
#             id='date-top10',
#             date=dt(2018, 11, 1)
#         )
#     ], className='mdl-cell mdl-cell--12-col'),
#
#
#
#     html.Div([
#         html.Div([
#             html.Div([
#                 html.Div([
#                     html.H3(['Track'])
#                 ], className='card')
#             ],className='mdl-cell mdl-cell--6-col'),
#             html.Div(['Artist'],className='mdl-cell mdl-cell--6-col'),
#
#             html.Div([
#                 html.Table(
#                     # Header
#                     [html.Tr(
#                         [html.Th(col, className='mdl-data-table__cell--non-numeric') for col in
#                          df_top10_track.columns])] +
#
#                     # Body
#                     [html.Tr([
#                         html.Td(df_top10_track.iloc[i][col], className='mdl-data-table__cell--non-numeric') for col
#                         in
#                         df_top10_track.columns
#                     ]) for i in range(min(len(df_top10_track), 10))], className='mdl-data-table mdl-js-data-table'
#                 ),
#             ], className='mdl-cell mdl-cell--6-col'),
#
#             html.Div([
#                 html.Table(
#                     # Header
#                     [html.Tr(
#                         [html.Th(col, className='mdl-data-table__cell--non-numeric') for col in
#                          df_top10_artist.columns])] +
#
#                     # Body
#                     [html.Tr([
#                         html.Td(df_top10_artist.iloc[i][col], className='mdl-data-table__cell--non-numeric') for col
#                         in
#                         df_top10_artist.columns
#                     ]) for i in range(min(len(df_top10_artist), 10))], className='mdl-data-table mdl-js-data-table'
#                 ),
#             ], className='mdl-cell mdl-cell--6-col'),
#
#         ],className='mdl-grid')
#     ], className='mdl-cell mdl-cell--12-col', id='top10_page')