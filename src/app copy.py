import pandas as pd
import altair as alt
from altair import datum
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

alt.data_transformers.disable_max_rows()

##import and wrangle data
trees = pd.read_csv("data/processed_trees.csv")

# Build Front End
app = Dash(__name__)
server = app.server
app.layout = html.Div(
    [
        "Neighbourhood",
        dcc.Dropdown(
            id="data_filter",
            value="Sunset",
            options=[
                {"label": i, "value": i} for i in trees.NEIGHBOURHOOD_NAME.unique()
            ],
        ),
        html.Iframe(
            id="bar", style={"border-width": "0", "width": "100%", "height": "500px"}
        ),
        dcc.Graph(id="map")
        # html.Iframe(
        #     id="map",
        #     style={"border-width": "0", "width": "100%", "height": "800px"},
        # ),
    ]
)


@app.callback(
    Output("bar", "srcDoc"), Input("data_filter", "value"), Input("map", "selectedData")
)
##Create Cultivar Chart
def create_plot(neighbourhood, selectedData):
    # print(selectedData)
    if selectedData == None:
        mytrees = trees
    else:
        selectedTrees = []
        if "points" in selectedData:
            if selectedData["points"] is not None:
                for point in selectedData["points"]:
                    print(point)
                    selectedTrees.append(point["customdata"][0])
                print(selectedTrees)
        mytrees = trees[trees["TREE_ID"].isin(selectedTrees)]

    print(len(mytrees))
    tree_plot = (
        alt.Chart(mytrees[mytrees["NEIGHBOURHOOD_NAME"] == neighbourhood])
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

    return tree_plot.to_html()


# @app.callback(Output("map", "srcDoc"), Input("data_filter", "value"))
# def create_map(neighbourhood):
#     map_plot = px.scatter_mapbox(
#         trees[trees["NEIGHBOURHOOD_NAME"] == neighbourhood],
#         lat="lat",
#         lon="lon",
#         color_discrete_sequence=["fuchsia"],
#         zoom=10.8,
#         height=700,
#     )
#     map_plot.update_layout(mapbox_style="open-street-map")

#     return map_plot.to_html()


@app.callback(Output("map", "figure"), Input("data_filter", "value"))
def create_map(neighbourhood):
    map_plot = px.scatter_mapbox(
        trees[trees["NEIGHBOURHOOD_NAME"] == neighbourhood],
        lat="lat",
        lon="lon",
        color_discrete_sequence=["fuchsia"],
        hover_data=["TREE_ID"],
        zoom=10.8,
        height=700,
    )
    map_plot.update_layout(mapbox_style="open-street-map", clickmode="event+select")

    return map_plot


if __name__ == "__main__":
    app.run_server(debug=True)
