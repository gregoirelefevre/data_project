from src.get_dataset import getdata 
from src.dashboard import init_app
from src.cleandata import clean_data_histo, load_country, load_ranking

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import webbrowser


def main():
    getdata()
    clean_data_histo()
    load_country()
    load_ranking()
    app = dash.Dash(__name__, suppress_callback_exceptions=True)
    init_app(app)
    webbrowser.open('http://127.0.0.1:8050/')
    app.run_server(debug=True)




if __name__ == "__main__":
    main()