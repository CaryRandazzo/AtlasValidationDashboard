# Cary Randazzo - 9-12-2024, for the ATLAS Collaboration

import ROOT
import pandas as pd
import os
import matplotlib.pyplot as plt
import argparse
import replica_processor as rp
import seaborn as sns
import matplotlib.colors as mcolors
import sys


def normalize_histogram(hist, ref_hist, option):
    """Normalize histogram based on the selected option.

    Args:
        hist (TH1/TH2/TProfile): The histogram to normalize.
        ref_hist (TH1/TH2/TProfile): The reference histogram for normalization.
        option (str): The normalization option ('none', 'unit_area', 'same_entries', 'bin_width').

    Returns:
        None
    """
    if option == 'unit_area':
        if hist.Integral() != 0:
            hist.Scale(1.0 / hist.Integral())
        if ref_hist.Integral() != 0:
            ref_hist.Scale(1.0 / ref_hist.Integral())
    # Normalize to area of occupancies
    elif option == 'same_entries':
        hist_entries = hist.GetEntries()
        ref_entries = ref_hist.GetEntries()
        if ref_entries != 0:
            ref_hist.Scale(hist_entries / ref_entries)
    elif option == 'bin_width':
        for bin in range(1, hist.GetNbinsX() + 1):
            bin_width = hist.GetBinWidth(bin)
            hist.SetBinContent(bin, hist.GetBinContent(bin) / bin_width)
            hist.SetBinError(bin, hist.GetBinError(bin) / bin_width)
        for bin in range(1, ref_hist.GetNbinsX() + 1):
            bin_width = ref_hist.GetBinWidth(bin)
            ref_hist.SetBinContent(bin, ref_hist.GetBinContent(bin) / bin_width)
            ref_hist.SetBinError(bin, ref_hist.GetBinError(bin) / bin_width)
    # No normalization needed for 'none' option
    return hist, ref_hist

