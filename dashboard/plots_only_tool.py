# Cary Randazzo - 9-12-2024, for the ATLAS Collaboration

import ROOT
import pandas as pd
import os
import matplotlib.pyplot as plt
import argparse
# from replica_processor import *
import replica_processor as rp
import seaborn as sns
import matplotlib.colors as mcolors


def validate_uw_hists(tf,file1,file2,f_path,chi2_dict,n_th1,n_th2,n_tp,errors, path_length):  
    """Params based on root file structure -- be sure to change the "==" values based on the length of the path of the root file"""


    # Loop through the available directories or files in the .root file
    for key in tf.GetListOfKeys():

        # Get a handle for the next directory or file
        input = key.ReadObj()
    
        # Determine if the location in the file we are at is a directory
        if issubclass(type(input),ROOT.TDirectoryFile):

            # Record the path of the directory we are looking in
            try:
                f_path = input.GetPath() 
            except:
                print("cant GetPath")

            # Split the path by '/' so we can determine where we are in the folder structure        
            try:
                split_path = f_path.split("/")
            except:
                print('cant split_path')            
            
            
	    # IMPORTANT, these == values will require to be changed based on the length of the path of the root file. In the case of the docker system, /app/etc/etc adds 3 pieces to run/filename for a total length of 5
            # Recursively go deeper into the file structure depending on the length of split_path
            if len(split_path) == path_length:
            # if len(split_path) == 2:

                # We are 5 directories deep, go deeper
                f_path,chi2_dict,n_th1,n_th2,n_tp,errors = validate_uw_hists(input,file1, file2,f_path,chi2_dict,n_th1,n_th2,n_tp,errors, path_length)  

            # Path lengths greater than the specified number indicate a potential folder of interest from folder_list, check for these and go deeper if so
            elif len(split_path) > path_length and any(folder in split_path for folder in (folder_list)):                
            # elif len(split_path) > 2 and any(folder in split_path for folder in (folder_list)):                
                
		# We are greater than 3 directories deep and these directories include the specified folders above, goo deeper
                f_path,chi2_dict,n_th1,n_th2,n_tp,errors = validate_uw_hists(input,file1, file2,f_path,chi2_dict,n_th1,n_th2,n_tp,errors, path_length)     

            
            # If the length is shorter than the specified number, than we need to continue the loop
            else:
                pass
            
            # Record the file_path that will result now that we are done with the current folder level
            # i.e. the folder path that results from going up a level in the directory
            f_path = f_path.split('/')
            f_path = '/'.join(f_path[:-1])
                
        elif issubclass(type(input), ROOT.TProfile):
            # The is a TProfile 

            # Increment the number of TProfiles variable n_tp
            n_tp += 1                
            
            # Record the path of the directory we are looking in with the name of the hist file as part of the path
            try:
                f_path_tp = f_path + '/' + input.GetName()                
            except:
                print("can't get f_path_tp")
            
            # Format f_path_tp
            try:
                # Get the part of f_path that follows the ':'
                f_path_tp = f_path_tp.split(':')
                f_path_tp = f_path_tp[1][1:]
            except:
                print("can't format f_path_tp")
            
            
            # Calculate the chi2 values and store them in chi2_dict
            try:
                # Calculate the chi2 value between file1's and file2's filename:f_name
                chi2ndf_val = file1.Get(f_path_tp).Chi2Test(file2.Get(f_path_tp),'CHI2/NDF')
                chi2_dict['f_name'].append(f_path_tp)
                chi2_dict['f_type'].append('TProfile')
                chi2_dict['chi2ndf_vals'].append(chi2ndf_val)
                print('chi2success')
            except:            
                errors +=1
                print(f'chi2_tp error on filepath: {f_path_th2}')

        
        elif issubclass(type(input),ROOT.TH2):	    
            # The is a TH2 histogram

            # Increment the number of TH2s in variable n_th2
            n_th2 += 1            

            # Record the path of the directory we are looking in with the name of the hist file as part of the path
            try:
                f_path_th2 = f_path + '/' + input.GetName()                
            except:
                print("can't get f_path_th2")
            
            # Format f_path_th2 
            try:
	        # Get the part of f_path that follows the ':'
                f_path_th2 = f_path_th2.split(':')
                f_path_th2 = f_path_th2[1][1:]
            except:
                print("can't format f_path_th2")
            
	    # Calculate the chi2 values and store them in chi2_dict
            try:
                # Calculate the chi2 value between file1's and file2's filename:f_name
                chi2ndf_val = file1.Get(f_path_th2).Chi2Test(file2.Get(f_path_th2),'CHI2/NDF')
                chi2_dict['f_name'].append(f_path_th2)
                chi2_dict['f_type'].append('TH2')
                chi2_dict['chi2ndf_vals'].append(chi2ndf_val)
            except:            
                errors +=1
                print(f'chi2_th2 error on filepath: {f_path_th2}')
                
                
        elif issubclass(type(input),ROOT.TH1):            
            # This is a TH1 histogram

            # Increment the number of TH2s in variable n_th1
            n_th1 += 1
            
            # Record the path of the directory we are looking in with the name of the hist file as part of the path
            try:
                f_path_th1 = f_path + '/' + input.GetName()                
            except:
                print("cant GetPath2")

            # Format f_path_th1
            try:
                # Get the part of f_path that follows the ':'
                f_path_th1 = f_path_th1.split(':')
                f_path_th1 = f_path_th1[1][1:]
            except:
                print("can't format f_path_th1")

            # Calculate the chi2 values and store them in chi2_dict                                    
            try:
                # Calculate the chi2 value between file1's and file2's filename:f_name
                chi2ndf_val = file1.Get(f_path_th1).Chi2Test(file2.Get(f_path_th1),'CHI2/NDF')
                chi2_dict['f_name'].append(f_path_th1)
                chi2_dict['f_type'].append('TH1')
                chi2_dict['chi2ndf_vals'].append(chi2ndf_val)
            except Exception as e:
                print(e)            
                errors +=1
                print(f'chi2 error on filepath: {f_path_th1}')
            

    return f_path, chi2_dict, n_th1, n_th2,n_tp, errors



