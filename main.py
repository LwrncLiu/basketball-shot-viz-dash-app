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

shot1 = BasketballShot(-148, 207, 0, 'miss',1)
shot1_df = shot1.get_shot_path_coordinates()

shot2 = BasketballShot(-46, 1, 0, 'miss',2)
shot2_df = shot2.get_shot_path_coordinates()

shot3 = BasketballShot(-63, 138, 0, 'make',3)
shot3_df = shot3.get_shot_path_coordinates()

shot4 = BasketballShot(-240, 50, 0, 'make',4)
shot4_df = shot4.get_shot_path_coordinates()

shot5 = BasketballShot(-44, 183, 0, 'make',5)
shot5_df = shot5.get_shot_path_coordinates()

shot6 = BasketballShot(-198, 91, 0, 'miss',6)
shot6_df = shot6.get_shot_path_coordinates()

shot7 = BasketballShot(-119, 139, 0, 'make',7)
shot7_df = shot7.get_shot_path_coordinates()

shot8 = BasketballShot(92, 32, 0, 'miss',8)
shot8_df = shot8.get_shot_path_coordinates()

shot9 = BasketballShot(-18, -3, 0, 'make',9)
shot9_df = shot9.get_shot_path_coordinates()

shot10 = BasketballShot(227, 29, 0, 'miss',10)
shot10_df = shot10.get_shot_path_coordinates()

shot11 = BasketballShot(6, -8, 0, 'make',11)
shot11_df = shot11.get_shot_path_coordinates()

shot12 = BasketballShot(193, 199, 0, 'miss',12)
shot12_df = shot12.get_shot_path_coordinates()

shot13 = BasketballShot(-157, 203, 0, 'miss',13)
shot13_df = shot13.get_shot_path_coordinates()

shot14 = BasketballShot(-26, 192, 0, 'make',14)
shot14_df = shot14.get_shot_path_coordinates()

shot15 = BasketballShot(-5, 19, 0, 'make',15)
shot15_df = shot15.get_shot_path_coordinates()

shot16 = BasketballShot(35, 13, 0, 'miss',16)
shot16_df = shot16.get_shot_path_coordinates()


fig = px.line_3d(data_frame=pd.concat([court_df, shot1_df, shot2_df, shot3_df
                                       , shot4_df, shot5_df, shot6_df
                                       , shot7_df, shot8_df, shot9_df
                                       , shot10_df, shot11_df, shot12_df, shot13_df, shot14_df,
                                       shot15_df, shot16_df], ignore_index=True, axis=0),
                 x='x',
                 y='y',
                 z='z',
                 line_group='line_id',
                 color='line_group_id',
                 color_discrete_map={
                     "court": "black",
                     "shot_make": "green",
                     "shot_miss": "red"
                 })
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