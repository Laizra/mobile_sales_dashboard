""" module to manipulate data """
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Import and clean data (importing csv into pandas)
df = pd.read_csv("Sales.csv")
dff = df.copy()
dff['Brands'] = dff['Brands'].str.upper()
un = dff["Brands"].unique().tolist()

# Plotly Express to show bar chart
fig = px.bar(dff, x='Selling Price', y='Rating',
             template='plotly_dark',
             labels={'x': 'Selling Price', 'y': 'Rating'},
             barmode='group')

# Setup options dynamically
list_options = [{'label': u, 'value': u} for u in un]

# app layout
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            options=list_options,
            placeholder="Select a brand",
            id="my-dynamic-dropdown",
            value='SAMSUNG',
            style={"width": "60%", 'fontFamily': 'Arial'}
            ),

        html.Div(id='output_container', children=[]),
        html.Br(),

        dcc.Graph(id="bars", figure={})
    ]),
])

# callback and function to retrive value and children
@app.callback(
    Output("bars","figure"),
    [Input("my-dynamic-dropdown", "value")]
)
def update_output(selected_brand):
    """ displays text under dropdown indicating selected option """

    # Filter data based on selected brand
    filtered_df = dff[dff['Brands'] == selected_brand]

    # Update bar chart with filtered data
    updated_fig = px.scatter(filtered_df, x='Selling Price', y='Rating',
                             hover_data={'Models': True},
                             title = "Rating and Selling Price of Smartphones by brand",
                             template='plotly_dark')

    return updated_fig

# run server
if __name__ == '__main__':
    app.run_server(debug=True)