# Modified version for standalone
def chi2df(file1_path, file2_path):

    # Get root file1
    try:
        file1 = ROOT.TFile.Open(file1_path)
        # print(len(file1.GetPath().split('/')))
    except Exception as e:
        print(f'file1 error: {e}')


    # Get root file2
    try:
        file2 = ROOT.TFile.Open(file2_path)
        path_length = len(file2.GetPath().split('/'))
        # print(len(file2.GetPath().split('/')))
    except Exception as e:
        print(f'file2 error: {e}')
        

    # To silence the chi2 errors, use the following
    # ROOT.gSystem.RedirectOutput("/dev/null")

    # Calculate the chi2 values and other relevant information for the comparison
    f_path, chi2_dict,n_th1,n_th2,n_tp,errors = validate_uw_hists(file1, file1,file2,'',{'f_name':[],'f_type':[],'chi2ndf_vals':[]},0,0,0,0, path_length)

    # Construct the dataframe
    df = pd.DataFrame(chi2_dict)
    
    
    print('processing complete..')

    return df, errors



def plot_dist_th1(df, bins=10000, sizex=15, sizey=9):
    print("constructing th1 data...")
    df_th1s = df[df['f_type']=='TH1']
    hist_data = df_th1s['chi2ndf_vals'].values

    plt.figure(figsize=(sizex,sizey))
    plt.hist(hist_data, bins=bins, alpha=0.7, label='TH1 Chi2/NDF', color='blue') # marker = ?
    plt.xlabel('Chi2/NDF')
    plt.ylabel('Frequency')
    plt.title('TH1 Chi2/NDF Distplot')
    plt.legend(loc='upper right')
    plt.show()
    
