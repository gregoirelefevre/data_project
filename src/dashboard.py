from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Data
year = 2002
gapminder = px.data.gapminder()
years = gapminder["year"].unique()
data = {year: gapminder.query("year == @year") for year in years}

colors = {
    'background': '#f7f7f7',
    'text': '#000000',
    'blue': '#0085C7',
    'yellow': '#FFD700',
    'black': '#000000',
    'green': '#00A651',
    'red': '#EF3340'
}

def init_app(app):
    app.title = "Jeux Olympiques 2024"

    fig = px.scatter(data[year], x="gdpPercap", y="lifeExp",
                     color="continent",
                     size="pop",
                     hover_name="country")

    app.layout = html.Div(
        style={'backgroundColor': colors['background'], 'padding': '0px'},
        children=[
            html.H1(
                children='Analyse des Jeux Olympiques 2024',
                style={'textAlign': 'center', 'color': colors['black'], 'fontSize': '50px', 'marginBottom': '10px'}
            ),
            html.Img(
                src="https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg",
                style={'width': '400px', 'height': 'auto', 'display': 'block', 'margin': '0 auto'}
            ),
            html.Label(
                "Sélectionnez un Sport :",
                style={'fontSize': '18px', 'fontWeight': 'bold'}
            ),
            dcc.Dropdown(
                id='dropdown-medals',
                options=[
                    {'label': 'Or', 'value': 'Or'},
                    {'label': 'Argent', 'value': 'Argent'},
                    {'label': 'Bronze', 'value': 'Bronze'},
                ],
                value='Or',
                style={'width': '500px'}
            ),
            dcc.Graph(
                id='graph1',
                figure=fig
            ),
            html.Div(children=f'''
                The graph above shows relationship between life expectancy and
                GDP per capita for year {year}. Each continent data has its own
                colour and symbol size is proportionnal to country population.
                Mouse over for details.
            '''),
        ]
    )

    # Callback for updating the graph
    @app.callback(
        Output(component_id='graph1', component_property='figure'),
        [Input(component_id='dropdown-medals', component_property='value')]
    )
    def update_figure(input_value):
        return px.scatter(
            data[year], x="gdpPercap", y="lifeExp",
            color="continent",
            size="pop",
            hover_name="country"
        )
