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
server = app.server

uniquelaunchsites = spacex_df['Launch Site'].unique().tolist()
lsites = []
lsites.append({'label': 'All Sites', 'value': 'All Sites'})
for site in uniquelaunchsites:
 lsites.append({'label': site, 'value': site})
 

app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                dcc.Dropdown(id='site_dropdown',
                                             options=lsites,
                                             placeholder="Select a Launch Site here",
                                             searchable=True,
                                             value='All Sites'
                                             ),
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                html.P("Payload range (Kg):"),
                                dcc.RangeSlider(id='selected_payload',
                                                min=0, max=10000, step=1000,
                                                marks = {
                                                         0: '0 kg',
                                                         1000: '1000 kg',
                                                         2000: '2000 kg',
                                                         3000: '3000 kg',
                                                         4000: '4000 kg',
                                                         5000: '5000 kg',
                                                         6000: '6000 kg',
                                                         7000: '7000 kg',
                                                         8000: '8000 kg',
                                                         9000: '9000 kg',
                                                         10000: '10000 kg'
                                                        },
                                                value=[min_payload, max_payload]
                                                ),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              [Input(component_id='site_dropdown', component_property='value')]
)
def get_pie_chart(site_dropdown):
    filtered_df = spacex_df[spacex_df['class'] == 1]
    if site_dropdown == 'All Sites':
        fig = px.pie(filtered_df, 
                     names = 'Launch Site',
                     hole=.3,
                     title = 'Total Success Launches By all sites'
                     )
    else:
        # return the outcomes piechart for a selected site
        df  = spacex_df.loc[spacex_df['Launch Site'] == site_dropdown]
        fig = px.pie(df, 
                     names = 'class',
                     hole=.3,
                     title = 'Total Success Launches for site '+site_dropdown
                     )
    return fig

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site_dropdown', component_property='value'), Input(component_id="selected_payload", component_property="value")]
)
def update_scatter_chart(site_dropdown, selected_payload):
    if site_dropdown == 'All Sites':
        low, high = selected_payload
        mask = (spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
        fig = px.scatter(
            spacex_df[mask],
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            size='Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'],
            title='Payload Mass vs. Class (All Sites)'
        )
    else:
        low, high = selected_payload
        mask = (df['Payload Mass (kg)'] > low) & (df['Payload Mass (kg)'] < high)
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        fig = px.scatter(
            filtered_df[mask],
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            size='Payload Mass (kg)',
            hover_data=['Payload Mass (kg)'],
            title=f'Payload Mass vs. Class ({site_dropdown})'
        )
    return fig

if __name__ == '__main__':
    app.run_server()
