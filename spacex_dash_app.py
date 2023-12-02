# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

dropdown_options=[{'label': 'All Sites', 'value': 'ALL'},
                  {'label': spacex_df['Launch Site'].unique()[0], 'value': spacex_df['Launch Site'].unique()[0]},
                  {'label': spacex_df['Launch Site'].unique()[1], 'value': spacex_df['Launch Site'].unique()[1]},
                  {'label': spacex_df['Launch Site'].unique()[2], 'value': spacex_df['Launch Site'].unique()[2]},
                  {'label': spacex_df['Launch Site'].unique()[3], 'value': spacex_df['Launch Site'].unique()[3]}]

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', 
                                             options=dropdown_options, 
                                             value='ALL', 
                                             placeholder='Select a Launch Site here', 
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                      2500: '2500',
                                                      5000: '5000',
                                                      7500: '7500',
                                                      10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df[(spacex_df['Launch Site']==entered_site)]
    if entered_site == 'ALL':
        suc_data = spacex_df[['Launch Site','class']][spacex_df['class']==1].groupby(['Launch Site']).count().reset_index()
        fig = px.pie(suc_data, values='class', names=suc_data['Launch Site'], title='Total successful launches by site')
        return fig
    else:
        suc_data_site = filtered_df[['Launch Site','class']].groupby(['class']).count().reset_index()
        fig = px.pie(suc_data_site, values='Launch Site', names=suc_data_site['class'], title='Total successful launches in' + entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))

def get_scatter_chart(entered_site, selected_payload):
    filtered_df = spacex_df[(spacex_df['Launch Site']==entered_site) & 
                            (spacex_df['Payload Mass (kg)'] >= selected_payload[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= selected_payload[1])]
    if entered_site == 'ALL':
        suc_data_scatter = spacex_df[['Payload Mass (kg)', 'Booster Version Category', 'Booster Version', 'class']][(spacex_df['Payload Mass (kg)'] >= selected_payload[0]) & (spacex_df['Payload Mass (kg)'] <= selected_payload[1])]
        fig = px.scatter(suc_data_scatter, x='Payload Mass (kg)', y='class', color='Booster Version Category', hover_data=['Booster Version','class'], title='Correlation between Payload and Success for all sites')
        return fig
    else:
        suc_data_scatter_site = filtered_df[['Payload Mass (kg)', 'Booster Version Category', 'Booster Version', 'class']]
        fig = px.scatter(suc_data_scatter_site, x='Payload Mass (kg)', y='class', color='Booster Version Category', hover_data=['Booster Version','class'], title='Correlation between Payload and Success for in site' + entered_site)
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
