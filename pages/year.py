from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from app_init import app, fips_data

# Extract unique states for the first dropdown
states = fips_data['State'].unique()

# Layout for the year page
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='state-dropdown-year',
                options=[{'label': state, 'value': state} for state in states],
                placeholder="Select a state"
            ),
            dcc.Dropdown(
                id='county-dropdown-year',
                placeholder="Select a county"
            ),
            
            dcc.Dropdown(
                id='age-dropdown',
                options=[{'label': age, 'value': age} for age in ['<30','30-40','40-50','50-60','60-70','70>']],
                placeholder="Select age"
            )
        ], width={"size": 4, "offset": 8})  
    ]),
    dbc.Row([
        dbc.Col([
            html.Img(
                id='central-image',
                src='',  # Add your image source later
                style={'width': '100%', 'height': 'auto'}
            )
        ], width={"size": 6, "offset": 3}, style={'textAlign': 'center', 'marginTop': '50px'})
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Slider(
                id='year-slider',
                min=2002,
                max=2022,
                step=5,
                marks={2002: '2002', 2007: '2007', 2012: '2012', 2017: '2017', 2022: '2022'},
                value=2012
            )
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='fips-output', style={'marginTop': '20px'})  # This is where the output will be shown
        ], width=12)
    ])
])

@app.callback(
    Output('county-dropdown-year', 'options'),
    Input('state-dropdown-year', 'value')
)
def update_county_dropdown(selected_state):
    if selected_state is None:
        return []
    filtered_counties = fips_data[fips_data['State'] == selected_state]
    return [{'label': county, 'value': county} for county in filtered_counties['County Name']]


@app.callback(
    Output('fips-output', 'children'),
    [Input('state-dropdown-year', 'value'),
     Input('county-dropdown-year', 'value'),
     Input('age-dropdown','value'),
     Input('year-slider','value')]
)

def display_fips2(selected_state, selected_county,selected_age,selected_year):
    if selected_state and selected_county:
        # Filter the corresponding FIPS and county code
        selected_row = fips_data[(fips_data['State'] == selected_state) &
                                 (fips_data['County Name'] == selected_county)]
        fips_code = selected_row['FIPS State'].values[0]
        county_code = selected_row['FIPS County'].values[0]
        
        return f"FIPS Code: {fips_code}, County Code: {county_code}, Age: {selected_age}, Year: {selected_year}"
    return ""