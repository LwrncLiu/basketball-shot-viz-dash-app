from dash import html, dcc
from dash.dependencies import Input, Output

# connect to main app.py file
from app import app

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