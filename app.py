# Define the Dash App and it's properties here

import dash
import dash_bootstrap_components as dbc

custom_font_sheets = [
    "https://fonts.googleapis.com/css2?family=Lato:wght@700&display=swap"
]
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP, custom_font_sheets],
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)
server = app.server
