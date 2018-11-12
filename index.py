# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html

from app import app
from apps import groups, popularity, features

app.title = "SPOTIFY DASHBOARD"

# Estrutura principal do dashboard
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    # Criação de header da página principal
    html.Header([
        html.Div([
            html.Span(['Spotify Dashboard'], className='mdl-layout-title'),
            html.Div([], className='mdl-layout-spacer')
        ], className='mdl-layout__header-row')
    ], className='mdl-layout__header mdl-layout__header--scroll'),

    html.Div([
        html.Span(['Menu'], className='mdl-layout-title'),
        html.Nav([
            dcc.Link('Análise de grupos', href='/apps/page-grupos', className='mdl-navigation__link'),
            dcc.Link('Análise de Features', href='/apps/page-features', className='mdl-navigation__link'),
            dcc.Link('Análise de popularidade', href='/apps/page-popularidade', className='mdl-navigation__link'),
        ], className='mdl-navigation')
    ], className='mdl-layout__drawer'),

    # Parte que será substituida pelo callback
    html.Main([
        html.Div(id='page-main', className='page-content'),
    ], className='mdl-layout__content'),

], className='mdl-layout mdl-js-layout')


# Leva até as páginas desejadas
@app.callback(dash.dependencies.Output('page-main', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/page-grupos':
        return groups.page_grupos
    if pathname == '/apps/page-popularidade':
        return popularity.page_top_10
    if pathname == '/apps/page-features':
        return features.page_features

    else:
        return popularity.page_top_10


if __name__ == '__main__':
    app.run_server(debug=True)
