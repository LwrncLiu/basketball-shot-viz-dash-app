import pandas as pd
import plotly.express as px  # allows you to create graphs
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
from court import CourtCoordinates
from shot import BasketballShot
import dash_bootstrap_components as dbc

# Incorporate data into app
court = CourtCoordinates()
court_df = court.get_court_lines_coordinates()

shot1 = BasketballShot(180, 400, 0)
shot1_df = shot1.get_shot_path_coordinates()

fig = px.line_3d(data_frame=pd.concat([court_df, shot1_df], ignore_index=True, axis=0),
                 x='x',
                 y='y',
                 z='z',
                 line_group='line_id')
# Build your components
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
graph_title = dcc.Markdown(children='# 3D Visualization of NBA Shot Attempts')
shot_graph = dcc.Graph(figure=fig)

# Customize your own Layout
app.layout = dbc.Container([graph_title, shot_graph])

# Callback allows components to interact
# Callback decorator has an output and input
# @app.callback(
#     Output(shot_graph, component_property='figure'),
#     Input(dropdown, component_property='value')
# )
# def update_graph(user_input): # the function argument(s) come from the component property of the Input
#     fig = px.line_3d(data_frame=df,
#                      x='x',
#                      y='y',
#                      z='z',
#                      line_group='line_id')
#
#     return fig

# court_lines_df = get_court_line_coordinates()
#
# shot_location = (177, 53, 0)
# shot_3d_coordinates = calculate_shot_path_coordinates(shot_location)
# df1 = pd.DataFrame(shot_3d_coordinates, columns=['x', 'y', 'z', 'i'])
# df1['line_id'] = 'JT'
# df1['color'] = 'green'
#
# shot_location = (180, 400, 0)
# shot_3d_coordinates = calculate_shot_path_coordinates(shot_location)
# df2 = pd.DataFrame(shot_3d_coordinates, columns=['x', 'y', 'z', 'i'])
# df2['line_id'] = 'IT'
# df2['color'] = 'red'
#
# df = pd.concat([df1, df2, court_lines_df], ignore_index=True, axis=0)
#
# fig = px.line_3d(df, x='x', y='y', z='z', line_group='line_id')
# fig

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)