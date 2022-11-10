# Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc

nav_bar = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(html.A("Projects", href='#projects', className='custom-nav-link')),
            dbc.NavItem(html.A("Resume", href='/resume', className='custom-nav-link')),
        ],
        color="white"
    )
])

former_experiences = [
    html.P([
        html.A(
            html.B('Epic Systems', className='epic-color'),
            href="https://www.epic.com/", target="_blank"),
        ': creating internal reporting tools for the 3500+ Technical Services Division'
    ])
]

home_section = html.Div(
    [
        dbc.Row([
            nav_bar
        ]),
        dbc.Row([
            dbc.Col([
                html.H1("Hi, I'm Lawrence Liu"),
                html.Div(
                    html.P('(2x half-marathon finisher)'),
                    id='marathon-tooltip-target'
                ),
                html.P([
                        html.Br(),
                        'I am currently a Data Engineer at ',
                        html.A(html.B('phData', className='phdata-color'), href="https://www.phdata.io/", target="_blank"),
                        ' creating Machine Learning pipelines for supply chain forecasting. ',
                        'I graduated from ',
                        html.B('NYU', className='nyu-color'),
                        ' in 2021 with a degree in Economics and found a passion for coding soon after entering the workforce.',
                        html.Br(),
                        html.Br(),
                        'My former experience includes:'
                ]),
                html.Ul(id='experience-list',
                        children=[html.Li(i) for i in former_experiences]),
                dbc.Tooltip(
                    "Brooklyn Half on October 19th, 2019 and Madison Half on November 13th, 2022 (🤞)",
                    target="marathon-tooltip-target",
                    placement='right'
                ),
            ])
        ],
        className='landing-page-text'
        ),

    ],
)

shot_chart_card = dbc.Card(
    [
        dbc.CardImg(src='/static/images/shot_chart.PNG', top=True),
        dbc.CardBody([
            html.H4('3D Shot Charts', className='card-title'),
            html.P(
                "Traditional shot charts are two-dimensional. "
                "I processed 21 years of data and re-learned the quadratic equation to add a third dimension."
            ),
            html.Div([
                html.Div('Python', className='pill', style={'backgroundColor': '#fff7e1', 'color': '#ffd241'}),
                html.Div('Dash', className='pill', style={'backgroundColor': '#ebedf1', 'color': '#3f4f75'}),
                html.Div('GCP', className='pill', style={'backgroundColor': '#9cbcf4', 'color': '#4485f4'})
            ]),
            dbc.Button('Check it out', color='secondary', href="/shot_chart", className='project-button')
        ])
    ]
)

project_section = html.Div([
    dbc.Row([
        html.H3('My Project(s)', className='project-title')
        ]),
    dbc.Row([
        dbc.Col([
            shot_chart_card
            ], width=4)
        ], className='project-cards', id='projects')
    ])

layout = html.Div(
    dbc.Container([
        html.Div(
            home_section, style={'height': '100vh'}, className='landing-page'
        ),
        html.Div(
            project_section, style={'height': '100vh'}, className='project-page'
        )
    ])
)