def plot_dist_th2(df, bins=50, sizex=15, sizey=9):
    print("constructing th2 data...")
    df_th2s = df[df['f_type']=='TH2']
    hist_data = [df_th2s['chi2ndf_vals'].values]

    plt.figure(figsize=(sizex,sizey))
    plt.hist(hist_data, bins=bins, alpha=0.7, label='TH2 Chi2/NDF', color='blue')
    plt.xlabel('Chi2/NDF')
    plt.ylabel('Frequency')
    plt.title('TH2 Chi2/NDF Distplot')
    plt.legend(loc='upper right')
    plt.show()
    
def plot_dist_tp(df, bins=50, sizex=15, sizey=9):
    print("constructing tp data...")
    df_tp = df[df['f_type']=='TProfile']
    hist_data = [df_tp['chi2ndf_vals'].values]    

    plt.figure(figsize=(10,6))
    plt.hist(hist_data, bins=bins, alpha=0.7, color='b', label='TProfile Chi2/NDF')
    plt.xlabel('Chi2/NDF')
    plt.ylabel('Frequency')
    plt.title('TProfile Chi2/NDF Distplot')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()
    
def plot_chi2_th1(df, sizex=15, sizey=9):
    print("constructing th1 data...")
    df_th1s = df[df['f_type']=='TH1']

    plt.figure(figsize=(sizex,sizey))
    plt.scatter(df_th1s['f_name'],df_th1s['chi2ndf_vals'], marker='o', color='blue')
    plt.xlabel('Hist Name')
    plt.ylabel('Chi2/NDF')
    plt.title('TH1 Chi2/NDF values by hist')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()
    
def plot_chi2_th2(df, sizex=15, sizey=9):
    print("constructing th2 data...")
    df_th2s = df[df['f_type']=='TH2']

    plt.figure(figsize=(sizex,sizey))
    plt.scatter(df_th2s['f_name'],df_th2s['chi2ndf_vals'], marker='o', color='blue')
    plt.xlabel('Hist Name')
    plt.ylabel('Chi2/NDF')
    plt.title('TH2 Chi2/NDF values by hist')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()
    
def plot_chi2_tp(df, sizex=15, sizey=9):
    print("constructing th1 data...")
    df_tp = df[df['f_type']=='TProfile']

    plt.figure(figsize=(sizex,sizey))
    plt.scatter(df_tp['f_name'], df_tp['chi2ndf_vals'], marker='o', color='blue')
    plt.xlabel('Hist Name')
    plt.ylabel('Chi2/NDF')
    plt.title('TProfile Chi2/NDF values by hist')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()
    
