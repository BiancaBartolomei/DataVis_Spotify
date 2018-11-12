import dash

external_stylesheets = ['assets/material.css']
external_scripts = ['assets/material.js']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)
server = app.server

app.config.suppress_callback_exceptions = True
