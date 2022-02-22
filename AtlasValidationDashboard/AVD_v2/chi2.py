####################
#import modules
####################

import ROOT
from IPython.display import clear_output
import pandas as pd

####################
#import files
####################

from config import *

####################
#Main Function
####################

def validate_uw_hists(tf,file2,f_path,chi2_dict,n_th1,n_th2,n_tp,errors):  
    #main loop
    for key in tf.GetListOfKeys():        
        input = key.ReadObj()
    
        #determine if the location in the file we are at is a directory
        if issubclass(type(input),ROOT.TDirectoryFile):
           
            #record the path of the directory we are looking in
            try:
                f_path = input.GetPath() 
#                 print(f'f_path:{f_path}')
            except:
                print("cant GetPath")
                

            #split the path by '/' so we can determine where we are in the folder structure        
            try:
                split_path = f_path.split("/")
            except:
                print('cant split_path')            
            
            
            #recursively go deeper into the file structure depending on the length of split_path
            if len(split_path) == 2:
                #we are 2 directories deep, go deeper
                f_path,chi2_dict,n_th1,n_th2,n_tp,errors = validate_uw_hists(input,file2,f_path,chi2_dict,n_th1,n_th2,n_tp,errors)  
            elif len(split_path) > 2 and any(folder in split_path for folder in ('CaloMonitoring', 'Jets','MissingEt','Tau','egamma')):                
                #we are greater than 3 directories deep and these directories include the specified folders above, goo deeper
                f_path,chi2_dict,n_th1,n_th2,n_tp,errors = validate_uw_hists(input,file2,f_path,chi2_dict,n_th1,n_th2,n_tp,errors)     
            else:
                pass
            
            #record the file_path that will result now that we are done with the current folder level
            #i.e. the folder path that results from going up a level in the directory
            f_path = f_path.split('/')
            f_path = '/'.join(f_path[:-1])
                
        elif issubclass(type(input), ROOT.TProfile):
            #print('test????')
            try:
                n_tp += 1
                #clear_output(wait=True)
                #print(f'n_th1:{n_th1}')
                #print(f'n_th2:{n_th2}')
                #print(f'n_tp:{n_tp}')
            except:
                print('error code: 0')
                
            #print('test???')
            
            #record the path of the directory we are looking in with the name of the hist file as part of the path
            try:
                f_path_tp = f_path + '/' + input.GetName()                
            except:
                print("error code: 1, cant GetPath3")
            
            #print('test??')
            
            try:
                #get the part of f_path that follows the ':'
                f_path_tp = f_path_tp.split(':')
                f_path_tp = f_path_tp[1][1:]
            except:
                print('error code: 2')
            
            #print('test?')
            
            #print(f_path_tp)
            try:
                #print('T')
                #calculate the chi2 value between file1's and file2's filename:f_name
                chi2ndf_val = file1.Get(f_path_tp).Chi2Test(file2.Get(f_path_tp),'CHI2/NDF')
                #print('T2')
                chi2_dict['f_name'].append(f_path_tp)
                #print('T3')
                chi2_dict['f_type'].append('TProfile')
                #print('T4')
                chi2_dict['chi2ndf_vals'].append(chi2ndf_val)
                #print('T5')
            except:            
                errors +=1
                print(f'error code: 3, chi2_tp error on filepath: {f_path_th2}')
            #print('test')

        
        elif issubclass(type(input),ROOT.TH2):
            n_th2 += 1            
            #clear_output(wait=True)
            #print(f'n_th1:{n_th1}')
            #print(f'n_th2:{n_th2}')
            #print(f'n_tp:{n_tp}')

            #record the path of the directory we are looking in with the name of the hist file as part of the path
            try:
                f_path_th2 = f_path + '/' + input.GetName()                
            except:
                print("cant GetPath3")
            
            #get the part of f_path that follows the ':'
            f_path_th2 = f_path_th2.split(':')
            f_path_th2 = f_path_th2[1][1:]
            
            try:
                #calculate the chi2 value between file1's and file2's filename:f_name
                chi2ndf_val = file1.Get(f_path_th2).Chi2Test(file2.Get(f_path_th2),'CHI2/NDF')
                chi2_dict['f_name'].append(f_path_th2)
                chi2_dict['f_type'].append('TH2')
                chi2_dict['chi2ndf_vals'].append(chi2ndf_val)
            except:            
                errors +=1
                print(f'chi2_th2 error on filepath: {f_path_th2}')
                
                
        elif issubclass(type(input),ROOT.TH1):            
            n_th1 += 1
            #clear_output(wait=True)
            #print(f'n_th1:{n_th1}')
            #print(f'n_th2:{n_th2}')
            #print(f'n_tp:{n_tp}')
            
            #record the path of the directory we are looking in with the name of the hist file as part of the path
            try:
                f_path_th1 = f_path + '/' + input.GetName()                
            except:
                print("cant GetPath2")

            #get the part of f_path that follows the ':'
            f_path_th1 = f_path_th1.split(':')
            f_path_th1 = f_path_th1[1][1:]
                                    
            try:
                #calculate the chi2 value between file1's and file2's filename:f_name
                chi2ndf_val = file1.Get(f_path_th1).Chi2Test(file2.Get(f_path_th1),'CHI2/NDF')
                chi2_dict['f_name'].append(f_path_th1)
                chi2_dict['f_type'].append('TH1')
                chi2_dict['chi2ndf_vals'].append(chi2ndf_val)
            except:            
                errors +=1
                print(f'chi2 error on filepath: {f_path_th1}')
                
          
    return f_path, chi2_dict, n_th1, n_th2,n_tp, errors

########################
#Using the Main Function
########################
#data15_13TeV.00276689.physics_Main.merge.HIST.f1051_h335._0001.1
#data15_13TeV.00276689.physics_Main.merge.HIST.f1052_h335._0001

###FILE_CONFIG - these are the two files that you want to analyze
#they must be in the same directory as the scripts
#fileOne = 'PHYSVAL_JZ7W_FE.root'
#fileTwo = 'PHYSVAL_JZ7W_PFO.root'

#defining these files should be done by input from a dash input box
file1 = ROOT.TFile.Open(fileOne)
 #for some weird reason when this file1 line above is uncommented, the file2 line works fine
 #from within the callback. But specifically not this one
file2 = ROOT.TFile.Open(fileTwo)
#file1 = 'the fakeness'
#file2 = 'the fakeness2'

#WHEN YOU WANT TO KEEP WORKING ON THE INPUT TEXT FOR THE FILES, COMMENT THESE BELOW OUT
#get output on the main function based on the 2 input files
f_path, chi2_dict,n_th1,n_th2,n_tp,errors = validate_uw_hists(file1,file2,'',{'f_name':[],'f_type':[],'chi2ndf_vals':[]},0,0,0,0)

#construct the dataframe
df = pd.DataFrame(chi2_dict)

print('done')
