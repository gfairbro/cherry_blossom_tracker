import pandas as pd
from dash import Dash, html, dcc, Input, Output, no_update
import altair as alt
import dash_bootstrap_components as dbc
from datetime import date
import plotly.express as px

alt.data_transformers.disable_max_rows()

# Data (wrangled)
raw_trees = pd.read_csv("data/processed_trees.csv")
raw_trees["BLOOM_START"] = pd.to_datetime(raw_trees["BLOOM_START"], format="%d/%m/%Y")
raw_trees["BLOOM_END"] = pd.to_datetime(raw_trees["BLOOM_END"], format="%d/%m/%Y")
raw_trees["CULTIVAR_NAME"] = raw_trees["CULTIVAR_NAME"].str.title()
raw_trees["COMMON_NAME"] = raw_trees["COMMON_NAME"].str.title()

# Vancouver geojson
url_geojson = "https://raw.githubusercontent.com/UBC-MDS/cherry_blossom_tracker/main/data/vancouver.geojson"
data_geojson_remote = alt.Data(
    url=url_geojson, format=alt.DataFormat(property="features", type="json")
)

# Setup app and layout/frontend
app = Dash(
    __name__,
    external_stylesheets=[
        "https://fonts.googleapis.com/css2?family=Montserrat:wght@300&display=swap",
        dbc.themes.BOOTSTRAP,
    ],
    compress=True
)

server = app.server

# C O M P O N E N T S

# Collapse

toast = html.Div(
    [
        dbc.Button(
            "About",
            id="simple-toast-toggle",
            color="#B665A4",
            className="mb-3",
            n_clicks=0,
        )
    ]
)


# Header navigation component
navbar = dbc.NavbarSimple(
    children=[toast],
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
    placeholder="Select neighbourhoods",
    options=[
        {"label": i, "value": i} for i in sorted(raw_trees.NEIGHBOURHOOD_NAME.unique())
    ],
    multi=True
)

drop_cultivar = dcc.Dropdown(
    id="filter_cultivar",
    placeholder="Select cultivars",
    options=[
        {"label": i, "value": i} for i in sorted(raw_trees.CULTIVAR_NAME.unique())
    ],
    multi=True
)

# Range sliders
range_slider = dcc.RangeSlider(
    id="slider_diameter",
    min=0,
    max=150,
    value=[0, 100],
    marks={0: "0cm", 150: "150cm"},
    tooltip={"placement": "bottom", "always_visible": True},
)

