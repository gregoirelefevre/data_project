from src.cleandata import countries_involved, countries_medals, hist_data
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import folium
import dash_bootstrap_components as dbc
import json

#
# Data
#
data = pd.DataFrame({
    "Pays": ["USA", "Chine", "Japon", "France", "Allemagne"],
    "Skateboarding": [39, 38, 27, 10, 10],
    "Boxing": [41, 32, 14, 12, 11],
    "Archery": [33, 18, 17, 7, 16],
    "Latitude": [37.0902, 35.8617, 36.2048, 46.6034, 51.1657],
    "Longitude": [-95.7129, 104.1954, 138.2529, 2.2137, 10.4515]
})

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
# Création de la map
#
def create_folium_map():
    # Chargement des frontières
    with open("data/countries.geojson", "r") as geojson_file:
        geojson_data = json.load(geojson_file)
    
    # Style de remplissage pour les pays
    def style_function(feature):
        country_name = feature["properties"]["ADMIN"]
        country_code = feature["properties"]["ISO_A3"]
        if country_code in countries_medals or country_name in [v["name"] for v in countries_medals.values()]:
            return {
                "fillColor": "#006400",  # Vert foncé pour les médaillés
                "color": "#006400",      # Bordures vertes 
                "fillOpacity": 0.1 + 0.5*(1-countries_medals[country_code]["rank"]/100),      # Opacité du remplissage
                "weight": 1
            }
        elif country_code in countries_involved or country_name in countries_involved:
            return {
                "fillColor": "#006400",  # Vert canard pour les autres
                "color": "#006400",      # Bordures Vertes 
                "fillOpacity": 0.1,      # Opacité du remplissage
                "weight": 1
            }
        else:
            return {
                "fillColor": "#8B0000",  # Rouge foncé pour les non participants
                "color": "#8B0000",      # Bordures rouge foncé
                "fillOpacity": 0.3,      # Opacité du remplissage
                "weight": 1,             # Épaisseur des bordures
            }

    # Création de la carte
    folium_map = folium.Map(location=[20, 0], zoom_start=2, max_bounds=True, min_zoom=2, max_zoom=20, tiles="CartoDB positron")
    folium_map.fit_bounds([[-60, -180], [85, 180]]) # Ajout des limites

    
    # Appliquer les styles aux pays via GeoJSON
    folium.GeoJson(
        geojson_data,
        style_function=style_function
    ).add_to(folium_map)

    # Ajout des messages au survol des pays
    for feature in geojson_data['features']:
        country_name = feature['properties']['ADMIN']
        country_code = feature['properties']['ISO_A3']
        
        # Créer le contenu du message pour les pays médaillés
        if country_code in countries_medals or country_name in [v["name"] for v in countries_medals.values()]:
            result = countries_medals.get(country_code, countries_medals.get(country_name, {}))
            tooltip_content = f"""
            <div style="background-color: #006400; color: white; padding: 10px; border-radius: 5px; font-size: 14px; font-weight: bold;">
                <strong style="font-size: 20px;">{country_name}</strong><br>
                <span style="color: yellow;">Or: {result.get('gold', 0)}</span><br>
                <span style="color: silver;">Argent: {result.get('silver', 0)}</span><br>
                <span style="color: #cd7f32;">Bronze: {result.get('bronze', 0)}</span><br>
                <span style="color: #FFFFFF;">Rang: {result.get('rank', 0)}</span>
            </div>
            """
        elif country_code in countries_involved or country_name in countries_involved:
            tooltip_content = f"""
            <div style="background-color: #808080; color: white; padding: 10px; border-radius: 5px; font-size: 14px; font-weight: bold;">
                <strong style="font-size: 20px;">{country_name}</strong><br>
                <span style="color: #FFFFFF;">Aucune Medaille</span>
            </div>
            """
        else:
            tooltip_content = f"""
            <div style="background-color: #c26262; color: white; padding: 10px; border-radius: 5px; font-size: 14px; font-weight: bold;">
                <strong style="font-size: 20px;">{country_name}</strong><br>
                <span style="color: #FFFFFF;">Non Participant</span>
            </div>
            """

        # Ajouter le message pour ce pays
        folium.GeoJson(
            feature,
            style_function=style_function,
            tooltip=folium.Tooltip(tooltip_content)
        ).add_to(folium_map)
    
    return folium_map
def save_folium_map():
    folium_map = create_folium_map()
    folium_map.save("folium_map.html")

#
# Création du composant Histogramme
#
def create_hist_view():
    return html.Div(
        className="hist-view",
        children=[
            html.Label(
                "Sélectionnez un Sport :",
                className="hist-label"
            ),
            dcc.Dropdown(
                id='dropdown-sports',
                options=[{'label': sport, 'value': sport} for sport in hist_data],
                value='All',  # Valeur par défaut
                placeholder="Sélectionnez un sport",  # Texte de remplacement
                className='hist-dropdown',
                clearable=True  # Permet de retirer la sélection
            ),
            dcc.Graph(
                id='histogram',
                className='hist-graph'
            ),
            html.H3(
                children='''
                    Cet Histogramme représente la répartition des athlètes en fonction de leurs âge dans la discipline sélectionnée
                ''',
                className='hist-description'
            ),
        ]
    )


