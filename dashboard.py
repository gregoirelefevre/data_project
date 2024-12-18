import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import webbrowser

app = dash.Dash(__name__)

#
# Data
#
year = 2002
gapminder = px.data.gapminder() # (1)
years = gapminder["year"].unique()
data = { year:gapminder.query("year == @year") for year in years} # (2)

colors = {
    'background': '#f7f7f7',  # Blanc cassé (fond)
    'text': '#000000',        # Noir (texte)
    'blue': '#0085C7',        # Bleu olympique
    'yellow': '#FFD700',      # Jaune olympique
    'black': '#000000',       # Noir olympique
    'green': '#00A651',       # Vert olympique
    'red': '#EF3340'          # Rouge olympique
}

#
# Création du style et des composants du dashboard
#
def init_app():
    app.title = "Jeux Olympiques 2024"

    fig = px.scatter(data[year], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country")

    app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '0px'},
                          children=[
                            html.H1(children=f'Analyse des Jeux Olympiques 2024',
                                    style={'textAlign': 'center', 'color': colors['black'], 'fontSize': '50px', 'marginBottom': '10px'}),
                            html.Img(src="https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg", style={'width': '400px', 'height': 'auto', 'display': 'block', 'margin': '0 auto'}), 
                            html.Label("Sélectionnez un Sport :",
                                   style={'fontSize': '18px', 'fontWeight': 'bold'}),
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

#
# Maj de l'histogramme quand on séléctionne un sport
# 
@app.callback(
    Output(component_id='graph1', component_property='figure'),
    [Input(component_id='year-dropdown', component_property='value')]
)
def update_figure(input_value):
    return px.scatter(data[input_value], x="gdpPercap", y="lifeExp",
                    color="continent",
                    size="pop",
                    hover_name="country") 

#
# Main
#
if __name__ == '__main__':
    #
    # RUN APP
    #
    init_app()
    webbrowser.open('http://127.0.0.1:8050/')
    app.run_server(debug=True)