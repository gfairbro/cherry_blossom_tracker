from dash import Dash, html, dcc, Input, Output
import altair as alt
from vega_datasets import data
import dash_bootstrap_components as dbc

# Navbar component

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About", href="#"))
    ],
    brand="Vancouver Cherry Blossom Tracker",
    brand_href="#",
    color="#B665A4",
    dark=True,
)

# Drop placeholder

drop_hood = dcc.Dropdown(
    id='hood',
    value='Month', 
    options=['Downtown', 'West End'])

# Read in global data
cars = data.cars()

# Setup app and layout/frontend
app = Dash(external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Montserrat:wght@300&display=swap',
    dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div(
                html.Img(src = 'assets/logo.png', height='50px')),
                id='logo-img',
                width = 1),
        dbc.Col(navbar, style = {'padding': '0'}, width = 10)
    ],
    id = 'header'),
    dbc.Row([
        dbc.Col(drop_hood, width = 3),
        dbc.Col('Text', width = 2)],
        id = 'menu-bar'),
    dbc.Row([dbc.Col(
        width = 12, 
        style = {
            'height': '400px',
            'background-image':'url("assets/map_placeholder.png")'})]),
    dbc.Row([
        dbc.Col(width = 6, style={'height': '500px', 'background-color': 'gray'}),
        dbc.Col(width = 6, style={'height': '500px', 'background-color': 'lightgrey'})]),
    dbc.Row([
        dbc.Col( 
            html.Iframe(
                id='scatter',
                style={'border-width': '0', 'width': '100%', 'height': '400px'}
                ),
                width = 6,
            ),
        dbc.Col(width = 6, style={'height': '500px', 'background-color': 'gray'})]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='xcol-widget',
                value='Horsepower',  # REQUIRED to show the plot on the first page load
                options=[{'label': col, 'value': col} for col in cars.columns]),
            dcc.Dropdown(
                id='ycol-widget',
                value='Displacement',  # REQUIRED to show the plot on the first page load
                options=[{'label': col, 'value': col} for col in cars.columns])],
            md=4),
        dbc.Col()])])
# Set up callbacks/backend
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xcol-widget', 'value'),
    Input('ycol-widget', 'value'))
def plot_altair(xcol, ycol):
    chart = alt.Chart(cars).mark_point().encode(
        x=xcol,
        y=ycol,
        tooltip='Horsepower').interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)