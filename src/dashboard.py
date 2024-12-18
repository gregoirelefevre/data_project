import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import webbrowser
import folium


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
    # Création de la carte centrée sur le monde
    folium_map = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron")

    # Ajouter des marqueurs pour chaque pays
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
            icon=folium.Icon(color="blue", icon="info-sign"),
        ).add_to(folium_map)

    return folium_map

def save_folium_map():
    folium_map = create_folium_map()
    folium_map.save("folium_map.html")

#
# Création du style et des composants du dashboard
#
def init_app(app):
    app.title = "Jeux Olympiques 2024"
    save_folium_map()

    app.layout = html.Div(style={'backgroundColor': colors['background'], 'padding': '0px'},
                          children=[
                            html.H1(children=f'Analyse des Jeux Olympiques 2024',
                                    style={'textAlign': 'center', 'color': colors['black'], 'fontSize': '85px', 'marginBottom': '10px'}),
                            html.Img(src="https://upload.wikimedia.org/wikipedia/commons/5/5c/Olympic_rings_without_rims.svg", style={'width': '400px', 'height': 'auto', 'display': 'block', 'margin': '0 auto'}), 
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
                            html.H1("Carte des pays participants", style={'textAlign': 'center', 'color': '#000000', 'fontSize': '45px', 'marginTop': '100px'}),
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
                                    else '#CD7F32']  # Couleur basée sur la sélection
        )
        # Mise en forme du graphique
        fig.update_layout(
            plot_bgcolor='#ffffff',  # Fond du graphique
            paper_bgcolor='#ffffff',  # Fond global
            font_color='#000000',  # Couleur du texte
            title_font_size=20
        )
        return fig
