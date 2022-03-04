import pandas as pd
from dash import Dash, html, dcc, Input, Output
import altair as alt
from vega_datasets import data
import dash_bootstrap_components as dbc
from datetime import date
alt.data_transformers.disable_max_rows()

# Data (wrangled)
raw_trees = pd.read_csv("../data/processed_trees.csv", parse_dates=["BLOOM_START", "BLOOM_END"], dayfirst=True)

# Setup app and layout/frontend
app = Dash(external_stylesheets=[
    'https://fonts.googleapis.com/css2?family=Montserrat:wght@300&display=swap',
    dbc.themes.BOOTSTRAP])

# C O M P O N E N T S

# Header navigation component
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About", href="#"))
    ],
    brand="Vancouver Cherry Blossom Tracker",
    brand_href="#",
    color="#B665A4",
    dark=True,
)

# Menu filters

date_picker = dcc.DatePickerRange(
    id="picker_date",
    min_date_allowed=date(2022, 1, 1),
    max_date_allowed=date(2022, 5, 30),
    start_date_placeholder_text="Start date",
    end_date_placeholder_text="End date",
)

drop_hood = dcc.Dropdown(
    id="filter_neighbourhood",
    value="all_neighbourhoods",
    options=[
        { "label": "All neighbourhoods", "value": "all_neighbourhoods",
        }] + 
        [{"label": i, "value": i}
        for i in raw_trees.NEIGHBOURHOOD_NAME.unique()
        ]
    )

drop_cultivar = dcc.Dropdown(
    id="filter_cultivar",
    value="all_cultivars",
    options=[
        {"label": "All cultivars", "value": "all_cultivars"}
        ] +
        [{"label": i, "value": i}
        for i in raw_trees.CULTIVAR_NAME.unique()
        ]
)

# Range sliders

range_slider = dcc.RangeSlider(
    id="slider_diameter",
    min=0,
    max=150,
    value=[0, 150],
    marks={0: "0cm", 150: "150cm"},
    tooltip={"placement": "bottom", "always_visible": True},
)


# Read in global data
cars = data.cars()

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
        dbc.Col([
            html.Label(["Blossom date"], style={"font-weight": "bold"}),
            date_picker
            ],
            width = 3),
        dbc.Col([
            html.Label(["Neighbourhood"], style={"font-weight": "bold"}),
            drop_hood
            ],
            width = 3),
        dbc.Col([
            html.Label(["Cherry cultivars (types)"], style={"font-weight": "bold"}),
            drop_cultivar
            ],
            width = 3),
        dbc.Col([
            html.Label(["Cherry tree diameter"], style={"font-weight": "bold"}),
            range_slider
            ],
        width = 3)
        ],
        id = 'menu-bar'),
    dbc.Container([
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
            dbc.Col()])
            ])
        ],
    id = 'content'
)


        
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
    app.run_server(debug=True, port=8000)