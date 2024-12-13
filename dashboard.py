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
    app.title = "Olympic Games 2024"
    fig = px.scatter(data[year], x="gdpPercap", y="lifeExp",
                        color="continent",
                        size="pop",
                        hover_name="country")
    app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '20px'},
                          children=[

                            html.H1(children=f'Data analysis of the 2024 Olympic Games',
                                        style={'textAlign': 'center', 'color': colors['blue'], 'font-family': 'Gotham'}),
                            
                            html.Label('Year'),
                            dcc.Dropdown(
                                id="year-dropdown",
                                options=[
                                    {'label': '1952', 'value': 1952},
                                    {'label': '1957', 'value': 1957},
                                    {'label': '1962', 'value': 1962},
                                    {'label': '1967', 'value': 1967},
                                    {'label': '1972', 'value': 1972},
                                    {'label': '1977', 'value': 1977},
                                    {'label': '1982', 'value': 1982},
                                    {'label': '1987', 'value': 1987},
                                    {'label': '1992', 'value': 1992},
                                    {'label': '1997', 'value': 1997},
                                    {'label': '2002', 'value': 2002},
                                    {'label': '2007', 'value': 2007},
                                ],
                                value=2007,
                            ),

                            dcc.Graph(
                                id='graph1',
                                figure=fig
                            ), # (6)

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