def validate_hists(tf,file1,file2,f_path,chi2_dict,n_th1,n_th2,n_tp,errors, path_length, chi2_mode='CHI2/NDF', normalization_option=None):  
    """Recursively validate the histograms in a root file and calculate the chi2 values between two root files.

    Args:
        tf (TFile): The root file used for mapping the histograms.
        file1 (TFile): The first root file to compare. 
        file2 (TFile): The second root file to compare.
        f_path (string): The path of the current directory in the root file.
        chi2_dict (dict): A dictionary containing the chi2 values of the histograms.
        n_th1 (int): The number of TH1 histograms.
        n_th2 (int): The number of TH2 histograms.
        n_tp (int): The number of TProfile histograms. 
        errors (int): The number of errors encountered. 
        path_length (int): The length of the path of the root file. 
        
    NOTE:
        path_length: This value DEPENDS on the path length current working directory that executed this function.
        Be sure to change the path_length accordingly to the length of the path of the root file at its location.
    """
    


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
                f_path,chi2_dict,n_th1,n_th2,n_tp,errors = validate_hists(input,file1, file2,f_path,chi2_dict,n_th1,n_th2,n_tp,errors, path_length, chi2_mode, normalization_option)  

            # Path lengths greater than the specified number indicate a potential folder of interest from args.folders, check for these and go deeper if so
            elif len(split_path) > path_length and any(folder in split_path for folder in (args.folders)):                
            # elif len(split_path) > 2 and any(folder in split_path for folder in (args.folders)):                
                
		# We are greater than 3 directories deep and these directories include the specified folders above, goo deeper
                f_path,chi2_dict,n_th1,n_th2,n_tp,errors = validate_hists(input,file1, file2,f_path,chi2_dict,n_th1,n_th2,n_tp,errors, path_length, chi2_mode, normalization_option)     

            
            # If the length is shorter than the specified number, than we need to continue the loop
            else:
                pass
            
            # Record the file_path that will result now that we are done with the current folder level
            # i.e. the folder path that results from going up a level in the directory
            f_path = f_path.split('/')
            f_path = '/'.join(f_path[:-1])
                
        elif issubclass(type(input), ROOT.TProfile):
            # TODO: Sumw2? normalization?, check dqm_algs
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
                # TODO: Change this to remove the ndf part as it takes options now
                chi2ndf_val = file1.Get(f_path_tp).Chi2Test(file2.Get(f_path_tp), chi2_mode)
                chi2_dict['f_name'].append(f_path_tp)
                chi2_dict['f_type'].append('TProfile')
                chi2_dict['chi2ndf_vals'].append(chi2ndf_val)
            except Exception as e:            
                errors +=1
                print(f'chi2_tp error on filepath: {f_path_tp}')
                print(e)

        
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
        
            # Sumw2 and Normalize the histograms
            # TODO: fix this and put in TH1 and TProfile as necessary
            try:
                file1_hist = file1.Get(f_path_th2)
                ref_hist = file2.Get(f_path_th2)
                
                if not file1_hist.GetSumw2N():
                    file1_hist.Sumw2()
                if not ref_hist.GetSumw2N():
                    ref_hist.Sumw2()
                
                file1_hist, ref_hist = normalize_histogram(file1_hist, ref_hist, normalization_option)
                    
            except Exception as e:
                print("Error in sumw2/norming TH2 histograms halting execution...")
                print(e)
                # sys.exit()
            
	    # Calculate the chi2 values and store them in chi2_dict
            try:
                # TODO: Change this to remove the ndf part as it takes options now
                # Calculate the chi2 value between file1's and file2's filename:f_name
                chi2ndf_val = file1.Get(f_path_th2).Chi2Test(file2.Get(f_path_th2), chi2_mode)
                chi2_dict['f_name'].append(f_path_th2)
                chi2_dict['f_type'].append('TH2')
                # TODO: change this to chi2_vals
                chi2_dict['chi2ndf_vals'].append(chi2ndf_val)
            except Exception as e:            
                errors +=1
                print(f'chi2_th2 error on filepath: {f_path_th2}')
                print(e)
                
                
        elif issubclass(type(input),ROOT.TH1):
            # TODO: Sumw2? normalization? check dqm_algs         
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
                # TODO: Change this to remove the ndf part as it takes options now
                # Calculate the chi2 value between file1's and file2's filename:f_name
                chi2ndf_val = file1.Get(f_path_th1).Chi2Test(file2.Get(f_path_th1), chi2_mode)
                chi2_dict['f_name'].append(f_path_th1)
                chi2_dict['f_type'].append('TH1')
                chi2_dict['chi2ndf_vals'].append(chi2ndf_val)
            except Exception as e:
                print(e)            
                errors +=1
                print(f'chi2 error on filepath: {f_path_th1}')
            

    return f_path, chi2_dict, n_th1, n_th2,n_tp, errors



# Modified version for standalone
def chi2df(file_path, ref_path, chi2_mode, normalization_option=None):
    """Calculates the chi2 values for the histograms in two root files and returns a dataframe of the results.

    Args:
        file_path (string): Path to the first root file.
        ref_path (string): Path to the second root file.

    Returns:
        df, errors (Dataframe, int): The dataframe containing the chi2 values of the histograms and the number of errors encountered.
    """

    # Get root file
    try:
        file = ROOT.TFile.Open(file_path)
        # print(len(file.GetPath().split('/')))
    except Exception as e:
        print(f'root "file" error: {e}')


    # Get root ref
    try:
        ref = ROOT.TFile.Open(ref_path)
        path_length = len(ref.GetPath().split('/'))
        # print(len(ref.GetPath().split('/')))
    except Exception as e:
        print(f'root "ref" file error: {e}')
        

    # Calculate the chi2 values and other relevant information for the comparison
    if normalization_option:
        # TODO: change chi2ndf_vals to to chi2_vals
        f_path, chi2_dict,n_th1,n_th2,n_tp,errors = validate_hists(file, file, ref,'',{'f_name':[],'f_type':[],'chi2ndf_vals':[]},0,0,0,0, path_length, chi2_mode, normalization_option)
    else:
        # TODO: change chi2ndf_vals to to chi2_vals
        f_path, chi2_dict,n_th1,n_th2,n_tp,errors = validate_hists(file, file, ref,'',{'f_name':[],'f_type':[],'chi2ndf_vals':[]},0,0,0,0, path_length, chi2_mode, "")

    # Construct the dataframe
    df = pd.DataFrame(chi2_dict)

    return df, errors



