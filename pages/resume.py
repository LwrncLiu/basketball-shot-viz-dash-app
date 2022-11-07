from dash import html

layout = html.Div(
    html.Iframe(id='embedded-resume', src='static/documents/Lawrence_CV.pdf', style={'height': '100vh', 'width': '100vw'})
)
