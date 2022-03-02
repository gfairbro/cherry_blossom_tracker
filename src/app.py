import pandas as pd
import altair as alt
from altair import datum
from dash import Dash, html, dcc, Input, Output
alt.data_transformers.disable_max_rows()

##import and wrangle data
trees = pd.read_csv('../data/processed_trees.csv')

#Build Front End
app = Dash(__name__)
server=app.server
app.layout = html.Div([
        'Neighbourhood',
        dcc.Dropdown(
            id='data_filter', value='SUNSET',
            options=[{'label': i, 'value': i} for i in trees.NEIGHBOURHOOD_NAME.unique()]
            ),
        html.Iframe(
            id='bar',
            style={'border-width': '0', 'width': '100%', 'height': '800px'}
            ) 
        ])
            
@app.callback(
    Output('bar', 'srcDoc'),
    Input('data_filter', 'value'))
##Create Cultivar Chart
def create_plot(neighbourhood):
    tree_plot = alt.Chart(trees[trees['NEIGHBOURHOOD_NAME'] == neighbourhood]).mark_bar().encode(
        x=alt.X('count()', axis=alt.Axis(title='Number of Trees')),
        y=alt.Y('COMMON_NAME:N', axis=alt.Axis(title='Tree Name'),
        sort=alt.EncodingSortField(op='count', order='descending')),
        tooltip='count()'
 #   ).transform_filter(
 #       (datum.count > 10)
    ).configure_mark(
        opacity=0.6,
        color='pink'
    ).interactive()

    return tree_plot.to_html()
if __name__ == '__main__':
    app.run_server(debug=True)