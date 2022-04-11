#####################################################################################################################################################
#Author: Cary Randazzo, Masters Applied Physics, Louisiana Tech University                                                                                                   
#Date: 11-13-2020                                                                                                                                   
# Run directions:                                                                                                                                   
""" Install Docker, Install Docker Compose,                                                                                                         
navigate to the github containing the installtion files (currently CaryRandazzo/AtlasNetPrivate/) 
then click code and in terminal at the location you want the files stored enter the command:
git pull https://github.com:CaryRandazzo/AtlasNetPrivate.git
In order to change the configuration, (for now) place the data files to compare in the cary-data folder.
Then navigate to the /AtlasNetPrivate/AtlasValidationDashboard/docker-server/cary-server/server/config.py folder and set fileOne
to the name of the first file to compare, fileTwo to the name of the second file to compare, and folder_list to the folders of interest to analyze
for the comparison, save the changes to the config.
Finally, in /AtlasNetPrivate/AtlasValidationDashboard/docker-server/ execute the command:
docker compose build
then execute the command:
docker compose up
then enter a browser and navigate to the url: http://localhost:1337/
The dashboard should be visible.
Use ctrl+z in termal to close the server, docker compose down to take down the currently up version of the server, and sometimes rebuilding may be
necessary.
"""
#####################################################################################################################################################


##########################
# Import modules for app #
##########################
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


###############################
# Import python files for app #
###############################
from styles import *
from controls import *
from content_first_row import *
from content_second_row import *
from content_third_row import *
from content_fourth_row import *


########################################
# Create the Parameters Area (sidebar) #
########################################

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE), #see styles.py
        html.Hr(),
        controls # see controls.py
    ],
    style=SIDEBAR_STYLE, #see styles.py
)


################################
# Create the main content area #
################################
content = html.Div( children=
    [
        html.H2('Atlas Validation Dashboard', style=TEXT_STYLE),
        html.Hr(),
        content_first_row, #see content_first_row.py
        dcc.Tabs(id='tabs-example', value='tab-1', children=[
            dcc.Tab(label='Distributions', value='tab-1', children=[
                content_second_row,]),
            dcc.Tab(label='Chi2/NDF vs Hists', value='tab-2', children=[
                content_third_row]),
        ]),

        #content_second_row, #see content_second_row.py
        #content_third_row, #see content_third_row.py
        content_fourth_row, #see content_fourth_row.py
        # Hidden div inside the app that stores the intermediate value
        html.Div(id='transfer_val1', style={'display': 'none'}),
        html.Div(id='transfer_val2', style={'display': 'none'}),
        html.Div(id='transfer_val_df', style={'display': 'none'})
    ],
    style=CONTENT_STYLE
)


##########################
# App and Layout Handles #
##########################
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content]) #see sidebar.py  #BOTH
#app.layout = html.Div([content]) #see sidebar.py   #JUST CONTENT


######################################
# Import callbacks from callbacks.py #
######################################
from callbacks import *


######################
# Run the app server #
######################
server = app.server
if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0',port='1337')
