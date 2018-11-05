
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine
from datetime import date as dt



engine = create_engine('postgres://bdxulnbxczgzlx:41d56d0522876a442b7494fa56070a4993b34868812d14d5f93debd7a98fde6b@ec2-'
                       '184-72-234-230.compute-1.amazonaws.com:5432/d9vbm9b8oufhkq')

df = pd.read_sql_query('select * from spotify_db.top_musicas_populares',con=engine)


external_stylesheets = ['assets/material.css']
external_scripts = ['assets/material.js']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)
server = app.server

app.title = "SPOTIFY POPULARITY DATABASE"

app.layout = html.Div(children=[
#-----------------------------------------------------------------------------------------------------------------------
    #Header
    html.Div(children=[
        html.Header([
            html.Div([
                html.Span(children='Titulo', className='mdl-layout-title'),

                html.Div([

                ],className='mdl-layout-spacer'),

                html.Nav([
                    html.A('link1', href='/link-location',  className='mdl-navigation__link'),
                    html.A('link1', href='/link-location',  className='mdl-navigation__link'),
                    html.A('link1', href='/link-location',  className='mdl-navigation__link'),
                ], className='mdl-navigation mdl-layout--large-screen-only')

            ], className='mdl-layout__header-row')
        ], className='mdl-layout__header'),

        html.Div([
            html.Span(children='Titulo', className='mdl-layout-title'),

            html.Nav([
                html.A('link1', href='/link-location',  className='mdl-navigation__link'),
                html.A('link1', href='/link-location',  className='mdl-navigation__link'),
                html.A('link1', href='/link-location',  className='mdl-navigation__link')
            ], className="mdl-navigation")
        ], className='mdl-layout__drawer')
    ], className='mdl-layout mdl-js-layout mdl-layout--fixed-header'),


#-----------------------------------------------------------------------------------------------------------------------
    html.Main([
        html.Div([

        ], className='page-content')
    ], className='mdl-layout__content')
])


if __name__ == '__main__':
    app.run_server(debug=True)