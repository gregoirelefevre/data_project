from src.get_dataset import getdata 
from src.dashboard import init_app
from src.cleandata import clean_data_histo

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import webbrowser


def main():
    getdata()
    clean_data_histo('data/raw/27/athletes.csv')
    app = dash.Dash(__name__)
    init_app(app)
    webbrowser.open('http://127.0.0.1:8050/')
    app.run_server(debug=True)




if __name__ == "__main__":
    main()