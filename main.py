import pandas as pd
import plotly.express as px  # allows you to create graphs
from dash import Dash, dcc, Input, Output, State, html  # pip install dash (version 2.0.0 or higher)
from court import CourtCoordinates
import dash_bootstrap_components as dbc
import os
from dotenv import load_dotenv
from basketballshot import BasketballShot
from google.cloud import bigquery

load_dotenv()
# establish connection to database
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
client = bigquery.Client()

# get the court lines from the CourtCoordinates class
court = CourtCoordinates()
court_df = court.get_court_lines_coordinates()

# pull data needed for web app
# TODO: move data to bigquery and query dynamically, otherwise, there will be a csv file with ~22 million rows

season_query = """
    SELECT      distinct
                season_year
    FROM        processed.games
    ORDER BY    season_year;
"""

seasons_df = client.query(season_query).to_dataframe()  # Make an API request.
available_seasons = seasons_df.to_dict('records')

# dash components
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

dropdown_option_styles = {'color': 'white', 'text-align': 'center'}
graph_title = dcc.Markdown(children='# Field Goal Attempts from the 2021-2022 NBA season', style={'color': 'white'})
season_option_title = dcc.Markdown(children='Season *', style=dropdown_option_styles)
team_option_title = dcc.Markdown(children='Team *', style=dropdown_option_styles)
player_option_title = dcc.Markdown(children='Player', style=dropdown_option_styles)
game_option_title = dcc.Markdown(children='Game *', style=dropdown_option_styles)

generate_graph_button = dbc.Button(
    'Update Graph',
    disabled=True,
    color='secondary',
    class_name='ml-3',
    size='md',
    n_clicks=0,
    id='generate_graph_button',
    style={'position': 'relative',
           'float': 'right'}
)

reset_options_button = dbc.Button(
    'Reset Options',
    class_name='ml-3',
    color='light',
    size='md',
    n_clicks=0,
    id='reset_options_button'
)

summary_card = dbc.Card(body=True, id='summary_card')

season_option = dcc.Dropdown(id='season_option', options=[
    {'label': i['season_year'], 'value': i['season_year']} for i in available_seasons
])
team_option = dcc.Dropdown(id='team_option')
player_option = dcc.Dropdown(id='player_option')
game_option = dcc.Dropdown(id='game_option')

shot_path_switch = html.Div(
    [
        dbc.Checklist(
            options=[
                {'label': 'Include 3D Shot Paths', 'value': 1}
            ],
            value=[1],
            id='shot_path_switch',
            switch=True,
            style={'color': 'white'}
        ),
    ]
)

color_blind_switch = html.Div(
    [
        dbc.Checklist(
            options=[
                {'label': 'Colorblind-Friendly(er)', 'value': 1}
            ],
            value=[],
            id='color_blind_switch',
            switch=True,
            style={'color': 'white'}
        )
    ]
)

shot_graph = dcc.Graph(id='3d_shot_graph', style={'width': '100%', 'height': '90vh'})
graph_loading_spinner = dbc.Spinner(shot_graph, id='graph_spinner',
                                    spinner_style={'width': '4rem', 'height': '4rem', 'color': 'white'})

# Layout formatting
app.layout = html.Div(
    dbc.Container([
        dbc.Row([
            dbc.Col([graph_title])
        ], justify='center', style={'padding': '1rem 0rem'}),

        dbc.Row([
            dbc.Col([season_option_title, season_option]),
            dbc.Col([team_option_title, team_option]),
            dbc.Col([player_option_title, player_option]),
            dbc.Col([game_option_title, game_option]),
        ], justify='center'),

        dbc.Row([
            dbc.Col([shot_path_switch], width=3, align='center'),
            dbc.Col([color_blind_switch], width=6, align='center'),
            dbc.Col([reset_options_button, generate_graph_button])
        ], style={'padding-top': '1rem'}),

        dbc.Row([
            dbc.Col([summary_card])
        ], align='center', justify='center', style={'padding-top': '1rem'}),

        dbc.Row([
            dbc.Col([graph_loading_spinner])
        ], align='center'
        )
    ], style={'backgroundColor': '#659DBD'}), style={'backgroundColor': '#659DBD'}
)


