import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import webbrowser
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
    # Charger les frontières géographiques (GeoJSON)
    with open("src/countries.geojson", "r") as geojson_file:
        geojson_data = json.load(geojson_file)

    # Liste des pays à griser
    countries_to_gray = ["Anguilla", "Bermuda", "Cayman Islands", "British Virgin Islands", "United States Virgin Islands", "Hong Kong S.A.R.", "Macao S.A.R", "Palestine", "North Korea", "Vatican", "Russia", "Belarus", "Antarctica", "Greenland"]

    # Définir un style pour les pays
    def style_function(feature):
        if feature["properties"]["ADMIN"] in countries_to_gray:
            return {
                "fillColor": "#8B0000",  # Rouge foncé
                "color": "#8B0000",      # Bordures rouge foncé
                "fillOpacity": 0.3,      # Opacité du remplissage
                "weight": 1,             # Épaisseur des bordures
            }
        else:
            return {
                "fillColor": "#006400",  # Vert pour les autres
                "color": "#006400",      # Bordures vertes
                "fillOpacity": 0.3,      # Opacité du remplissage
                "weight": 1
            }

    # Création de la carte
    folium_map = folium.Map(location=[20, 0], zoom_start=2, max_bounds=True, min_zoom=2, max_zoom=20, tiles="CartoDB positron")
    folium_map.fit_bounds([[-60, -180], [85, 180]]) # Ajout des limites

    # Appliquer les styles aux pays via GeoJSON
    folium.GeoJson(
        geojson_data,
        style_function=style_function
    ).add_to(folium_map)

    # Ajout des marqueurs pour chaque pays
    for _, row in data.iterrows():
        popup_text = f"""
        <strong>{row['Pays']}</strong><br>
        <strong>Skateboarding:</strong> {row['Skateboarding']}<br>
        <strong>Boxing:</strong> {row['Boxing']}<br>
        <strong>Archery:</strong> {row['Archery']}
        """
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=folium.Popup(popup_text, max_width=200),
            icon=folium.Icon(color="black", icon="info-sign"),
        ).add_to(folium_map)
    
    return folium_map

def save_folium_map():
    folium_map = create_folium_map()
    folium_map.save("folium_map.html")

#
# Création des composants du dashboard : Histogramme
#
def create_hist_view():
    return html.Div(
                        children=[
                            html.Label("Sélectionnez un Sport :",
                                    style={'fontSize': '35px', 'fontWeight': 'bold', 'marginTop': '20px'}),
                            dcc.Dropdown(
                                id='dropdown-sports',
                                options=[
                                    {'label': 'Skateboarding', 'value': 'Skateboarding'},
                                    {'label': 'Boxing', 'value': 'Boxing'},
                                    {'label': 'Archery', 'value': 'Archery'},
                                ],
                                value='Skateboarding',
                                style={'width': '200px'}
                            ),
                            dcc.Graph(
                                id='histogram',
                                style={'flexGrow': 1}
                            ),

                            html.Div(children=f'''
                                Cet Histogramme représente la répartition des athlètes en fonction de leurs âge dans la discipline sélectionnée
                            ''', style={'textAlign': 'center', 'fontSize': '20px'}),
                        ]
                    )

#
# Création des composants du dashboard : Map
#
def create_map_view():
    return html.Div(
                    children=[
                        html.H1("Carte des pays participants", style={'textAlign': 'center', 'color': '#000000', 'fontSize': '45px', 'marginTop': '10px'}),
                        html.Div(  # Conteneur pour centrer l'Iframe
                            children=[
                                html.Iframe(
                                    id='folium-map',
                                    srcDoc=open("folium_map.html", "r").read(),
                                    width='60%',
                                    height='500'
                                )
                            ],
                            style={
                                'display': 'flex',         
                                'justifyContent': 'center',  
                                'alignItems': 'center',    
                                'height': '470px'       
                            }
                        ),
                        html.Div(children=f'''
                            Cette carte représente les pays participants aux JO 2024, ainsi que leurs résultats respectifs
                        ''', style={'textAlign': 'center', 'fontSize': '20px', 'marginTop': '25px'})
                    ]
                )

#
# Création du style et des composants du dashboard
#
def init_app(app):
    app.title = "Jeux Olympiques 2024"
    save_folium_map()
    histogram_view = create_hist_view()
    map_view = create_map_view()

    app.layout = html.Div(style={'backgroundColor': colors['background']},
                          children=[
                            html.H1(children=f'Analyse des Jeux Olympiques 2024',
                                    style={'textAlign': 'center', 'color': colors['black'], 'fontSize': '85px', 'marginBottom': '10px'}),
                            html.Img(src="https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg", style={'width': '400px', 'height': 'auto', 'display': 'block', 'margin': '0 auto'}), 
                            # Menu de navigation avec boutons stylisés
                            html.Div(
                                children=[
                                    dbc.Button(
                                        "Histogramme", id="show-histogram", color="primary", className="mr-2", n_clicks=0,
                                        style={'fontSize': '18px', 'padding': '10px 20px', 'borderRadius': '12px'}
                                    ),
                                    html.Label("         "),
                                    dbc.Button(
                                        "Carte", id="show-map", color="primary", className="mr-2", n_clicks=0,
                                        style={'fontSize': '18px', 'padding': '10px 20px', 'borderRadius': '12px'}
                                    ),
                                ],
                                style={'textAlign': 'center', 'marginTop': '20px'}
                            ),
                            # Conteneur pour afficher l'histogramme ou la carte
                            html.Div(id='content', children=[]),
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
        # Créer un histogramme basé sur la sélection
        fig = px.bar(
            data,
            x="Pays",
            y=selected_sport,
            title=f"Répartition des Athlètes : {selected_sport}",
            labels={"Pays": "Pays", selected_sport: "Nombre de médailles"},
            color_discrete_sequence=['#FFD700' if selected_sport == 'Skateboarding'
                                    else '#C0C0C0' if selected_sport == 'Boxing'
                                    else '#CD7F32']  # Couleur sélection
        )
        # Mise en forme du graphique
        fig.update_layout(
            plot_bgcolor='#ffffff',  # Fond du graphique
            paper_bgcolor='#ffffff',  # Fond global
            font_color='#000000',  # Couleur du texte
            title_font_size=20
        )
        return fig