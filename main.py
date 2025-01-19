#imports 
from src.utils.get_dataset import getdata
from src.dashboard import init_app
import dash
import webbrowser

def main():
    #getdata() récupère les données et les charge dans 'data/raw'
    print("Récupération des données...")
    getdata()
    print("Lancement de l'application...")
    #initialise l'application
    app = dash.Dash(__name__, suppress_callback_exceptions=True)
    init_app(app)

    # Ouvre le navigateur web automatiquement
    webbrowser.open('http://127.0.0.1:8050/')
    app.run_server(debug=False)  # Désactiver debug pour éviter le double chargement

if __name__ == "__main__":
    main()
