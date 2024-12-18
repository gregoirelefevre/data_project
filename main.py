from src.get_dataset import getdata 
from src.dashboard import init_app
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import webbrowser

def main():
    getdata()
    app = dash.Dash(__name__)
    init_app(app)
    webbrowser.open('http://127.0.0.1:8050/')
    app.run_server(debug=True)




if __name__ == "__main__":
    main()