# app_init.py

import dash
import pandas as pd
import dash_bootstrap_components as dbc

# Load FIPS data
fips_data = pd.read_excel('US_FIPS_Codes.xls',skiprows=1)

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
