# pages/age.py

from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from app_init import app, fips_data  # Import from app_init.py

# Define the layout for the Age Analysis page
states = fips_data['State'].unique()
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='state-dropdown-age',
                options=[{'label': state, 'value': state} for state in states],
                placeholder="Select a state"
            ),
            dcc.Dropdown(
                id='county-dropdown-age',
                placeholder="Select a county"
            ),
            dcc.Dropdown(
                id='year-dropdown',
                options=[{'label': year, 'value': year} for year in [2002, 2007, 2012, 2017, 2022]],
                placeholder="Select a year"
            ),
        ], width={"size": 4, "offset": 8})
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Slider(
                id='age-slider',
                min=0,
                max=5,
                marks={
                    0: '<30', 1: '30-40', 2: '40-50',
                    3: '50-60', 4: '60-70', 5: '70+'
                },
                value=2,
                step =1
            )
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='fips-output-year', style={'marginTop': '20px'})  # This is where the output will be shown
        ], width=12)
    ])
])

# Register the callback for updating county dropdown
@app.callback(
    Output('county-dropdown-age', 'options'),
    Input('state-dropdown-age', 'value')
)
def update_county_dropdown(selected_state):
    if selected_state is None:
        return []
    filtered_counties = fips_data[fips_data['State'] == selected_state]
    return [{'label': county, 'value': county} for county in filtered_counties['County Name']]

@app.callback(
    Output('fips-output-year', 'children'),
    [Input('state-dropdown-age', 'value'),
     Input('county-dropdown-age', 'value'),
     Input('year-dropdown','value'),
     Input('age-slider','value'),]
)

def display_fips1(selected_state, selected_county,selected_age,selected_year):
    if selected_state and selected_county:
        # Filter the corresponding FIPS and county code
        selected_row = fips_data[(fips_data['State'] == selected_state) &
                                 (fips_data['County Name'] == selected_county)]
        fips_code = selected_row['FIPS State'].values[0]
        county_code = selected_row['FIPS County'].values[0]
        
        return f"FIPS Code: {fips_code}, County Code: {county_code}, Age: {selected_age}, Year: {selected_year}"
    return ""