@app.callback(
    Output(team_option, component_property='options'),
    Input(season_option, component_property='value')
)
def update_team_option(season_selected):
    query = """
        SELECT      distinct
                    team_id,
                    team_name
        FROM        processed.games
        WHERE       season_year = @season
        ORDER BY    team_name;
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter('season', 'STRING', season_selected)
        ]
    )

    possible_teams_df = client.query(query, job_config=job_config).to_dataframe()
    possible_teams_dict = possible_teams_df.to_dict('records')

    return [{'label': i['team_name'], 'value': i['team_id']} for i in possible_teams_dict]


@app.callback(
    Output(player_option, component_property='options'),
    [Input(team_option, component_property='value'),
     Input(season_option, component_property='value')]
)
def update_player_option(team_selected, season_selected):
    possible_players_dict = {}

    if team_selected and season_selected:
        player_query = """
        SELECT      distinct 
                    player_id,
                    player_name
        FROM        processed.players 
        WHERE       players.game_id in (SELECT    distinct 
                                                  cast(game_id as int)
                                        FROM      processed.games 
                                        WHERE     season_year = @season
                                        AND       team_id = @team)
        AND         team_id = cast(@team as int)
        ORDER BY    player_name;
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter('team', 'STRING', team_selected),
                bigquery.ScalarQueryParameter('season', 'STRING', season_selected)
            ]
        )

        possible_players_df = client.query(player_query, job_config=job_config).to_dataframe()  # Make an API request.
        possible_players_dict = possible_players_df.to_dict('records')

    return [{'label': i['player_name'], 'value': i['player_id']} for i in possible_players_dict]


@app.callback(
    Output(game_option, component_property='options'),
    [Input(team_option, component_property='value'),
     Input(player_option, component_property='value'),
     Input(season_option, component_property='value')]
)
def update_game_option(team_selected, player_selected, season_selected):
    possible_games_dict = {}

    if season_selected and team_selected:
        if player_selected:
            game_query_by_team_and_player = """
                SELECT      distinct
                            games.game_id,
                            matchup || ' on ' || cast(cast(cast(game_date as datetime) as date) as string) as game_name,
                            cast(game_date as datetime) as game_datetime                       
                FROM        processed.games
                INNER JOIN  processed.players
                ON          cast(games.game_id as int) = players.game_id
                AND         players.player_id = @player
                WHERE       games.season_year = @season
                AND         games.team_id = @team
                ORDER BY    game_datetime;
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter('team', 'STRING', team_selected),
                    bigquery.ScalarQueryParameter('player', 'INTEGER', player_selected),
                    bigquery.ScalarQueryParameter('season', 'STRING', season_selected)
                ]
            )

            game_ids_df = client.query(game_query_by_team_and_player, job_config=job_config).to_dataframe()
            possible_games_dict = game_ids_df.to_dict('records')

        else:
            game_query_by_team = """
                SELECT      distinct
                            game_id,
                            matchup || ' on ' || cast(cast(cast(game_date as datetime) as date) as string) as game_name,
                            cast(game_date as datetime) as game_datetime                       
                FROM        processed.games
                WHERE       games.season_year = @season
                AND         games.team_id = @team
                ORDER BY    game_datetime;
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter('team', 'STRING', team_selected),
                    bigquery.ScalarQueryParameter('season', 'STRING', season_selected)
                ]
            )

            game_ids_df = client.query(game_query_by_team, job_config=job_config).to_dataframe()
            possible_games_dict = game_ids_df.to_dict('records')

    return [{'label': i['game_name'], 'value': i['game_id']} for i in possible_games_dict]


@app.callback(
    [Output('generate_graph_button', component_property='color'),
     Output('generate_graph_button', component_property='disabled')],
    [Input(season_option, component_property='value'),
     Input(team_option, component_property='value'),
     Input(game_option, component_property='value')]
)
def update_button(season_selected, team_selected, game_selected):

    valid_button_color = 'success'
    valid_button_disabled_state = False
    invalid_button_color = 'secondary'
    invalid_button_disabled_state = True

    if season_selected and team_selected and game_selected:
        return valid_button_color, valid_button_disabled_state

    return invalid_button_color, invalid_button_disabled_state