def plot_dist_th1(df, bins=10000, sizex=15, sizey=9):
    """Plots the distribution of Chi2/NDF values for TH1 histograms.

    Args:
        df (Dataframe): The dataframe containing the chi2 values of the TH1 histograms.
        bins (int, optional): The number of bins to use for the histogram. Defaults to 10000.
        sizex (int, optional): The x-axis figsize of the plot. Defaults to 15.
        sizey (int, optional): The y-axis figsize of the plot. Defaults to 9.
    """
    
    print("constructing th1 data...")
    df_th1s = df[df['f_type']=='TH1']
    # TODO: change chi2ndf_vals to to chi2_vals
    hist_data = df_th1s['chi2ndf_vals'].values

    plt.figure(figsize=(sizex,sizey))
    # TODO: change Chi2/NDF to something more reaonable that includes the options
    plt.hist(hist_data, bins=bins, alpha=0.7, label='TH1 Chi2/NDF', color='blue') # marker = ?
    plt.xlabel('Chi2/NDF')
    plt.ylabel('Frequency')
    plt.title('TH1 Chi2/NDF Distplot')
    plt.legend(loc='upper right')
    plt.show()
    
def plot_dist_th2(df, bins=50, sizex=15, sizey=9):
    """Plots the distribution of Chi2/NDF values for TH2 histograms.

    Args:
        df (Dataframe): The dataframe containing the chi2 values of the TH2 histograms.
        bins (int, optional): The number of bins to use for the histogram. Defaults to 50.
        sizex (int, optional): The x-axis figsize of the plot. Defaults to 15.
        sizey (int, optional): The y-axis figsize of the plot. Defaults to 9.
    """
    
    print("constructing th2 data...")
    df_th2s = df[df['f_type']=='TH2']
    # TODO: hcange this
    hist_data = [df_th2s['chi2ndf_vals'].values]

    plt.figure(figsize=(sizex,sizey))
    # TODO: change Chi2/NDF to something more reaonable that includes the options
    plt.hist(hist_data, bins=bins, alpha=0.7, label='TH2 Chi2/NDF', color='blue')
    plt.xlabel('Chi2/NDF')
    plt.ylabel('Frequency')
    plt.title('TH2 Chi2/NDF Distplot')
    plt.legend(loc='upper right')
    plt.show()
    
def plot_dist_tps(df, bins=50, sizex=15, sizey=9):
    """Plots the distribution of Chi2/NDF values for TProfile histograms.

    Args:
        df (Dataframe): The dataframe containing the chi2 values of the TProfile histograms.
        bins (int, optional): The number of bins to use for the histogram. Defaults to 50.
        sizex (int, optional): The x-axis figsize of the plot. Defaults to 15.
        sizey (int, optional): The y-axis figsize of the plot. Defaults to 9.
    """
    
    print("constructing tp data...")
    df_tp = df[df['f_type']=='TProfile']
    # TODO: change this
    hist_data = [df_tp['chi2ndf_vals'].values]    

    plt.figure(figsize=(10,6))
    # TODO: change Chi2/NDF to something more reaonable that includes the options
    plt.hist(hist_data, bins=bins, alpha=0.7, color='b', label='TProfile Chi2/NDF')
    plt.xlabel('Chi2/NDF')
    plt.ylabel('Frequency')
    plt.title('TProfile Chi2/NDF Distplot')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()
    
    