# L A Y O U T
app.title = "Vancouver Cherry Blossom Tracker"
app.layout = dbc.Container(
    [
        dbc.Toast(
            [
                html.A(
                    "GitHub",
                    href="https://github.com/UBC-MDS/cherry_blossom_tracker",
                    style={"color": "white", "text-decoration": "underline"},
                ),
                html.P(
                    "The dashboard was created by Katia Aristova, Gabriel Fairbrother, Chaoran Wang, TZ Yan. It is licensed under the terms of the GNU General Public License v3.0 license. You can find more information in our GitHub repo."
                ),
                html.A(
                    "Data",
                    href="https://opendata.vancouver.ca/explore/dataset/street-trees/",
                    style={"color": "white", "text-decoration": "underline"},
                ),
                html.P(
                    "The dataset was created by the City of Vancouver and accessed via Vancouver Open Data website."
                ),
                html.A(
                    "Logo",
                    href="https://thenounproject.com/icon/cherry-blossoms-2818017/",
                    style={"color": "white", "text-decoration": "underline"},
                ),
                html.P(
                    "The cherry blossom logo Cherry Blossoms by Olena Panasovska from NounProject.com"
                ),
            ],
            id="simple-toast",
            header="About",
            icon="primary",
            dismissable=True,
            is_open=False,
        ),
        dbc.Container(
            [
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.Div(
                                        html.Img(src="assets/logo.png", height="70px")
                                    ),
                                    id="logo-img",
                                    width=1,
                                    style={"padding-top": "5px"},
                                ),
                                dbc.Col(navbar, style={"padding": "0"}, width=11),
                            ]
                        )
                    ],
                    id="header",
                )
            ],
            id="header-back",
        ),
        dbc.Container(
            [
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.Label(
                                            ["Blossom date"],
                                        ),
                                        date_picker,
                                    ],
                                    width=3,
                                ),
                                dbc.Col(
                                    [
                                        html.Label(
                                            ["Neighbourhood"],
                                        ),
                                        drop_hood,
                                    ],
                                    width=3,
                                ),
                                dbc.Col(
                                    [
                                        html.Label(["Tree cultivar (type)"]),
                                        drop_cultivar,
                                    ],
                                    width=3,
                                ),
                                dbc.Col(
                                    [
                                        html.Label(
                                            ["Tree diameter"],
                                        ),
                                        range_slider,
                                    ],
                                    width=3,
                                ),
                            ],
                            id="menu-bar",
                        )
                    ]
                )
            ],
            id="nav-back",
        ),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label(["Cherry blossom tree map"]),
                                dbc.Col(
                                    [
                                        dcc.Loading(
                                            id="loading-1",
                                            type="circle",
                                            children=dcc.Graph(id="map"),
                                            color="#B665A4"
                                        ),
                                    ]
                                ),
                            ],
                            width=12,
                            id="row-map",
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label(["Tree cultivars (types)"]),
                                dcc.Loading(
                                    id="loading-2",
                                    type="circle",
                                    children=html.Iframe(id="bar"),
                                    color="#B665A4"
                                ),
                            ],
                            width=6,
                            className="chart-box",
                        ),
                        dbc.Col(
                            [
                                html.Label(["Blooming timeline"]),
                                dcc.Loading(
                                    id="loading-3",
                                    type="circle",
                                    children=html.Iframe(id="timeline"),
                                    color="#B665A4"
                                ),
                            ],
                            width=6,
                            className="chart-box",
                        ),
                    ],
                    className="row-chart",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label(["Tree diameters"]),
                                dcc.Loading(
                                    id="loading-4",
                                    type="circle",
                                    children=html.Iframe(id="diameter"),
                                    color="#B665A4"
                                ),
                            ],
                            width=6,
                            className="chart-box",
                        ),
                        dbc.Col(
                            [
                                html.Label(["Tree density"]),
                                dcc.Loading(
                                    id="loading-5",
                                    type="circle",
                                    children=html.Iframe(
                                        id="density",
                                        style={
                                            "height": "400px",
                                            "width": "100%",
                                            "border": "0",
                                        },
                                    ),
                                    color="#B665A4"
                                ),
                            ],
                            width=6,
                            className="chart-box",
                        ),
                    ],
                    className="row-chart",
                ),
            ]
        ),
    ],
    id="content",
)

# C H A R T  F U N C T I O N S


def street_map(df):
    map_plot = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        color_discrete_sequence=["#B665A4"],
        hover_data={
            "COMMON_NAME": True,
            "NEIGHBOURHOOD_NAME": True,
            "DIAMETER": True,
            "lat": False,
            "lon": False,
            "TREE_ID": True,
        },
        zoom=10.9,
        height=600,
        opacity=0.8,
    )
    map_plot.update_layout(
        mapbox_style="open-street-map", autosize=True, margin=dict(t=0, b=0, l=0, r=0)
    )

    map_plot.update_xaxes(visible=False)
    map_plot.update_yaxes(visible=False)

    return map_plot


def density_map(df):
    van_base = (
        alt.Chart(data_geojson_remote)
        .mark_geoshape(fill="lightgray")
        .project(type="identity", reflectY=True)
    )

    plot_van = (
        van_base
        + alt.Chart(df)
        .transform_lookup(
            default="0",
            as_="geo",
            lookup="NEIGHBOURHOOD_NAME",
            from_=alt.LookupData(data=data_geojson_remote, key="properties.name"),
        )
        .mark_geoshape()
        .encode(
            alt.Color(
                "count()",
                scale=alt.Scale(scheme="redpurple"),
                legend=alt.Legend(orient="bottom", title="Number of Trees"),
            ),
            alt.Shape(field="geo", type="geojson"),
            tooltip=["count()", "NEIGHBOURHOOD_NAME:N"],
        )
    ).project(type="identity", reflectY=True)

    return plot_van.to_html()


def bar_plot(trees_bar):
    trees_bar = trees_bar.dropna(subset=["CULTIVAR_NAME", "NEIGHBOURHOOD_NAME"])

    bar_plot = (
        alt.Chart(trees_bar)
        .mark_bar()
        .encode(
            x=alt.X("count:Q", axis=alt.Axis(title="Number of Trees")),
            y=alt.Y(
                "CULTIVAR_NAME:N",
                axis=alt.Axis(title="Tree Name"),
                sort=alt.SortField("count", order="descending"),
            ),
            tooltip=alt.Tooltip("count:Q"),
        )
        .transform_aggregate(count="count()", groupby=["CULTIVAR_NAME"])
        .configure_mark(opacity=0.6, color="#F3B2D2")
    )

    return bar_plot.to_html()


