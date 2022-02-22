#################################################
#Author: Cary Randazzo, Louisiana Tech University
#Date: 11-13-2020
#Run directions: ???
#################################################


########################
#import modules for app
########################
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px


#############################
#import python files for app
#############################
from styles import *
from controls import *
from content_first_row import *
from content_second_row import *
from content_third_row import *
from content_fourth_row import *


######################################
#create the Parameters Area (sidebar)
######################################

sidebar = html.Div(
    [
        html.H2('Parameters', style=TEXT_STYLE), #see styles.py
        html.Hr(),
        controls # see controls.py
    ],
    style=SIDEBAR_STYLE, #see styles.py
)


##############################
#create the main content area
##############################
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


########################
#App and Layout Handles
########################
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([sidebar, content]) #see sidebar.py  #BOTH
#app.layout = html.Div([content]) #see sidebar.py   #JUST CONTENT


####################################
#Import callbacks from callbacks.py
####################################
from callbacks import *


####################
#Run the app server
####################
if __name__ == '__main__':
    #make all the tools False to turn off errors in dashboard
    app.run_server(debug=False,dev_tools_props_check=False,dev_tools_ui=False,host='localhost',port='1337')

#NOTE: in terminal, if you get "address is in use", free the port by
#killing the server with the command: fuser -k 1337/tcp