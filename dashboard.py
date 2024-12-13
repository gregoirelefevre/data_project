# Install necessary libraries: dash, pandas, plotly
# pip install dash pandas plotly

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Sample data
data = {
    'Category': ['A', 'B', 'C', 'D'],
    'Value': [10, 15, 13, 17]
}
df = pd.DataFrame(data)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Simple Dashboard", style={'text-align': 'center'}),
    
    html.Label("Select Category:"),
    dcc.Dropdown(
        id='category-filter',
        options=[{'label': cat, 'value': cat} for cat in df['Category']],
        value=None,
        placeholder="All Categories",
    ),
    
    dcc.Graph(id='bar-chart'),
])

# Callback to update chart
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('category-filter', 'value')]
)
def update_chart(selected_category):
    if selected_category:
        filtered_df = df[df['Category'] == selected_category]
    else:
        filtered_df = df
    fig = px.bar(filtered_df, x='Category', y='Value', title='Bar Chart')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
