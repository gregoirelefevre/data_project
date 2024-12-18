from src.get_dataset import getdata 
from src.dashboard import init_app
import webbrowser
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

def main():
    getdata()
    app = dash.Dash(__name__)
    init_app()
    webbrowser.open('http://127.0.0.1:8050/')
    app.run_server(debug=True)




if __name__ == "__main__":
    main()