def timeline_plot(trees_timeline):
    trees_timeline = trees_timeline.dropna(subset=["BLOOM_START", "BLOOM_END"])

    timeline = (
        alt.Chart(trees_timeline)
        .mark_bar()
        .encode(
            x=alt.X(
                "BLOOM_START",
                axis=alt.Axis(
                    values=[
                        d.isoformat()
                        for d in pd.date_range(
                            start="2022-01-01", end="2022-5-31", freq="1M"
                        )
                    ],
                    format="%b",
                    tickCount=5,
                    orient="top",
                ),
                title=None,
            ),
            x2="BLOOM_END",
            y=alt.Y("CULTIVAR_NAME:N", title=None, sort="x"),
            tooltip=[
                alt.Tooltip("BLOOM_START", title="Start"),
                alt.Tooltip("BLOOM_END", title="End"),
            ],
        )
        .configure_mark(color="#F3B2D2")
        .configure_axis(domainOpacity=0)
        .configure_view(strokeOpacity=0)
    )

    return timeline.to_html()


def diameter_plot(trees_df):
    trees_df = trees_df.dropna(subset=["DIAMETER"])
    trees_df["DIAMETER_CM"] = trees_df["DIAMETER"] * 2.54
    diameter = (
        alt.Chart(trees_df)
        .transform_density("DIAMETER_CM", as_=["DIAMETER", "density"])
        .mark_area(
            interpolate="monotone",
            color="#F3B2D2",
            opacity=0.4,
            line=({"color": "#B665A4"}),
        )
        .encode(
            alt.X("DIAMETER", title="Tree diameter (cm)", scale=alt.Scale(nice=False)),
            alt.Y("density:Q", title="Density", axis=alt.Axis(labels=False)),
        )
    )
    return diameter.to_html()


# Set up callbacks/backend
@app.callback(
    Output("bar", "srcDoc"),
    Output("timeline", "srcDoc"),
    Output("diameter", "srcDoc"),
    Output("density", "srcDoc"),
    Output("map", "figure"),
    Input("picker_date", "start_date"),
    Input("picker_date", "end_date"),
    Input("filter_neighbourhood", "value"),
    Input("filter_cultivar", "value"),
    Input("slider_diameter", "value"),
    Input("map", "selectedData"),
)
def main_callback(
    start_date, end_date, neighbourhood, cultivar, diameter_range, selectedData
):
    # Build new dataset and call all charts

    # Date input Cleanup
    if start_date is None:
        start_date = "2022-01-01"
    if end_date is None:
        end_date = "2022-05-30"
    start_date = pd.Timestamp(date.fromisoformat(start_date))
    end_date = pd.Timestamp(date.fromisoformat(end_date))

    filtered_trees = raw_trees

    # Filter by selection from big map
    if selectedData is not None:
        selectedTrees = []
        if "points" in selectedData:
            if selectedData["points"] is not None:
                for point in selectedData["points"]:
                    # print(point)
                    selectedTrees.append(point["customdata"][-1])
                # print(selectedTrees)
        filtered_trees = filtered_trees[filtered_trees["TREE_ID"].isin(selectedTrees)]

    # Filter by neighbourhood
    if neighbourhood:
        filtered_trees = filtered_trees[
            filtered_trees["NEIGHBOURHOOD_NAME"].isin(neighbourhood)
        ]

    # Filter by date

    filtered_trees = filtered_trees[
        (
            (filtered_trees["BLOOM_START"] <= start_date)
            & (filtered_trees["BLOOM_END"] >= start_date)
        )
        | (
            (filtered_trees["BLOOM_START"] <= end_date)
            & (filtered_trees["BLOOM_END"] >= end_date)
        )
        | (filtered_trees["BLOOM_START"].between(start_date, end_date))
        | (filtered_trees["BLOOM_END"].between(start_date, end_date))
    ]

    # Filter by Diameter
    filtered_trees = filtered_trees[
        filtered_trees["DIAMETER"].between(diameter_range[0], diameter_range[1])
    ]

    if cultivar:
        filtered_trees = filtered_trees[filtered_trees["CULTIVAR_NAME"].isin(cultivar)]

    bar = bar_plot(filtered_trees)
    timeline = timeline_plot(filtered_trees)
    diameter = diameter_plot(filtered_trees)
    density = density_map(filtered_trees)
    big_map = street_map(filtered_trees)

    return bar, timeline, diameter, density, big_map


@app.callback(
    Output("simple-toast", "is_open"),
    [Input("simple-toast-toggle", "n_clicks")],
)
def open_toast(n):
    if n == 0:
        return no_update
    return True


if __name__ == "__main__":
    app.run_server(debug=True)
