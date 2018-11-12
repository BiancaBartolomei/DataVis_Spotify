import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine
from datetime import date as dt
import dash_table


from app import app
from apps import groups, popularity




app.title = "SPOTIFY DASHBOARD"

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
            dcc.Link('Análise de grupos', href='/apps/page-grupos', className='mdl-navigation__link'),
            dcc.Link('Análise de Features', href='/apps/page-features', className='mdl-navigation__link'),
            dcc.Link('Análise de popularidade', href='/apps/page-popularidade', className='mdl-navigation__link'),
        ], className='mdl-navigation')
    ], className='mdl-layout__drawer'),

    # --------- Main --------------
    html.Main([
        html.Div(id='page-main', className='page-content'),
    ], className='mdl-layout__content'),

], className='mdl-layout mdl-js-layout')


@app.callback(dash.dependencies.Output('page-main', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/page-grupos':
        return groups.page_grupos
    if pathname == '/apps/page-popularidade':
        return popularity.page_top_10

    else:
        return popularity.page_top_10


if __name__ == '__main__':
    app.run_server(debug=True)