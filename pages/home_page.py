# Import necessary libraries
from dash import html, dcc
import dash_bootstrap_components as dbc

nav_bar = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("About", href='#about')),
            dbc.NavItem(dbc.NavLink("Projects", href='#projects')),
            dbc.NavItem(dbc.NavLink("Resume", href='/resume')),
        ],
        color="white"
    )
])

about_section = dbc.Col([
                html.H3('About Me', id='about'),
                html.P(['Hello, my name is Lawrence. I am currently a Data Engineer at ', html.Strong('phData'), ' creating Machine Learning pipelines for supply chain forecasting.']),
                html.P('I graduated from NYU with a degree in Economics and found a passion for coding soon after entering the workforce.'),
                html.P('My former experience includes:'),
                html.P([html.Strong('Epic Systems:'), ' creating internal reporting tools for the 3500+ Technical Services Division'])
])

shot_chart_card = dbc.Card(
    [
        dbc.CardImg(src='/static/images/shot_chart.PNG', top=True),
        dbc.CardBody([
            html.H4('3D Shot Charts', className='card-title'),
            html.P(
                "Traditional shot charts are two-dimensional. "
                "I processed 21 years of data and re-learned the quadratic equation to add a third dimension."
            ),
            dbc.Button('Check it out', color='primary', href="/shot_chart")
        ])
    ]
)

layout = html.Div(
    dbc.Container([
        dbc.Row([
            nav_bar
        ]),
        dbc.Row([
            dbc.Col([
                html.H1('Lawrence Liu'),
                html.P('(2x half-marathon finisher)')
            ])
        ], className='text-center'),
        dbc.Row([
            about_section
        ]),
        dbc.Row([
            html.H3('Some of my Projects', id='projets')
        ]),

        dbc.Row([
            dbc.Col([
                shot_chart_card
            ], width=4)
        ])


    ])
)
# Define the page layout