def plot_diffs(df1, df2,  hist_name_to_view, f_type, sizex=15, sizey=9):
    """Plots the differences of a selected histogram between the values of a root file and a reference root file.

    Args:
        df1 (Dataframe): This is the first collection of histograms of f_type from the given root file.
        df2 (Dataframe): This is the second collection of histograms of f_type from the given root REFERENCE file.
        hist_name_to_view (string): This is the specific histogram which was selected to view the differences.
        f_type (string): _description_
        sizex (int, optional): The x-axis figsize of the plot. Defaults to 15.
        sizey (int, optional): The y-axis figsize of the plot. Defaults to 9.
    """
    
    print("constructing hist1 data...")
    hist_one = df1[df1['f_type'] == f_type]
    hist_one = hist_one[hist_one['paths'] == hist_name_to_view]
    
    print("constructing hist2 data...")
    hist_two = df2[df2['f_type'] == f_type]
    hist_two = hist_two[hist_two['paths'] == hist_name_to_view]
    
    # plot the differences of the values from the histogram of the two files
    if f_type == 'TH1':
        
        # Prepare plot of TH1 difference values
        plt.figure(figsize=(sizex,sizey))
        plt.plot(hist_one['x'], hist_two['occ']-hist_one['occ'], marker='o', color='blue')
        plt.scatter(hist_one['x'], hist_two['occ']-hist_one['occ'], marker='o', color='blue')
        plt.title(f'TH1-Diffs:{hist_name_to_view} (data=ref-file)')
        plt.xlabel(r'$\eta$')
        plt.ylabel('Occupancy')
        plt.grid(True)
        plt.legend(loc='upper right')
        plt.show()
        
    elif f_type == 'TH2':
        
        # Calculate and format plotting data for TH2 difference values
        hist_tmp = pd.DataFrame({'x':hist_one['x'], 'y':hist_one['y'], 'occ':hist_two['occ'].values-hist_one['occ'].values})
        pivot_table = hist_tmp.pivot(index='x', columns='y', values='occ')
        
        # Prepare plot parameters
        colors = [(0, 0, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # Blue -> Green -> Yellow -> Red
        n_bins = 100  # Discretize the colormap into 100 bins
        cmap_name = 'root_colormap'
        root_cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
        
        # Plot the heatmap of differences
        plt.figure(figsize=(sizex,sizey))
        sns.heatmap(pivot_table)
        plt.title(f'TH2-Diffs-2D:{hist_name_to_view},\n shown_value=ref_value-file_value')
        plt.xlabel(r'$\eta$')
        plt.ylabel(r'$\phi$')
        plt.grid(True)
        plt.legend(loc='upper right')
        plt.show()
        
    elif f_type == 'TProfile':
        plt.figure(figsize=(sizex,sizey))
        plt.title(f'TP-Diffs:{hist_name_to_view} (data=ref-file)')
        plt.plot(hist_one['x'], hist_two['occ']-hist_one['occ'], marker='o', color='blue')
        plt.scatter(hist_one['x'], hist_two['occ']-hist_one['occ'], marker='o', color='blue')
        plt.xlabel(r'$\eta$')
        plt.ylabel('Occupancy')
        plt.legend(loc='upper right')
        plt.grid(True)
        plt.show()
    
def plot_chi2_th1s(df_th1, sizex=15, sizey=9):
    """_summary_

    Args:
        df_th1 (_type_): _description_
        sizex (int, optional): _description_. Defaults to 15.
        sizey (int, optional): _description_. Defaults to 9.
    """

    # Plot the normalized chi2 data of the TH1 histograms
    plt.figure(figsize=(sizex,sizey))
    # TODO: change this to chi2_vals
    plt.scatter(df_th1['f_name'], df_th1['chi2ndf_vals'], marker='o', color='blue')
    plt.xlabel('Hist Name')
    # TODO: change Chi2/NDF to something more reaonable that includes the options
    plt.ylabel('Chi2/NDF')
    plt.title('TH1 Chi2/NDF values by hist, Normed over area')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()
    
def plot_chi2_th2s(df_th2, sizex=15, sizey=9):
    """Plot the chi2 values of TH2 histograms with various options calculated from given args.

    Args:
        df_th2 (Dataframe): Dataframe containing the Chi2 values of the TH2 histograms.
        sizex (int, optional): The x-axis figsize of the plot. Defaults to 15.
        sizey (int, optional): The y-axis figsize of the plot. Defaults to 9.
        
    Returns:
        None: The histogram data is normalized and plotted in place. 
    """

    # Plot the normalized chi2 data of the TH2 histograms
    plt.figure(figsize=(sizex,sizey))
    # TODO: change this to something more reasonable that includes the options
    plt.scatter(df_th2['f_name'], df_th2['chi2ndf_vals'], marker='o', color='blue')
    plt.xlabel('Hist Name')
    # TODO: change this
    plt.ylabel('Chi2/NDF')
    plt.title('TH2 Chi2/NDF values by hist, Normed over area')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()
    
def plot_chi2_tps(df_tp, sizex=15, sizey=9):
    """_summary_

    Args:
        df_tp (_type_): _description_
        sizex (int, optional): _description_. Defaults to 15.
        sizey (int, optional): _description_. Defaults to 9.
    
    Returns:
        None: The histogram data is normalized and plotted in place. 
    """

    plt.figure(figsize=(sizex,sizey))
    # TODO: change this to something more reasonable that includes the options
    plt.scatter(df_tp['f_name'], df_tp['chi2ndf_vals'], marker='o', color='blue')
    plt.xlabel('Hist Name')
    # TODO: change this
    plt.ylabel('Chi2/NDF')
    plt.title('TProfile Chi2/NDF values by hist, Normed over area')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()
    
def process_normalization_args(args, mode=None):
    print("Processing the chi2 dataframe...")
    if mode is not None:
        if args.norm:
            return chi2df(args.file, args.ref, mode, args.norm)
        else:
            return chi2df(args.file, args.ref, mode, )
    elif args.norm:
        return chi2df(args.file, args.ref, args.norm)
    else:
        print("No normalization applied.")
        return chi2df(args.file, args.ref)
    
def integral_normalize_histogram(hist_data):
    """Normalizes the chi2 values specifically. not the raw values."""
    chi2_vals = hist_data['chi2ndf_vals'].values
    integral = sum(chi2_vals)
    if integral == 0:
        return chi2_vals
    return chi2_vals / integral

if __name__ == "__main__":
    
    print("NOTE: files must be in the working directory of this script to work properly!")
    
    # Set the ROOT ignore level to ignore warnings
    ROOT.gErrorIgnoreLevel = ROOT.kWarning
    
    # Set the seaborn plot style to look more like typical ROOT framework plots
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Define the argument parser
    parser = argparse.ArgumentParser(description='Required: Plot histograms and chi2 values for two root files')
    parser.add_argument('--file', type=str, help='Required: Path to the root file.', required=True)
    parser.add_argument('--ref', type=str, help='Required: Path to the reference root file.', required=True)
    parser.add_argument('--htype', type=str, choices=['TH1', 'TH2', 'TProfile'], help='Required: Choose the type of histograms to view results about.', required=True)
    parser.add_argument('--folders', nargs='+', required=True,
                        help='Required: List of folders to analyze. Provide at least one folder.')
    parser.add_argument('--mode', type=str, choices=['dist', 'chi2', 'diff'], help='Required: Set plot mode to distrubution, chi2, or value differences.', required=True)
    
    # Add additional arguments for various modes
    parser.add_argument('--norm', type=str, choices=['unit_area', 'occ_area', 'same_entries', 'bin_width', ''], default="", help='Optional for chi2 or dist:Normalization mode as either {None, unit_area, same_entries, bin_width}.')
    parser.add_argument('--hname', type=str, help='Required for diff: Provide the name of the histogram to plot.')
    parser.add_argument('--uu', action='store_true', help='Optional for chi2 or dist: Use unweighted histograms. Can combine with some other options.')
    parser.add_argument('--uw', action='store_true', help='Optional for chi2 or dist: Use unweighted histogram for the first histogram and weighted histogram for the second histogram. Can combine with some other options.')
    parser.add_argument('--ww', action='store_true', help='Optional for chi2 or dist: Use weighted histograms. Can combine with some other options.')
    parser.add_argument('--p', action='store_true', help='Optional for chi2 or dist: Use the p-values. Can combine with some other options.')
    parser.add_argument('--perndf', action='store_true', help='Optional for chi2 or dist: Calculate chi2 per degree of freedom. Can combine with some other options.')
    
    args = parser.parse_args()
    
    
    ##################
    # ARG PROCESSING #
    ##################
    
    # Handle mode error
    # if (args.uu or args.uw or args.ww or args.p or args.perndf) and not (args.dist or args.chi2):
    if (args.uu or args.uw or args.ww or args.p or args.perndf) and not (args.mode=='dist' or args.mode=='chi2'):
        parser.error("--uu, --uw, --ww, --p, and --perndf require either --mode dist or --mode chi2 to be specified.")
    
    
    # Display given configurations of args from user
    print("--Current Configurations---")
    print(f"file: {args.file}")
    print(f"ref: {args.ref}")
    print(f"histogram type:{args.htype}")
    print(f"folders: {args.folders}")
    
    # Construct the mode option for Chi2Test based on various mode options given by user
    # if either chi2 or dist was given as an option.
    if args.mode=='chi2' or args.mode=='dist':
        
        chi2options = ""
        if args.perndf:
            chi2options += "CHI2/NDF"
            if args.uu:
                chi2options += " UU"
                if args.p:
                    chi2options += " P"
            elif args.uw:
                chi2options += " UW"
                if args.p:
                    chi2options += " P"
            elif args.ww:
                chi2options += " WW"
                if args.p:
                    chi2options += " P"
            elif args.p:
                chi2options += " P"
        elif args.uu:
            chi2options += "UU"
            if args.p:
                chi2options += " P"
        elif args.uw:
            chi2options += "UW"
            if args.p:
                chi2options += " P"
        elif args.ww:
            chi2options += "WW"
            if args.p:
                chi2options += " P"
        else:
            chi2options += "P"
    
        possible_options = [
            "",  # No options
            "CHI2/NDF",
            "UU",
            "UW",
            "WW",
            "P",
            "CHI2/NDF UU",
            "CHI2/NDF UW",
            "CHI2/NDF WW",
            "CHI2/NDF P",
            "UU P",
            "UW P",
            "WW P",
            "CHI2/NDF UU P",
            "CHI2/NDF UW P",
            "CHI2/NDF WW P"
        ]
    
    
    if args.mode == 'dist':
        print("dist selected.")
    if args.mode == 'chi2':
        print("chi2 selected.")
    if args.mode == 'diff':
        print("diff selected")
    if args.norm:
        print(f"norm: {args.norm} selected.")
    if args.uu:
        print("uu selected.")
    if args.uw:
        print("uw selected.")
    if args.ww:
        print("ww selected.")
    if args.p:
        print("p selected.")
    if args.perndf:
        print("perndf selected.")
    if args.hname:
        print(f"histogram name: {args.hname} selected.")
    
    
    # Line break for clarity before processing
    print()
        
        
    # Process the required data for the plots
    if args.mode == 'dist' or args.mode == 'chi2':
        
        # Process normalization args
        try:
            df, errors = process_normalization_args(args, chi2options)
        except NameError:
            df, errors = process_normalization_args(args)
            
        
    # Plot either the distribution or Chi2 values with set options of TH1,TH2, or TProfile histograms
    if args.htype == "TH1":
        
        print("Getting TH1 data...")
        df_th1 = df[df['f_type']=='TH1']
        
        if args.norm == 'occ_area':
            print("Normalizing TH1 Chi2 vals to occupancy area...")
            chi2_normed_vals = integral_normalize_histogram(df_th1)
            df_th1.loc[:,'chi2ndf_vals'] = chi2_normed_vals
            
        print("Plotting TH1 histograms...")
        if args.mode == 'dist':
            plot_dist_th1(df_th1)
            
        elif args.mode == 'chi2':
            plot_chi2_th1s(df_th1)
            
    elif args.htype == "TH2":
        
        print("Getting TH2 data...")
        df_th2 = df[df['f_type']=='TH2']
        
        if args.norm == 'occ_area':
            print("Normalizing TH2 Chi2 vals to occupancy area...")
            chi2_normed_vals = integral_normalize_histogram(df_th2)
            df_th2.loc[:,'chi2ndf_vals'] = chi2_normed_vals
            
        print("Plotting TH2 histograms...")
        if args.mode == 'dist':
            plot_dist_th2(df_th2)
            
        elif args.mode == 'chi2':
            plot_chi2_th2s(df_th2)
            
    elif args.htype == "TProfile":
        
        print("Getting TProfile data...")
        df_tp = df[df['f_type']=='TProfile']
        if args.norm == 'occ_area':
            print("Normalizing TProfile Chi2 vals to occupancy area...")
            chi2_normed_vals = integral_normalize_histogram(df_tp)
            df_tp.loc[:,'chi2ndf_vals'] = chi2_normed_vals
            
        print("Plotting TProfile histograms...")
        if args.mode == 'dist':
            plot_dist_tps(df_tp)
            
        elif args.mode == 'chi2':
            plot_chi2_tps(df_tp)
            
    if args.mode == 'diff':
        
        if not args.hname:
            parser.error("--diff additionally requires --hname")
            
        print('Processing "file" histogram data...')
        file_data = rp.hist_to_df(args.file)
        
        print('Processing "ref" histogram data...')
        ref_data = rp.hist_to_df(args.ref)
        
        print("Plotting difference values...")
        plot_diffs(file_data, ref_data, args.hname, args.htype)
    
    
    # FOR TESTING
    # VERSION 0.1
    
    # Make sure when you test a command you have the correct htype for the histogram hname you have set!
    
    # hist_name = 'run_472943/CaloMonitoring/TileCellMon_NoTrigSel/General/Summary/TIME_execute'
    # hist_type = 'TH1'
    
    # hist_name = 'run_472943/Tau/Calo/Tau_Calo_centFracVsLB'
    # hist_type = 'TH2'
    
    # hist_name = run_472943/CaloMonitoring/TileCellMon_NoTrigSel/General/CellsXEta
    # hist_type = 'TProfile'
    
    # example command:
    #  (OLD) python plots_only_tool.py --file data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1 --ref data24_13p6TeV.00472943.physics_Main.merge.HIST.r15810_p6305.root --htype TH1 --overlay --hname run_472943/CaloMonitoring/TileCellMon_NoTrigSel/General/Summary/TIME_execute
    #  python plots_only_tool.py --file data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1 --ref data24_13p6TeV.00472943.physics_Main.merge.HIST.r15810_p6305.root --htype TH1 --diff --hname run_472943/CaloMonitoring/TileCellMon_NoTrigSel/General/Summary/TIME_execute
    
    # VERSION 1.0
    
    # lxplus -> lsetup python, lsetup root
    # python plots_only_tool.py ...and the options
    # python plots_only_tool.py --file data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1 --ref data24_13p6TeV.00472943.physics_Main.merge.HIST.r15810_p6305.root --htype TH1 --chi2 --perndf --norm occ_area
    
    # VERSION 1.2
    # file: data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1
    # ref: data24_13p6TeV.00472943.physics_Main.merge.HIST.r15810_p6305.root
    # htype: TH1'
    # mode: chi2
    # norm: occ_area
    # optional: perndf
    # python plots_only_tool.py --file data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1 --ref data24_13p6TeV.00472943.physics_Main.merge.HIST.r15810_p6305.root --htype TH1 --folders CaloMonitoring Jets MissingEt Tau egamma --chi2 --perndf --norm occ_area
    
    # ON LXPLUS
    # python plots_only_tool.py --file /eos/home-c/crandazz/SWAN_projects/ATLAS_DQ_Dashboard/data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1 --ref /eos/home-c/crandazz/SWAN_projects/ATLAS_DQ_Dashboard/data24_13p6TeV.00472943.physics_Main.merge.HIST.r15810_p6305.root --htype TH1 --folders CaloMonitoring Jets MissingEt Tau egamma --mode chi2 --perndf --norm occ_area
    # Appears i need x11 running to display the plots on lxplus
    
    # TODO: try to programmatically, automatically get the path_length for validate_histogram function instead of it
    # required to be local to the working directory.