import pandas as pd
import altair as alt
from altair import datum
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

alt.data_transformers.disable_max_rows()

##import and wrangle data
trees = pd.read_csv("data/processed_trees.csv")

# Build Front End
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = html.Div([
    html.H1('Vancouver cherry blossom tracker'),
    dbc.Row([
        dbc.Col([
            html.Label(['Month'], style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id="filter_month",
                value="all_months",
                options=[
                    {'label': 'All months', 'value': 'all_months'},
                    {'label': 'January', 'value': 'January'},
                    {'label': 'March', 'value': 'March'},
                    {'label': 'April', 'value': 'April'},
                    {'label': 'October', 'value': 'October'},
                    {'label': 'No Month', 'value': 'No_Month'}
                    ],
            )
        ]),
        dbc.Col([
            html.Label(['Neighbourhood'], style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id="filter_neighbourhood",
                value="all_neighbourhoods",
                options=[
                    {'label': 'All neighbourhoods', 'value': 'all_neighbourhoods'}
                ] + [
                    {"label": i, "value": i} for i in trees.NEIGHBOURHOOD_NAME.unique()
                ],
            )
        ]),
        dbc.Col([
            html.Label(['Cherry tree cultivars'], style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id="filter_cultivar",
                value="all_cultivars",
                options=[
                    {'label': 'All cultivars', 'value': 'all_cultivars'}
                ] + [
                    {"label": i, "value": i} for i in trees.CULTIVAR_NAME.unique()
                ],
            )
        ]),
        dbc.Col([
            html.Label(['Cherry tree diameter'], style={'font-weight': 'bold'}),
            dcc.RangeSlider(
                id="slider_diameter",
                min=0,
                max=1,
                marks={
                    0: '0m',
                    1: '1m'
                },
                tooltip={
                    "placement": "bottom", 
                    "always_visible": True
                }
            ),
        ])
    ]),
    dbc.Row([
        html.Iframe(
            id="bar", style={"border-width": "0", "width": "100%", "height": "800px"}
        )
    ])
])


@app.callback(
    Output("bar", "srcDoc"), 
    Input("filter_neighbourhood", "value"),
    Input("filter_cultivar", "value"))
##Create Cultivar Chart
def create_plot(neighbourhood, cultivar):
    bar_plot = (
        alt.Chart(trees[(trees["NEIGHBOURHOOD_NAME"] == neighbourhood) & (trees["CULTIVAR_NAME"] == cultivar)])
        .mark_bar()
        .encode(
            x=alt.X("count:Q", axis=alt.Axis(title="Number of Trees")),
            y=alt.Y(
                "COMMON_NAME:N",
                axis=alt.Axis(title="Tree Name"),
                sort=alt.SortField("count", order="descending"),
            ),
            tooltip=alt.Tooltip("count:Q"),
        )
        .transform_aggregate(count="count()", groupby=["COMMON_NAME"])
        .transform_filter("datum.count >= 10")
        .configure_mark(opacity=0.6, color="pink")
        .interactive()
    )

    return bar_plot.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)