def plot_overlay(df1, df2,  hist_name_to_view, f_type, sizex=15, sizey=9):
    print("constructing hist1 data...")
    hist_one = df1[df1['f_type'] == f_type]
    hist_one = hist_one[hist_one['paths'] == hist_name_to_view]
    
    print("constructing hist2 data...")
    hist_two = df2[df2['f_type'] == f_type]
    hist_two = hist_two[hist_two['paths'] == hist_name_to_view]
    
    if f_type == 'TH1':
        # plot the overlay of the two histograms
        plt.figure(figsize=(sizex,sizey))
        # plt.plot(hist_one['x'], hist_one['occ'], marker='o', color='blue')
        # plt.scatter(hist_one['x'], hist_one['occ'], marker='o', color='blue')
        # plt.plot(hist_two['x'], hist_two['occ'], marker='o', color='black')
        # plt.scatter(hist_two['x'], hist_two['occ'], marker='o', color='black')
        plt.plot(hist_one['x'], hist_one['occ']-hist_two['occ'], marker='o', color='blue')
        plt.scatter(hist_one['x'], hist_one['occ']-hist_two['occ'], marker='o', color='blue')
        # plt.title(f'TH1-Overlay:{hist_name_to_view} (file1,file2)')
        plt.title(f'TH1-Overlay:{hist_name_to_view} (data=file1-file2)')
        plt.xlabel(r'$\eta$')
        plt.ylabel('Occupancy')
        plt.grid(True)
        plt.legend(loc='upper right')
        plt.show()
    elif f_type == 'TH2':
        colors = [(0, 0, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # Blue -> Green -> Yellow -> Red
        n_bins = 100  # Discretize the colormap into 100 bins
        cmap_name = 'root_colormap'
        root_cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
        pivot_table1 = hist_one.pivot(index='x', columns='y', values='occ')
        pivot_table2 = hist_one.pivot(index='x', columns='y', values='occ')
        # plot the overlay of the two histograms
        plt.figure(figsize=(sizex,sizey))
        # sns.heatmap(pivot_table1-pivot_table2, cmap=root_cmap, alpha=0.5, cbar=False)
        # sns.heatmap(pivot_table1-pivot_table2)
        # sns.heatmap(pivot_table1, cmap=root_cmap, alpha=0.5, cbar=False)
        sns.heatmap(pivot_table1-pivot_table2)
        plt.title(f'TH2-Heatmap1:{hist_name_to_view}, heat=occ')
        plt.xlabel(r'$\eta$')
        plt.ylabel(r'$\phi$')
        plt.grid(True)
        plt.legend(loc='upper right')
        plt.show()
        
        # plt.figure(figsize=(sizex,sizey))
        # sns.heatmap(pivot_table2, cmap='coolwarm')
        # plt.title(f'TH2-Heatmap2:{hist_name_to_view}, heat=occ')
        # plt.xlabel(r'$\eta$')
        # plt.ylabel(r'$\phi$')
        # plt.show()
        
    elif f_type == 'TProfile':
        plt.figure(figsize=(sizex,sizey))
        # plt.plot(hist_one['x'], hist_one['occ'], marker='o', color='blue')
        # plt.scatter(hist_one['x'], hist_one['occ'], marker='o', color='blue')
        # plt.plot(hist_two['x'], hist_two['occ'], marker='o', color='black')
        # plt.scatter(hist_two['x'], hist_two['occ'], marker='o', color='black')
        plt.title(f'TP-Overlay:{hist_name_to_view} (data=file1-file2)')
        plt.plot(hist_one['x'], hist_one['occ']-hist_two['occ'], marker='o', color='blue')
        plt.scatter(hist_one['x'], hist_one['occ']-hist_two['occ'], marker='o', color='blue')
        plt.xlabel(r'$\eta$')
        plt.ylabel('Occupancy')
        plt.legend(loc='upper right')
        plt.grid(True)
        plt.show()
        
def integral_normalize_histogram(hist_data):
    integral = sum(hist_data)
    if integral == 0:
        return hist_data
    return hist_data / integral
    
def plot_chi2norm_th1s(df, sizex=15, sizey=9):
    df_th1s = df[df['f_type']=='TH1']
    chi2_norm_occ_data = integral_normalize_histogram(df_th1s['chi2ndf_vals'].values)

    plt.figure(figsize=(sizex,sizey))
    plt.scatter(df_th1s['f_name'], chi2_norm_occ_data, marker='o', color='blue')
    plt.xlabel('Hist Name')
    plt.ylabel('Chi2/NDF')
    plt.title('TH1 Chi2/NDF values by hist, Normed over area')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()
    
def plot_chi2norm_th2s(df, sizex=15, sizey=9):
    df_th2s = df[df['f_type']=='TH2']
    chi2_norm_occ_data = integral_normalize_histogram(df_th2s['chi2ndf_vals'].values)

    plt.figure(figsize=(sizex,sizey))
    plt.scatter(df_th2s['f_name'],chi2_norm_occ_data, marker='o', color='blue')
    plt.xlabel('Hist Name')
    plt.ylabel('Chi2/NDF')
    plt.title('TH2 Chi2/NDF values by hist, Normed over area')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()
    
def plot_chi2norm_tps(df, sizex=15, sizey=9):
    df_tp = df[df['f_type']=='TProfile']
    chi2_norm_occ_data = integral_normalize_histogram(df_tp['chi2ndf_vals'].values)

    plt.figure(figsize=(sizex,sizey))
    plt.scatter(df_tp['f_name'], df_tp['chi2ndf_vals'], marker='o', color='blue')
    plt.xlabel('Hist Name')
    plt.ylabel('Chi2/NDF')
    plt.title('TProfile Chi2/NDF values by hist, Normed over area')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    
    print("NOTE: files must be in the working directory of this script to work properly!")
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Define the argument parser
    parser = argparse.ArgumentParser(description='Plot histograms and chi2 values for two root files')
    parser.add_argument('--file1', type=str, help='Path to the first root file', required=True)
    parser.add_argument('--file2', type=str, help='Path to the second root file', required=True)
    parser.add_argument('--htype', type=str, choices=['TH1', 'TH2', 'TProfile'], help='Type of histograms', required=True)

    # Define a mutually exclusive group for --norm, --dist, --chi2, and --overlay
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--chi2norm', action='store_true', help='Normalize histogram over 1/integral area')
    group.add_argument('--dist', action='store_true', help='Plot distribution')
    group.add_argument('--chi2', action='store_true', help='Calculate chi2 values')
    group.add_argument('--overlay', action='store_true', help='Overlay histograms')

    # Add additional arguments for overlay
    parser.add_argument('--hname', type=str, help='Name of the histogram for overlay')
    
    args = parser.parse_args()
    
    folder_list = ['CaloMonitoring', 'Jets','MissingEt','Tau','egamma']
    
    
    print("--Current Configurations---")
    print(f"file1: {args.file1}")
    print(f"file2 {args.file2}")
    print(f"histogram type:{args.htype}")
    if args.chi2norm:
        print("chi2norm: True")
    if args.dist:
        print("dist: True")
    if args.chi2:
        print("chi2: True")
    if args.overlay:
        print("overlay: True")
    if args.hname:
        print(f"histogram name: {args.hname}")
        
    
    
    
    if args.dist:
        df, errors = chi2df(args.file1, args.file2)
        if args.htype == "TH1":
            print("plotting th1....")
            plot_dist_th1(df)
        elif args.htype == "TH2":
            plot_dist_th2(df)
        elif args.htype == "TProfile":
            plot_dist_tp(df)
                    
    elif args.chi2:
        df, errors = chi2df(args.file1, args.file2)
        if args.htype == "TH1":
            plot_chi2_th1(df)
        elif args.htype == "TH2":
            plot_chi2_th2(df)
        elif args.htype == "TProfile":
            plot_chi2_tp(df)
            
    elif args.chi2norm:
        print("Calculating chi2 values...")
        df, errors = chi2df(args.file1, args.file2)
        if args.htype == "TH1":
            plot_chi2norm_th1s(df)
        elif args.htype == "TH2":
            plot_chi2norm_th2s(df)
        elif args.htype == "TProfile":
            plot_chi2norm_tps(df)
            
    elif args.overlay:
        if not args.hname:
            parser.error("--overlay additionally requires --hname")
        print("Processing file1 histogram data...")
        df1_data = rp.hist_to_df(args.file1)
        print("Processing file2 histogram data...")
        df2_data = rp.hist_to_df(args.file2)
        print("Generating overlay...")
        plot_overlay(df1_data, df2_data, args.hname, args.htype)
    
    
    
    # whatever the histograms are that are bad. Make an overlay of the plots to see the differences.
    # make copies of the offending histograms and put them to a root file.
    # the files will be separate and need to be overlayed.
    
    # for now , try implementing the normalization.
    # see if it changes how many histograms are bad
    
    # option - root hist displays
    # option - swan overlay displays
    
    # FOR TESTING
    # hist_name = 'run_472943/CaloMonitoring/TileCellMon_NoTrigSel/General/Summary/TIME_execute'
    # hist_type = 'TH1'
    # command:
    #  python plots_only_tool.py --file1 data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1 --file2 data24_13p6TeV.00472943.physics_Main.merge.HIST.r15810_p6305.root --htype TH1 --overlay --hname run_472943/CaloMonitoring/TileCellMon_NoTrigSel/General/Summary/TIME_execute
    
    # hist_name = 'run_472943/Tau/Calo/Tau_Calo_centFracVsLB'
    # hist_type = 'TH2'
    
    # hist_name = run_472943/CaloMonitoring/TileCellMon_NoTrigSel/General/CellsXEta
    # hist_type = 'TProfile'
    