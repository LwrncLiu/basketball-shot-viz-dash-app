from dash import html, dcc
from dash.dependencies import Input, Output
import dash
import dash_bootstrap_components as dbc

# first register the app
custom_font_sheets = [
    "https://fonts.googleapis.com/css2?family=Lato:wght@700&display=swap"
]
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP, custom_font_sheets],
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)
server = app.server

# and then call from the pages in the app
from pages import shot_chart, home_page, resume

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-container', children=[])
], style={'height': '100%'})


@app.callback(
    Output('page-container', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/':
        return home_page.layout
    elif pathname == '/shot_chart':
        return shot_chart.layout
    elif pathname == '/resume':
        return resume.layout
    else:
        return '404 Page Error! Please choose a Link'


if __name__ == '__main__':
    app.run_server(debug=True)