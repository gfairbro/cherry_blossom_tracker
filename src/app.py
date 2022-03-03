import pandas as pd
import altair as alt
from altair import datum
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

alt.data_transformers.disable_max_rows()

##import and wrangle data
trees = pd.read_csv("data/processed_trees.csv")
trees["BLOOM_START"] = pd.to_datetime(trees["BLOOM_START"])
trees["BLOOM_END"] = pd.to_datetime(trees["BLOOM_END"])

# Build Front End
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = html.Div([
    dbc.Container(
        html.H1('Vancouver cherry blossom tracker'),
        style={
            'color': 'white', 
            'background-color': 'orchid',
            'font-family': 'Helvetica'
        }
    ),
    dbc.Container(
        dbc.Row([
            dbc.Col([
                html.Label(['Month'], style={'font-weight': 'bold'}),
                dcc.RangeSlider(
                    id="slider_month",
                    min=0,
                    max=5,
                    step=1,
                    value=[0, 5],
                    marks={
                        0: 'NA',
                        1: 'Jan',
                        2: 'Feb',
                        3: 'Mar',
                        4: 'Apr',
                        5: 'May'
                    }
                )
            ], width=4),
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
            ], width=3),
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
            ], width=3),
            dbc.Col([
                html.Label(['Cherry tree diameter'], style={'font-weight': 'bold'}),
                dcc.RangeSlider(
                    id="slider_diameter",
                    min=0,
                    max=150,
                    value=[0, 150],
                    marks={
                        0: '0cm',
                        150: '150cm'
                    },
                    tooltip={
                        "placement": "bottom", 
                        "always_visible": True
                    }
                )
            ]),
        ]),
        style={'background-color': 'whitesmoke'}
    ),
    dbc.Row([
        dbc.Col([
            html.Iframe(
                id="bar", style={"border-width": "0", "width": "100%", "height": "800px"}
            )
        ]),
        dbc.Col([
            html.Iframe(
                id="timeline", style={"border-width": "0", "width": "100%", "height": "100%"}
            )
        ]),
    ])
])


@app.callback(
    Output("bar", "srcDoc"), 
    Input("filter_neighbourhood", "value"))
##Create Cultivar Chart
def bar_plot(neighbourhood):

    if neighbourhood != 'all_neighbourhoods':
        trees_bar = trees[trees['NEIGHBOURHOOD_NAME'] == neighbourhood]
    else:
        trees_bar = trees

    bar_plot = (
        alt.Chart(trees_bar)
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

@app.callback(
    Output("timeline", "srcDoc"),
    Input("slider_month", "value"),
    Input("filter_neighbourhood", "value"),
    Input("filter_cultivar", "value"),
    Input("slider_diameter", "value"))
##Create Cultivar Chart
def timeline(month_range, neighbourhood, cultivar, diameter_range):
    trees_timeline = trees.dropna(subset=["BLOOM_START", "BLOOM_END"])

    trees_timeline = trees_timeline[
        (trees_timeline['BLOOM_START_MONTH']>=month_range[0]) 
        & (trees_timeline['BLOOM_END_MONTH']<=month_range[1])]

    trees_timeline = trees_timeline[trees_timeline['DIAMETER'].between(diameter_range[0], diameter_range[1])]

    if neighbourhood != 'all_neighbourhoods':
        trees_timeline = trees_timeline[trees_timeline['NEIGHBOURHOOD_NAME'] == neighbourhood]

    if cultivar != 'all_cultivars':
        trees_timeline = trees_timeline[trees_timeline['CULTIVAR_NAME'] == cultivar]

    timeline = alt.Chart(trees_timeline).mark_bar().encode(
        x=alt.X('BLOOM_START', axis=alt.Axis(
            values=[d.isoformat() for d in pd.date_range(start='2022-01-01', end='2022-5-31', freq='1M')],
            format="%b",
            tickCount=5,
            orient='top'), title=None),
        x2='BLOOM_END',
        y=alt.Y('CULTIVAR_NAME:N', title=None),
        tooltip=[
            alt.Tooltip('BLOOM_START', title='Start'), 
            alt.Tooltip('BLOOM_END', title='End')
        ]
    ).configure_mark(
        color="pink"
    ).configure_axis(
        domainOpacity=0
    ).configure_view(
        strokeOpacity=0
    )

    return timeline.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)
