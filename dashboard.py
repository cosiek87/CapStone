# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
sites = np.append(spacex_df['Launch Site'].unique(), 'All sites')[::-1]
sites_dict  = [{'label': i, 'value': i} for i in sites]
# Create a dash application
app = dash.Dash(__name__)
print([min_payload,max_payload])
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options = sites_dict, value = 'All sites', placeholder = 'Select a Launch Site here', searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider', min = 0, max = 10000, 
                                                step = 1000, value = [min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

def get_piechart(site):
    if site == 'All sites':
        pie_fig = px.pie(spacex_df[['class','Launch Site']].groupby(by='Launch Site').sum().reset_index(), values='class', names='Launch Site', title='Total success launches')
    else:
        pie_fig = px.pie(spacex_df[spacex_df['Launch Site']==site]['class'], names='class', title='Launches outcome')
    return pie_fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatterplot(site, payload):
    payload_spacex_df = spacex_df[spacex_df['Payload Mass (kg)'].between(left=payload[0],right=payload[1]) ]
    if site == 'All sites':
        scatt_fig = px.scatter(payload_spacex_df, x='Payload Mass (kg)', y='class', color = 'Booster Version Category', title='Correlation between Payload and Success for all Sites')
    else:
        scatt_fig = px.scatter(payload_spacex_df[payload_spacex_df['Launch Site']==site], x='Payload Mass (kg)', y='class', 
        color = 'Booster Version Category', title='Correlation between Payload and Success for {} Sites'.format(site))
    return scatt_fig
# Run the app
if __name__ == '__main__':
    app.run_server()
