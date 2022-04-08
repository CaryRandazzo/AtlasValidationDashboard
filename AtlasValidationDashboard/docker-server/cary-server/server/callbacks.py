################
#import modules
################
from dash.dependencies import Input, Output, State
import plotly.figure_factory as ff


#####################
#import python files
#####################
from app import app
from chi2 import chi2df

df, errors = chi2df()


################
#UPDATE GRAPH 1
################
@app.callback(
    Output('graph_1', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    #print(n_clicks)
    #print(dropdown_value)
    #print(range_slider_value)
    #print(check_list_value)
    #print(radio_items_value)    
    df_th1s = df[df['f_type']=='TH1']
    hist_data = [df_th1s['chi2ndf_vals'].values]    
    group_labels = ['distplot'] # name of the dataset
    fig = ff.create_distplot(hist_data, group_labels, show_hist=False, histnorm='')#,show_rug=False)
    #fig['data'].append(px.Scatter())
    #fig.layout.paper_bgcolor = 'red'
    #fig.update_layout(title_text=f'TH1 Distplot',xaxis_title='Chi2/NDF', xaxis={'linecolor':'red', 'mirror':True}, yaxis={'linecolor':'red','mirror':True})
    fig.update_layout(title_text=f'TH1 Distplot',xaxis_title='Chi2/NDF')
    #fig.update_xaxes(linecolor='red')
    #fig.update_yaxes(linecolor='red')    
    #fig = {
        #'data': [{
        #    'x': [1, 2, 3],
        #    'y': [3, 4, 5]
    #    }]
    #}
    return fig


################
#UPDATE GRAPH 2
################
@app.callback(
    Output('graph_2', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_2(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    #print(n_clicks)
    #print(dropdown_value)
    #print(range_slider_value)
    #print(check_list_value)
    #print(radio_items_value)
    df_th2s = df[df['f_type']=='TH2']
    hist_data = [df_th2s['chi2ndf_vals'].values]    
    group_labels = ['distplot'] # name of the dataset
    fig = ff.create_distplot(hist_data, group_labels, show_hist=False, histnorm='')
    fig.update_layout(title_text=f'TH2 Distplot',xaxis_title='Chi2/NDF')
    #fig = {
    #    'data': [{
    #        'x': [1, 2, 3],
    #        'y': [3, 4, 5],
    #        'type': 'bar'
    #    }]
    #}
    return fig


################
#UPDATE GRAPH 3
################
@app.callback(
    Output('graph_3', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_3(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    #print(n_clicks)
    #print(dropdown_value)
    #print(range_slider_value)
    #print(check_list_value)
    #print(radio_items_value)
    df_tp = df[df['f_type']=='TProfile']
    hist_data = [df_tp['chi2ndf_vals'].values]    
    group_labels = ['distplot'] # name of the dataset
    fig = ff.create_distplot(hist_data, group_labels, show_hist=False, histnorm='')
    fig.update_layout(title_text=f'TProfile Distplot',xaxis_title='Chi2/NDF')
    #df = px.data.iris()
    #fig = px.density_contour(df, x='sepal_width', y='sepal_length')
    return fig


################
#UPDATE GRAPH 4
################

@app.callback(
    Output('graph_4', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_4(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    #print(n_clicks)
    #print(dropdown_value)
    #print(range_slider_value)
    #print(check_list_value)
    #print(radio_items_value)  # Sample data and figure
    df_th1s = df[df['f_type']=='TH1']
    #make smaller x-axis names?
    fig = px.scatter(df_th1s, x="f_name", y="chi2ndf_vals")
    fig.update_layout(title_text=f'TH1 Chi2/NDF values by hist',xaxis_title='hist', yaxis_title='Chi2/NDF values')
    return fig


################
#UPDATE GRAPH 5
################

@app.callback(
    Output('graph_5', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_5(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    #print(n_clicks)
    #print(dropdown_value)
    #print(range_slider_value)
    #print(check_list_value)
    #print(radio_items_value)  # Sample data and figure
    df_th2s = df[df['f_type']=='TH2']
    #make smaller x-axis names?
    fig = px.scatter(df_th2s, x="f_name", y="chi2ndf_vals")
    fig.update_layout(title_text=f'TH2 Chi2/NDF values by hist',xaxis_title='hist', yaxis_title='Chi2/NDF values')
    return fig


################
#UPDATE GRAPH 6
################

@app.callback(
    Output('graph_6', 'figure'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_graph_6(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    #print(n_clicks)
    #print(dropdown_value)
    #print(range_slider_value)
    #print(check_list_value)
    #print(radio_items_value)  # Sample data and figure
    df_tp = df[df['f_type']=='TProfile']
    #make smaller x-axis names?
    fig = px.scatter(df_tp, x="f_name", y="chi2ndf_vals")
    fig.update_layout(title_text=f'TProfile Chi2/NDF values by hist',xaxis_title='hist', yaxis_title='Chi2/NDF values')
    return fig


#####################
#UPDATE CARD TITLE 1
#####################
@app.callback(
    Output('card_title_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_title_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    #print(n_clicks)
    #print(dropdown_value)
    #print(range_slider_value)
    #print(check_list_value)
    #print(radio_items_value)  # Sample data and figure
    df_th1s = df[df['f_type']=='TH1']
    return f'{len(df_th1s.values)}'


####################
#UPDATE CARD TEXT 1
####################
@app.callback(
    Output('card_text_1', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_text_1(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    #print(n_clicks)
    #print(dropdown_value)
    #print(range_slider_value)
    #print(check_list_value)
    #print(radio_items_value)  # Sample data and figure
    return f"No. TH1's"

#####################
#UPDATE CARD TITLE 2
#####################
@app.callback(
    Output('card_title_2', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_title_2(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    #print(n_clicks)
    #print(dropdown_value)
    #print(range_slider_value)
    #print(check_list_value)
    #print(radio_items_value)  # Sample data and figure
    df_th2s = df[df['f_type']=='TH2']
    return f'{len(df_th2s.values)}'

####################
#UPDATE CARD TEXT 2
####################
@app.callback(
    Output('card_text_2', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_text_2(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    #print(n_clicks)
    #print(dropdown_value)
    #print(range_slider_value)
    #print(check_list_value)
    #print(radio_items_value)  # Sample data and figure
    return f"No. TH2's"

#####################
#UPDATE CARD TITLE 3
#####################
@app.callback(
    Output('card_title_3', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_title_3(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    #print(n_clicks)
    #print(dropdown_value)
    #print(range_slider_value)
    #print(check_list_value)
    #print(radio_items_value)  # Sample data and figure
    df_tp = df[df['f_type']=='TProfile']
    return f'{len(df_tp.values)}'

####################
#UPDATE CARD TEXT 3
####################
@app.callback(
    Output('card_text_3', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_text_3(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    #print(n_clicks)
    #print(dropdown_value)
    #print(range_slider_value)
    #print(check_list_value)
    #print(radio_items_value)  # Sample data and figure
    return f"No. TProfile's"

#####################
#UPDATE CARD TITLE 4
#####################
@app.callback(
    Output('card_title_4', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_title_4(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    #print(n_clicks)
    #print(dropdown_value)
    #print(range_slider_value)
    #print(check_list_value)
    #print(radio_items_value)  # Sample data and figure    
    return f'{errors}'

####################
#UPDATE CARD TEXT 4
####################
@app.callback(
    Output('card_text_4', 'children'),
    [Input('submit_button', 'n_clicks')],
    [State('dropdown', 'value'), State('range_slider', 'value'), State('check_list', 'value'),
     State('radio_items', 'value')
     ])
def update_card_text_4(n_clicks, dropdown_value, range_slider_value, check_list_value, radio_items_value):
    #print(n_clicks)
    #print(dropdown_value)
    #print(range_slider_value)
    #print(check_list_value)
    #print(radio_items_value)  # Sample data and figure
    return f"Chi2Test Errors"

#####################
#UPDATE transfer_vals
#####################

@app.callback(
    [Output('transfer_val1', 'children'),
    Output('transfer_val2','children')],
    [Input('submit_button', 'n_clicks')],
    [State('text_input1','value'),
     State('text_input2','value')]
    )
def update_transfer_vals(n_clicks,text_input1,text_input2):
    #print(text_input1)
    #print(text_input2)
    return text_input1, text_input2


####################
#UPDATE df
####################

@app.callback(
    Output('transfer_val_df','children'),
    [Input('submit_button', 'n_clicks')],
    [State('text_input1','value'),
     State('text_input2','value')]
    )
def update_df(n_clicks,text_input1,text_input2):
    #print('??????????????????????????????????')
    #defining these files should be done by input from a dash input box
    #print(type(text_input1))
    #print(type(text_input2))
    #try:      
        #file1 = ROOT.TFile.Open(text_input1)
        #file2 = ROOT.TFile.Open(text_input2) 
        #file1 = ROOT.TFile.Open('data15_13TeV.00276689.physics_Main.merge.HIST.f1051_h335._0001.1')
        #file2 = ROOT.TFile.Open('data15_13TeV.00276689.physics_Main.merge.HIST.f1052_h335._0001')
        
    #except:
    #    print('file error')
    #print(f'type:{type(file1)}') #THIS CURRENTLY IS THE MAIN PROBLEM
    #print(f'type:{type(file2)}') #THIS CURRENTLY IS THE MAIN PROBLEM
    #apparently, there is an issue with cppyy as the file type/class rather than ROOT/class
    #ask sawyer?
    #WORKAROUND: everything works fine if you can do the calculations outside of the callbacks
    #but i wont be able to input the file?
    #THEREALFIX - use cashe store @cache.memoize() to memorize the global store,
    # see https://dash.plotly.com/sharing-data-between-callbacks(Example 3)
    #maybe you can call the function() outside of the callback/def scope in a global scope
    #that way you can access the damn file1/file2 text input values from global
    #WORSTCASE - we use an external input.py file, import it (from input import *) and...
    #have it in the documentation that you need to manually input the filenames there to
    #
    
    #try:
        #get output on the main function based on the 2 input files
    #    f_path, chi2_dict,n_th1,n_th2,n_tp,errors = validate_uw_hists(file1,file2,'',{'f_name':[],'f_type':[],'chi2ndf_vals':[]},0,0,0,0)
    #except:
    #    print('procesing error')

    #try:
        #construct the dataframe
    #    df = pd.DataFrame(chi2_dict)
    #except:
    #    print('dataframe creation error')
    
    #my_string = str(Input('text_input1','value'))
    #print(my_string)
    #print(f"{str(Input('text_input1','value'))}")
    #print(f"-----------------num th1s:{df[df['f_type']=='TH1'].shape[0]}")
    #print('done')
    return #df #this may need to be returned as a json, see sharing data between callbacks