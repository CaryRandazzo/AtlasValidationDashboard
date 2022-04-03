################
#import modules
################
import dash_bootstrap_components as dbc
import dash_core_components as dcc

##############################
#Create content for second row
##############################
content_second_row = dbc.Row(
    [
        dbc.Col(
			dcc.Graph(id='graph_1'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_2'), md=4
        ),
        dbc.Col(
            dcc.Graph(id='graph_3'), md=4
        )
    ]
)