@app.callback(
    [Output('season_option', component_property='value'),
     Output('team_option', component_property='value'),
     Output('player_option', component_property='value'),
     Output('game_option', component_property='value'),
     Output('reset_options_button', component_property='n_clicks')],
    Input('reset_options_button', component_property='n_clicks')
)
def clear_selections(button_clicked):
    reset_button = 0
    season_value = None
    team_value = None
    player_value = None
    game_value = None

    return season_value, team_value, player_value, game_value, reset_button

@app.callback(
    [Output(shot_graph, component_property='figure'),
     Output(summary_card, component_property='children'),
     Output('generate_graph_button', component_property='n_clicks')],
    [State(player_option, component_property='value'),
     State(game_option, component_property='value'),
     State(team_option, component_property='value'),
     State(season_option, component_property='value'),
     Input('generate_graph_button', component_property='n_clicks'),
     State('shot_path_switch', component_property='value'),
     State('color_blind_switch', component_property='value')]
)
def update_graph_and_card(player_selected,
                          game_selected,
                          team_selected,
                          season_selected,
                          button_clicked,
                          shot_path_on,
                          colorblind_friendly):
    summary_string = 'Select values for season, team, game, and player (not required) to see 3D shot graph of a team''s or player''s shooting performance.'
    reset_button_clicks_num = 0

    # set color palette
    if len(colorblind_friendly) == 1:
        shot_color_palette = {
            'shot made': '#34ff29',
            'shot miss': '#b92179'
        }
        court_color = '#fdf9ea'
    else:
        shot_color_palette = {
            'shot made': '#2f9a2c',
            'shot miss': '#f34545'
        }
        court_color = '#fbeec1'

    # draw the lines of the court onto the 3d line plot
    fig = px.line_3d(data_frame=court_df,
                     x='x',
                     y='y',
                     z='z',
                     line_group='line_id',
                     color='line_group_id',
                     color_discrete_map={
                         'court': '#000000',
                         'hoop': '#e47041'
                     },
                     )
    fig.update_traces(line=dict(width=5), hovertemplate=None, hoverinfo='skip')  # set width for court lines

    camera = dict(
        eye=dict(x=1.2, y=1.2, z=0.9)
    )

    fig.update_layout(legend_title_text='Line Type: ',
                      legend=dict(
                          yanchor='top',
                          y=0.99,
                          xanchor='left',
                          orientation='h',
                          font=dict(size=12, color='black'),
                          bgcolor='white'
                      ),
                      scene_camera=camera,
                      scene=dict(
                          xaxis=dict(title='', showticklabels=False, showgrid=False,
                                     backgroundcolor='#fdfbf5'),
                          yaxis=dict(title='', showticklabels=False, showgrid=False,
                                     backgroundcolor='#fdfbf5',
                                     range=[-15, 485]),  # restricting 7 range (length) to avoid weird height formatting
                          zaxis=dict(title='',  showticklabels=False, showgrid=False,
                                     backgroundcolor=court_color),
                      ),
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=20, r=20, t=20, b=20),
                      )

    # update the graph with shot traces if 'update graph' button is clicked
    if button_clicked > 0:
        if season_selected and team_selected and game_selected:
            if player_selected:

                # only need to filter by player and game if all options are selected
                # to show the shot graphs of a player from a specific game
                shots_query = """
                    select      distinct
                                attempts.x,
                                attempts.y,
                                attempts.shot_distance,
                                attempts.shot_made_flag,
                                attempts.game_id,
                                attempts.game_event_id,
                                attempts.line_id,
                                attempts.shot_type_int,
                                players.player_name as subject
                    from        processed.shot_attempts attempts
                    inner join  processed.players
                    on          attempts.player_id = players.player_id
                    and         attempts.game_id = players.game_id
                    where       attempts.player_id = @player
                    and         attempts.game_id = @game;
                """
                job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter('player', 'INTEGER', player_selected),
                        bigquery.ScalarQueryParameter('game', 'INTEGER', game_selected)
                    ]
                )

            else:
                # filter by game and team if player is not selected to show shot graph
                # of a team from a specific game
                shots_query = """
                    select      distinct
                                attempts.x,
                                attempts.y,
                                attempts.shot_distance,
                                attempts.shot_made_flag,
                                attempts.game_id,
                                attempts.game_event_id,
                                attempts.line_id,
                                attempts.shot_type_int,
                                games.team_name as subject
                    from        processed.shot_attempts attempts
                    inner join  processed.games
                    on          attempts.game_id = cast(games.game_id as int)
                    and         attempts.team_id = cast(games.team_id as int)
                    where       attempts.game_id = @game
                    and         attempts.team_id = @team;
                """
                job_config = bigquery.QueryJobConfig(
                    query_parameters=[
                        bigquery.ScalarQueryParameter('game', 'INTEGER', game_selected),
                        bigquery.ScalarQueryParameter('team', 'INTEGER', team_selected)
                    ]
                )

            selected_shots_df = client.query(shots_query, job_config=job_config).to_dataframe()

            xyz_coordinates_df = pd.DataFrame()
            for index, row in selected_shots_df.iterrows():
                row_shot = BasketballShot(row.x,
                                          row.y,
                                          row.shot_distance,
                                          row.shot_made_flag,
                                          row.game_id,
                                          row.game_event_id,
                                          row.subject)
                row_coordinates_df = row_shot.get_shot_path_coordinates()
                xyz_coordinates_df = pd.concat([xyz_coordinates_df, row_coordinates_df])
            xyz_coordinates_df = xyz_coordinates_df[xyz_coordinates_df['y'] < 470]

            # summary subject for the summary card
            try:
                summary_subject = xyz_coordinates_df['subject'].values[0]
            except:
                print('No shots returned.')

            # make sure there's data before generating a graph
            if len(selected_shots_df.index) > 0:
                player_shots_start_df = xyz_coordinates_df[(xyz_coordinates_df['line_index'] == 0) &
                                                           (xyz_coordinates_df['y'] < 470)]

                # draw the arc of the basketball shots
                if len(shot_path_on) == 1:
                    shot_fig = px.line_3d(data_frame=xyz_coordinates_df,
                                          x='x',
                                          y='y',
                                          z='z',
                                          line_group='line_id',
                                          color='shot_result',
                                          color_discrete_map=shot_color_palette
                                          )
                    shot_fig.update_traces(line=dict(width=5), opacity=0.4,
                                           hovertext='line_id', hovertemplate=xyz_coordinates_df['line_id'])

                    # append the arcs to the court map
                    for i in range(len(shot_fig.data)):
                        fig.add_trace(shot_fig.data[i])

                shot_start_legend = True if len(shot_path_on) == 0 else False

                # plot the starting locations of the basketball shots
                shot_start_fig = px.scatter_3d(data_frame=player_shots_start_df,
                                               x='x',
                                               y='y',
                                               z='z',
                                               color='shot_result',
                                               color_discrete_map=shot_color_palette,
                                               opacity=0.7)
                shot_start_fig.update_traces(marker_size=2, showlegend=shot_start_legend,
                                             hovertext='line_id', hovertemplate=player_shots_start_df['line_id'])

                # append the shot location starts to the court map
                for i in range(len(shot_start_fig.data)):
                    fig.add_trace(shot_start_fig.data[i])

                n_fga = len(selected_shots_df['line_id'].unique())
                n_fgm = len(
                    selected_shots_df[selected_shots_df['shot_made_flag'] == 1]['line_id'].unique())

                three_pointer_df = selected_shots_df[selected_shots_df['shot_type_int'] == 3]
                n_3pt_fga = len(three_pointer_df['line_id'].unique())
                n_3pt_fgm = len(three_pointer_df[three_pointer_df['shot_made_flag'] == 1]['line_id'].unique())
                fg_percent = round((100.0 * n_fgm) / n_fga, 1)

                # generate summary string
                summary_string = f'{summary_subject} shot {fg_percent}%, making {n_fgm} of {n_fga} from the field with {n_3pt_fgm} of {n_3pt_fga} from three-point range.'

            else:
                summary_string = 'No data currently available for your selected parameters'

    # set trace hide legend for court here
    for trace in fig['data']:
        if trace['name'] == 'court' or trace['name'] == 'hoop':
            trace['showlegend'] = False
    fig.layout.legend.itemsizing = 'constant'

    return fig, summary_string, reset_button_clicks_num


if __name__ == '__main__':
    app.run_server(debug=True)