def create_map_view():
    return html.Div(
        children=[
            html.H1("Carte des pays participants", style={'textAlign': 'center', 'color': '#000000', 'fontSize': '45px', 'marginTop': '10px'}),
            
            html.Div(
                className='main-container',
                children=[
                    html.Div(
                        id='map-div',
                        className='map',
                        children=[
                            html.Iframe(
                                id='folium-map',
                                srcDoc=open("folium_map.html", "r").read(),
                                width='100%',  # Make the map fill its container
                                height='500'
                            )
                        ]
                    ),

                    # Légende Div
                    html.Div(
                        id='legend-div',
                        className='legend',
                        children=[
                            html.Div(className='legend-item', children=[
                                html.Div(className='legend-box medalled'),
                                html.Span("Rang du pays (1-93)")
                            ]),
                            html.Div(className='legend-item', children=[
                                html.Div(className='legend-line in'),
                                html.Span("Pays participants")
                            ]),
                            html.Div(className='legend-item', children=[
                                html.Div(className='legend-line not_in'),
                                html.Span("Pays non participants")
                            ]),
                            html.Div(className='legend-item', children=[
                                html.Span("\"Les résultats des pays s'affiche au survol de la souris\"")
                            ])
                        ]
                    ),
                ],
                style={
                    'display': 'flex',
                    'justifyContent': 'space-between',  # Space between the map and the legend
                    'width': '100%',
                }
            ),
            html.Div(
                children=[
                    html.H3("Cette carte représente les pays participants aux JO 2024, ainsi que leurs résultats respectifs.")
                ]
            )
        ]
    )
# Création du style et des composants du dashboard
#
def init_app(app):
    app.title = "Jeux Olympiques 2024"
    save_folium_map()
    histogram_view = create_hist_view()
    map_view = create_map_view()

    app.layout = html.Div(style={'backgroundColor': colors['background']},
         children=[
             html.H1(children='Analyse des Jeux Olympiques 2024', className='olympic-title'), 
             # Menu de navigation avec boutons stylisés, using Flexbox to position buttons on each side
            
            html.Div(
                 children=[
                     dbc.Button(
                         "Histogramme", id="show-histogram", color="primary", className="mr-2", n_clicks=0,
                         style={'fontSize': '24px', 'padding': '10px 20px', 'borderRadius': '40px'}
                     ),
                     html.Img(src="https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg", 
                    style={'width': '100%', 'max-width' : '400px', 'height': 'auto', 'display': 'block', 'margin': '0 auto'}),
                     dbc.Button(
                         "Carte", id="show-map", color="primary", className="mr-2", n_clicks=0,
                         style={'fontSize': '24px', 'padding': '10px 20px', 'borderRadius': '40px'}
                     ),
                 ],
                 style={
                     'display': 'flex',           # Flexbox to align items
                     'justifyContent': 'space-between',  # Space buttons evenly with space between them
                     'alignItems': 'center',     # Vertically center the buttons
                     'width': '80%',             # Ensure buttons don't take full width
                     'margin': '0 auto',         # Center the flex container
                     'margin-top': '40px'         # Add some space from the image
                 }
             ),
             
             # Conteneur pour afficher l'histogramme ou la carte
             html.Div(className='contentHistMap', id='content', children=[]),
             
             html.H1("", style={'marginTop': '50px'})
         ]
)

    #
    # Maj du site quand on appuie sur un bouton de navigation
    # 
    @app.callback(
        Output('content', 'children'),
        Input('show-histogram', 'n_clicks'),
        Input('show-map', 'n_clicks')
    )
    def update_view(histogram_clicks, map_clicks):
        if histogram_clicks > map_clicks:
            return histogram_view
        else:
            return map_view
    #
    # Maj de l'histogramme quand on séléctionne un sport
    # 
    @app.callback(
        Output('histogram', 'figure'),
        Input('dropdown-sports', 'value')
    )
    def update_histogram(selected_sport):
        if selected_sport is None:
            selected_sport = "All"
        # Créer un histogramme basé sur la sélection
        fig = px.bar(
            hist_data[selected_sport],
            x=hist_data[selected_sport]["age"],
            y=hist_data[selected_sport]["nb"],
            title=f"Répartition des Athlètes : {selected_sport}",
            labels={"x": "Âge", "y": "Nombre d'Athlètes"},
            color_discrete_sequence=['#FFD700']  # Couleur sélection
        )
        # Mise en forme du graphique
        fig.update_layout(
            plot_bgcolor='#ffffff',  # Fond du graphique
            paper_bgcolor='#ffffff',  # Fond global
            font_color='#000000',  # Couleur du texte
            title_font_size=20
        )

        # Personnalisation du style
        fig.update_layout(
            plot_bgcolor='#f9f9f9',  # Fond du graphique
            paper_bgcolor='#f9f9f9',  # Fond global
            font=dict(
                size=14,
                color='#4d4d4d'
            ),
            title=dict(
                font_size=20,
                x=0.5,  # Centrer le titre
            ),
            xaxis=dict(
                title=dict(font_size=16),
                tickfont=dict(size=12),
                gridcolor='lightgrey'
            ),
            yaxis=dict(
                title=dict(font_size=16),
                tickfont=dict(size=12),
                gridcolor='lightgrey'
            ),
            margin=dict(l=40, r=40, t=50, b=40),  # Marges ajustées
        )
        return fig

if __name__ == "__main__":
    app = dash.Dash(__name__, suppress_callback_exceptions=True)
    init_app(app)