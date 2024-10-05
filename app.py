# import dash
# from dash import Dash, Input, Output, dcc, html
# import dash_bootstrap_components as dbc
# import plotly.express as px
# import pandas as pd

# app = Dash(__name__, external_stylesheets = [dbc.themes.VAPOR], use_pages=True)

# fips_data = pd.read_excel('US_FIPS_Codes.xls',skiprows=1)
# print(fips_data.columns)

# states = fips_data['State'].unique()


# app = dash.Dash(__name__)

# app.layout = html.Div([
    
#     dcc.Dropdown(
#         id='state-dropdown',
#         options=[{'label': state, 'value': state} for state in states],
#         placeholder="Select a state"
#     ),
    
#     dcc.Dropdown(
#         id='county-dropdown',
#         placeholder="Select a county"
#     ),

#     html.Div(id='fips-output')
# ])

# @app.callback(
#     Output('county-dropdown', 'options'),
#     Input('state-dropdown', 'value')
# )
# def update_county_dropdown(selected_state):
#     if selected_state is None:
#         return []
    
#     filtered_counties = fips_data[fips_data['State'] == selected_state]
#     return [{'label': county, 'value': county} for county in filtered_counties['County Name']]

# @app.callback(
#     Output('fips-output', 'children'),
#     [Input('state-dropdown', 'value'),
#      Input('county-dropdown', 'value')]
# )

# def display_fips(selected_state, selected_county):
#     if selected_state and selected_county:
#         # Filter the corresponding FIPS and county code
#         selected_row = fips_data[(fips_data['State'] == selected_state) &
#                                  (fips_data['County Name'] == selected_county)]
#         fips_code = selected_row['FIPS State'].values[0]
#         county_code = selected_row['FIPS County'].values[0]
        
#         return f"FIPS Code: {fips_code}, County Code: {county_code}"
#     return ""


# if __name__ == '__main__':
#     app.run_server(debug=True)

from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app_init import app  # Import app from the initialization file

# Main Page Layout
main_page_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Welcome to the Analysis Dashboard", style={'textAlign': 'center'}),
            html.Br(),
            dbc.Button("Age Analysis", id="age-analysis-btn", color="primary", size="lg", className="mr-2"),
            dbc.Button("Year Analysis", id="year-analysis-btn", color="secondary", size="lg")
        ], width={"size": 6, "offset": 3})
    ]),
])

# Import page layouts from pages
from pages.age import layout as age_layout
from pages.year import layout as year_layout

# Main app layout with dynamic page loading
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Callback to handle button clicks and redirect to the correct page
@app.callback(
    Output('url', 'pathname'),
    [Input('age-analysis-btn', 'n_clicks'),
     Input('year-analysis-btn', 'n_clicks')]
)
def navigate_page(n_age, n_year):
    if n_age:
        return '/age'
    elif n_year:
        return '/year'
    return '/'

# Callback to display the correct page content based on URL
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/age':
        return age_layout  # Age analysis page
    elif pathname == '/year':
        return year_layout  # Year analysis page
    else:
        return main_page_layout  # Main page layout

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port =8056)
