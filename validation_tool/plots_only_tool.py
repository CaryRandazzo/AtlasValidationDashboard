#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN and the ATLAS Collaboration
#
# This script has been created for the benefit of the ATLAS experiment and is made available under the
# terms of the GNU General Public License v3.0. A copy of this license can be found at http://www.gnu.org/licenses/.
#
# Author: Cary Randazzo <Cary.David.Randazzo@cern.ch> of Louisiana Tech University, 9-21-2024
# under the guidance of Dr. Lee Sawyer <lee.sawyer@cern.ch> of Louisiana Tech University
#
# Description: This script processes ROOT histograms and calculates chi-squared values
#              for validation purposes. It includes functions for normalizing histograms,
#              calculating chi-squared values, and plotting the results.
#
# For usage instructions and examples, run "python plots_only_tool.py --help".
#
# NOTE: This script requires the ROOT, pandas, matplotlib, and seaborn libraries. It has been tested with conda.
# NOTE: chi2options and normalziation_option are not the same! The former is constructed from a combination of optional parameters while the latter is a single optional parameter "--norm"

import argparse
import logging
from typing import Tuple, Optional, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import ROOT

# Configure the system for logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# TODO: Consider adding error handling for when you are given --hname histogram_name/etc/etc and the histogram does not exist in the root file (will need to map a list of histograms and slow down the recursion though maybe)

def process_hist_to_data(tf,file,f_path,f_path_list, f_type_list, binNums,binNumsY, occupancies):  
    """
    Process ROOT runfile histogram to data.
    """
    
    # Main loop
    for key in tf.GetListOfKeys():    
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
            
            
            # Recursively go deeper into the file structure depending on the length of split_path
            if 'run' in split_path[-1]:
                # We are 2 directories deep, go deeper
                f_path,f_path_list, f_type_list, binNums,binNumsY, occupancies = process_hist_to_data(input,file,f_path, f_path_list, f_type_list, binNums,binNumsY, occupancies)  
            elif len(split_path) > 2 and any(folder in split_path for folder in ('CaloMonitoring', 'Jets','MissingEt','Tau','egamma')):                
                # We are greater than 3 directories deep and these directories include the specified folders above, goo deeper
                f_path, f_path_list, f_type_list, binNums,binNumsY, occupancies = process_hist_to_data(input,file,f_path, f_path_list, f_type_list, binNums,binNumsY, occupancies)     
            else:
                pass
            
            # Record the file_path that will result now that we are done with the current folder level
            #  i.e. the folder path that results from going up a level in the directory
            f_path = f_path.split('/')
            f_path = '/'.join(f_path[:-1])
                
        elif issubclass(type(input), ROOT.TProfile):
            
            # Record te path of the directory we are looking in with the name of the hist file as part of the path
            f_path_tp = get_f_path_at_histo_level(f_path, input)
            
            hist_file = file.Get(f_path_tp)
            binsX = hist_file.GetNbinsX()                                    
            
            # Setup the 3 arrays for creating the dataframe
            for binX in range(binsX+1):
                f_path_list.append(f_path_tp)
                binNum = hist_file.GetBin(binX)
                binNums.append(binX)
                binNumsY.append(None)
                occupancies.append(hist_file.GetBinContent(binNum))
                f_type_list.append('TProfile')
            
        elif issubclass(type(input),ROOT.TH2):

            # Record the path of the directory we are looking in with the name of the hist file as part of the path
            # Record te path of the directory we are looking in with the name of the hist file as part of the path
            f_path_th2 = get_f_path_at_histo_level(f_path, input)
            
            hist_file = file.Get(f_path_th2)
            binsX = hist_file.GetNbinsX()                        
            binsY = hist_file.GetNbinsY()
            
            # Setup the 3 arrays for creating the dataframe
            for binX in range(binsX+1):
                for binY in range(binsY+1):
                    f_path_list.append(f_path_th2)
                    binNumXY = hist_file.GetBin(binX,binY)
                    binNums.append(binX)
                    binNumsY.append(binY)
                    occupancies.append(hist_file.GetBinContent(binNumXY))
                    f_type_list.append('TH2')
                
        elif issubclass(type(input),ROOT.TH1):
            
            # Record the path of the directory we are looking in with the name of the hist file as part of the path
            # Record te path of the directory we are looking in with the name of the hist file as part of the path
            f_path_th1 = get_f_path_at_histo_level(f_path, input)
            
            hist_file = file.Get(f_path_th1)
            binsX = hist_file.GetNbinsX()            
            
            # Setup the 3 arrays for creating the dataframe
            for binX in range(binsX+1):                
                f_path_list.append(f_path_th1)
                binNum = hist_file.GetBin(binX,0)                
                binNums.append(binNum)
                binNumsY.append(None)                
                occupancies.append(hist_file.GetBinContent(binNum))
                f_type_list.append('TH1')
    
    return f_path, f_path_list, f_type_list, binNums,binNumsY, occupancies

def hist_to_df(path):
    """
    Converts ROOT histogram data from process_hist_to_data() to a pandas dataframe.
    """
    
    file = ROOT.TFile.Open(path)

    f_path, f_path_list, f_type_list, binNums,binNumsY, occupancies = process_hist_to_data(file,file,'',[],[],[],[],[])
    
    return pd.DataFrame({'paths':f_path_list,'f_type':f_type_list, 'x':binNums,'y':binNumsY,'occ':occupancies})


def normalize_histogram(hist: pd.DataFrame, ref_hist: pd.DataFrame, option: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Normalize histogram based on the selected option.

    Args:
        hist (DataFrame): The histogram to normalize containing type TH1, TH2, or TProfile histograms.
        ref_hist (DataFrame): The reference histogram for normalization containing type TH1, TH2, or TProfile histograms.
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


def get_f_path_at_histo_level(f_path: str, input: Optional[object]) -> Optional[str]:
    """
    Reformat the given file path at the histogram level by appending the name of the input object.
    Args:
        f_path (str): The base file path.
        input (Optional[object]): An object that is expected to have a 'GetName' method.
    Returns:
        Optional[str]: The reformatted file path, or None if an error occurs.
    Raises:
        AttributeError: If the input object does not have a 'GetName' method.
        IndexError: If the file path split does not return the expected format.
        Exception: For any other unexpected errors.
    """

    # TODO: Verify this works locally and on lxplus
    try:
        # Reformat the path for the histogram
        new_f_path = f_path + '/' + input.GetName()
        
        # Adjust the new_f_path if we are on lxplus vs locally running the script
        if "eos" in new_f_path:
            new_f_path = new_f_path.split(':')[2][1:] # On lxplus
        else:
            new_f_path = new_f_path.split(':')[1][1:]
        return new_f_path
    
    # HAndle exceptions
    except AttributeError as e:
        logging.error(f"AttributeError: {e} - input object has no attribute 'GetName'")
    except IndexError as e:
        logging.error(f"IndexError: {e} - f_path_th1 split did not return expected format")
    except Exception as e:
        logging.error(f"Unexpected error: {e} - can't format f_path_th1")

    return None

# def calculate_chi2(file1: Any, file2: Any, hist_type: str, f_path_type: str, chi2options: str, chi2_dict: Dict[str, Any]) ->Tuple[Any, Dict[str, Any]]:
def calculate_chi2(file1: Any, file2: Any, hist_type: str, f_path_type: str, chi2options: str, output_val_dict: Dict[str, Any]) ->Tuple[Any, Dict[str, Any]]:
    """
    Calculate the chi-squared (chi2) value between two ROOT histogram files and update the chi2 dictionary.
    Args:
        file1 (Any): The first ROOT file containing the histogram.
        file2 (Any): The second ROOT file containing the histogram.
        hist_type (str): The type of histogram being compared.
        f_path_type (pd.DataFrame): The path type in the DataFrame.
        chi2options (str): The optional return parameter for chi2 calculation.
        output_val_dict (Dict[str, Any]): Dictionary to store chi2 values and related information.
    Returns:
        output_val, output_val_dict (Tuple[Any, Dict[str, Any]]): A tuple containing the chi2 value and the updated chi2 dictionary.
    """
    
    

    try:
        # Calculate chi2 values given chi2options
        if hist_type == 'TH2':
            # chi2_val = chi2_test_2d(args, chi2options, file1, file2, f_path_type, chi2options)
            output_val = chi2_test_2d(args, chi2options, file1, file2, f_path_type, chi2options)
        else:
            # chi2_val = file1.Get(f_path_type).Chi2Test(file2.Get(f_path_type), chi2options)
            output_val = file1.Get(f_path_type).Chi2Test(file2.Get(f_path_type), chi2options)

        # Update chi2_dict
        # chi2_dict['f_name'].append(f_path_type)
        # chi2_dict['f_type'].append(hist_type)
        # chi2_dict['chi2ndf_vals'].append(chi2_val)
        output_val_dict['f_name'].append(f_path_type)
        output_val_dict['f_type'].append(hist_type)
        output_val_dict['output_vals'].append(output_val)

        return output_val, output_val_dict
    
    # Handle errors
    except KeyError as e:
        logging.error(f"KeyError: {e} - key not found in output_val_dict")
    except AttributeError as e:
        logging.error(f"AttributeError: {e} - issue with accessing attributes of ROOT objects")
    except Exception as e:
        logging.error(f"Unexpected error: {e} - while calculating chi2 values")    
    # return None, None
    # return None, chi2_dict
    return None, output_val_dict


class InsufficientStatisticsError(Exception):
    """Custom exception for insufficient statistics in the histogram."""
    pass

def chi2_test_2d(args: Any, chi2options: str, file1: Any, file2: Any, f_path_type: str, normalization_option: Optional[str] = None, min_stat=1) -> Tuple[Optional[Any], Optional[Any]]:
    """
    Preprocess histograms by retrieving them from the provided files, applying Sumw2 if necessary, 
    and normalizing them based on the given normalization option.
    Args:
        file1 (Any): The first file containing the histogram.
        file2 (Any): The second file containing the reference histogram.
        f_path_type (str): The path type used to retrieve the histograms from the files.
        normalization_option (Optional[str]): The option for normalizing the histograms. Default is None.
        min_stat (int): The minimum number of entries required for the histogram. Default is 1.
    Returns:
        Tuple[Optional[Any], Optional[Any]]: A tuple containing the processed histograms from file1 and file2.
        Returns (None, None) if an error occurs during processing.
    Raises:
        AttributeError: If there is an issue with accessing attributes of histograms.
        KeyError: If there is an issue with accessing histograms using the provided path.
        ValueError: If there is an issue with the normalization option.
        Exception: For any other unexpected errors during histogram preparation.
    """

    # TODO: consider outputting error statistics for this chi2 method similar to the chi2_2d method (review this with people individuals helping to test script)

    try:
        # Get the histogram at f_path_type from the root file(s)
        hist_2d = file1.Get(f_path_type)
        ref_hist = file2.Get(f_path_type)
        
        # Get handles for the histograms' shapes
        hist_2d_n_bins_x = hist_2d.GetNbinsX()
        hist_2d_n_bins_y = hist_2d.GetNbinsY()
        ref_hist_n_bins_x = ref_hist.GetNbinsX()
        ref_hist_n_bins_y = ref_hist.GetNbinsY()
        
        # Get handles for the histograms' entries
        hist_2d_entries = hist_2d.GetEntries()
        ref_hist_entries = ref_hist.GetEntries()
        
        # Ensure the histograms have the same shape
        assert hist_2d_n_bins_x == ref_hist_n_bins_x and hist_2d_n_bins_y == ref_hist_n_bins_y, "Observed and reference histograms must have the same shape"
        
        # Check if the histograms have enough statistics
        if hist_2d_entries < min_stat:
            raise InsufficientStatisticsError(f"Insufficient entries in the observed histogram: {hist_2d_entries} < {min_stat}. Execution halted.")
        
        # TODO: Decide if we should use this method and add "norm_to_hist2d" as a normalization option in normalize_histogram OR as we are currently set, normalize with sumw2-> scale entries to the same as hist_2d
        # Normalize them if a normalization option is set
        # file1_hist, ref_hist = normalize_histogram(file1_hist, ref_hist, normalization_option)
        
        print("Using default normalization method for this configuration (sumw2->scale to hist_2d entries)...")
        # Get the errors as sqrt(n)
        if not hist_2d.GetSumw2N():
            hist_2d.Sumw2()
        if not ref_hist.GetSumw2N():
            ref_hist.Sumw2()
        # Scale the reference histograms to the same number of entries as the input histogram 
        ref_hist.Scale(hist_2d_entries/ref_hist_entries)
        
        # Calculate chi2 value for each bin
        total_chi2_val = 0
        ndf = 0
        # TODO: Something is unusual about this code, NSigma is calculated from p_value, but it was given from a config parameter. How was that config paremeter calcluated without looping through and getting
        # the p_value for the histograms? And yet, its using the n_sigma it got from the config during calculating the chi2 values. So what comes first, the p_value or the n_sigma?
        # For now, I will temporarily comment out the n_sigma and p_value calculations and just calculate the chi2 values
        # vals_over_threshold = []
        for i in range(hist_2d_n_bins_x):
            for j in range(hist_2d_n_bins_y):
                error_squared = (hist_2d.GetBinError(i,j)**2 + ref_hist.GetBinError(i,j)**2)
                if error_squared > 0.000001:
                    chi2_val_at_ij = (hist_2d.GetBinContent(i,j) - ref_hist.GetBinContent(i,j))**2 / error_squared
                else:
                    print(f"Insufficient statistics in bin ({i},{j}). Continuing...")
                    # raise InsufficientStatisticsError(f"Insufficient statistics in bin ({i},{j})")
                    continue
                
                total_chi2_val = total_chi2_val + chi2_val_at_ij
                ndf += 1
                # p_value = ROOT.TMath.Prob(total_chi2_val, ndf)
                # n_sigma = ROOT.TMath.NormQuantile(1 - p_value)
                # if total_chi2_val >= n_sigma**2:
                    # vals_over_threshold.append(total_chi2_val)
                    
        p_value = ROOT.TMath.Prob(total_chi2_val, ndf)
        
        # Adjust the ndf down by 1 after counting
        ndf -= 1
        # And calculate the final chi2_per_ndf value
        chi2_per_ndf = total_chi2_val / ndf
                                  
        if "P" in chi2options:
            return p_value
        elif "NDF" in chi2options:
            return chi2_per_ndf
        # This condition should be last as all modes will be set to chi2, but if --p or --perndf is set, it will return those values first
        else:
            return total_chi2_val
    
    # Handle exceptions
    except AttributeError as e:
        logging.error(f"AttributeError: {e} - issue with accessing attributes of histograms")
    except KeyError as e:
        logging.error(f"KeyError: {e} - issue with accessing histograms using path {f_path_type}")
    except ValueError as e:
        logging.error(f"ValueError: {e} - issue with normalization option {normalization_option}")
    except Exception as e:
        logging.error(f"Unexpected error: {e} - while preparing histograms")

    return None, None


# def validate_hists(tf,file1,file2,f_path,chi2_dict,n_th1,n_th2,n_tp,path_length,chi2options='',normalization_option=None):  
def validate_hists(tf,file1,file2,f_path,output_val_dict,n_th1,n_th2,n_tp,path_length,chi2options='',normalization_option=None):  
    """
    Recursively validate the histograms in a root file and calculate the chi2 values between two root files.
    Args:
        tf (TFile): The root file used for mapping the histograms.
        file1 (TFile): The first root file to compare. 
        file2 (TFile): The second root file to compare.
        f_path (string): The path of the current directory in the root file.
        output_val_dict (dict): A dictionary containing the chi2 values of the histograms.
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
                # f_path,chi2_dict,n_th1,n_th2,n_tp = validate_hists(input,file1,file2,f_path,chi2_dict,n_th1,n_th2,n_tp,path_length,chi2options, normalization_option)  
                f_path,output_val_dict,n_th1,n_th2,n_tp = validate_hists(input,file1,file2,f_path,output_val_dict,n_th1,n_th2,n_tp,path_length,chi2options, normalization_option)  

            # Path lengths greater than the specified number indicate a potential folder of interest from args.folders, check for these and go deeper if so
            elif len(split_path) > path_length and any(folder in split_path for folder in (args.folders)):                
            # elif len(split_path) > 2 and any(folder in split_path for folder in (args.folders)):                
                
		        # We are greater than 3 directories deep and these directories include the specified folders above, goo deeper
                # f_path,chi2_dict,n_th1,n_th2,n_tp = validate_hists(input,file1, file2,f_path,chi2_dict,n_th1,n_th2,n_tp, path_length, chi2options, normalization_option)     
                f_path,output_val_dict,n_th1,n_th2,n_tp = validate_hists(input,file1, file2,f_path,output_val_dict,n_th1,n_th2,n_tp, path_length, chi2options, normalization_option)     
            
            # If the length is shorter than the specified number, than we need to continue the loop
            else:
                pass
            
            # Record the file_path that will result now that we are done with the current folder level
            # i.e. the folder path that results from going up a level in the directory
            f_path = f_path.split('/')
            f_path = '/'.join(f_path[:-1])
                
        elif issubclass(type(input), ROOT.TProfile):
            # Sumw2 and normalization is handled via Chi2Test method already, no need to implement here

            # Increment the number of TProfiles variable n_tp
            n_tp += 1                
            
            # Record the path of the directory we are looking in with the name of the hist file as part of the path
            # with error handling.
            f_path_tp = get_f_path_at_histo_level(f_path, input)
            
            # Apply chi2 calculations to TProfile histogram data with error handling
            # chi2_val, chi2_dict = calculate_chi2(file1, file2, 'TProfile', f_path_tp, chi2options, chi2_dict)
            output_val, output_val_dict = calculate_chi2(file1, file2, 'TProfile', f_path_tp, chi2options, output_val_dict)
        
        elif issubclass(type(input),ROOT.TH2):	    
            # The is a TH2 histogram

            # Increment the number of TH2s in variable n_th2
            n_th2 += 1            

            # Record the path of the directory we are looking in with the name of the hist file as part of the path
            f_path_th2 = get_f_path_at_histo_level(f_path, input)
        
            # Apply chi2 calculations to TH2 histogram data with error handling
            # (Normalize via Sumw2 and scale ref hist by the 2d hist)
            # (Calculate and return a choice of p_value, chi2_value, or chi2_per_ndf)
            # chi2_val, chi2_dict = calculate_chi2(file1, file2, 'TH2', f_path_th2, chi2options, chi2_dict)
            output_val, output_val_dict = calculate_chi2(file1, file2, 'TH2', f_path_th2, chi2options, output_val_dict)
                
        elif issubclass(type(input),ROOT.TH1):
            # Sumw2 and normalization is handled via Chi2Test method already, no need to implement here

            # Increment the number of TH2s in variable n_th1
            n_th1 += 1
            
            # Record the path of the directory we are looking in with the name of the hist file as part of the path
            f_path_th1 = get_f_path_at_histo_level(f_path, input)

            # Apply chi2 calculations to TProfile histogram data with error handling
            # chi2_val, chi2_dict = calculate_chi2(file1, file2, 'TH1', f_path_th1, chi2options, chi2_dict)
            output_val, output_val_dict = calculate_chi2(file1, file2, 'TH1', f_path_th1, chi2options, output_val_dict)

    # return f_path, chi2_dict, n_th1, n_th2,n_tp
    return f_path, output_val_dict, n_th1, n_th2,n_tp

def get_root_file(file_path: str) -> Any:
    """
    Opens a ROOT file from the given file path.
    Args:
        file_path (str): The path to the ROOT file to be opened.
    Returns:
        Any: The opened ROOT file object, or None if an error occurs.
    Raises:
        Exception: If there is an error opening the ROOT file, it will be caught and printed.
    """
    
    # Get root file
    try:
        file = ROOT.TFile.Open(file_path)
        if not file or file.IsZombie():
            raise IOError(f"Failed to open file: {file_path}")
        path_length = len(file.GetPath().split('/'))
        return file, path_length
    
    # Handle errors
    except IOError as e:
        logging.error(f"IOError: {e} - Could not open ROOT file at {file_path}")
    except Exception as e:
        logging.error(f"Unexpected error: {e} - while opening ROOT file at {file_path}")

    return None

# Modified version for standalone
def chi2df(file_path: str, ref_path: str, chi2options: str='', normalization_option:str=None) -> Tuple[pd.DataFrame, int]:
    """
    Calculates the chi2 values for the histograms in two root files and returns a dataframe of the results.
    Args:
        file_path (str): Path to the first root file.
        ref_path (str): Path to the second root file.
        chi2options (str): The optional return parameter for chi2 or dist modes. Defaults to ''.
        

    Returns:
        df (Dataframe): The dataframe containing the chi2 values of the histograms.
    """
    
    # Access the root file at file_path
    file, path_length = get_root_file(file_path)

    # Access the root file at ref_path
    ref_file, _ = get_root_file(ref_path)

    # Calculate the chi2 values and other relevant information for the comparison
    # TODO: at this moment, validate_hists does need the same input_file as two separate input args, can be fixed at some point
    # f_path, chi2_dict,n_th1,n_th2,n_tp = validate_hists(file, file, ref_file, '', {'f_name':[],'f_type':[],'chi2ndf_vals':[]}, 0, 0, 0, path_length, chi2options, normalization_option)
    # f_path, chi2_dict,n_th1,n_th2,n_tp = validate_hists(file, file, ref_file, '', {'f_name':[],'f_type':[],'output_vals':[]}, 0, 0, 0, path_length, chi2options, normalization_option)
    f_path, output_val_dict,n_th1,n_th2,n_tp = validate_hists(file, file, ref_file, '', {'f_name':[],'f_type':[],'output_vals':[]}, 0, 0, 0, path_length, chi2options, normalization_option)

    # Construct the dataframe
    # df = pd.DataFrame(chi2_dict)
    df = pd.DataFrame(output_val_dict)

    return df


def plot_dist_th1(df: pd.DataFrame, chi2options: str, bins:int=10000, sizex:int=15, sizey:int=9):
    """
    Plots the distribution of Chi2/NDF values for TH1 histograms.
    Args:
        df (Dataframe): The dataframe containing the chi2 values of the TH1 histograms.
        bins (int, optional): The number of bins to use for the histogram. Defaults to 10000.
        sizex (int, optional): The x-axis figsize of the plot. Defaults to 15.
        sizey (int, optional): The y-axis figsize of the plot. Defaults to 9.
        chi2options (str): The optional return parameter for chi2 or dist modes.
    """
    
    print("constructing th1 data...")
    df_th1s = df[df['f_type']=='TH1']
    # hist_data = df_th1s['chi2ndf_vals'].values
    hist_data = df_th1s['output_vals'].values

    plt.figure(figsize=(sizex,sizey))
    if "P" in chi2options:
        plt.hist(hist_data, bins=bins, alpha=0.7, label=f'TH1 P-Value:{chi2options} freq', color='blue') # marker = ?
        plt.title(f'TH1 P-Values Distplot')
    elif "NDF" in chi2options:
        plt.hist(hist_data, bins=bins, alpha=0.7, label=f'TH1 Chi2/NDF Value:{chi2options} freq', color='blue') # marker = ?
        plt.title(f'TH1 Chi2/NDF Values Distplot')
    else:
        plt.hist(hist_data, bins=bins, alpha=0.7, label=f'TH1 Chi2 Value:{chi2options} freq', color='blue') # marker = ?
        plt.title(f'TH1 Chi2 Values Distplot')
    plt.xlabel(f'{chi2options}')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.show()
    
def plot_dist_th2(df: pd.DataFrame, chi2options: str, bins:int=50, sizex:int=15, sizey:int=9):
    """
    Plots the distribution of Chi2/NDF values for TH2 histograms.
    Args:
        df (Dataframe): The dataframe containing the chi2 values of the TH2 histograms.
        bins (int, optional): The number of bins to use for the histogram. Defaults to 50.
        sizex (int, optional): The x-axis figsize of the plot. Defaults to 15.
        sizey (int, optional): The y-axis figsize of the plot. Defaults to 9.
        chi2options (str): The optional return parameter for chi2 or dist modes.
    """
    
    print("constructing th2 data...")
    df_th2s = df[df['f_type']=='TH2']
    # hist_data = [df_th2s['chi2ndf_vals'].values]
    hist_data = df_th2s['output_vals'].values

    print("plotting th2 data...")
    plt.figure(figsize=(sizex,sizey))
    plt.hist(hist_data, bins=bins, alpha=0.7, label=f'TH2 Chi2:{chi2options} freq', color='blue')
    plt.xlabel(f'Chi2:{chi2options}')
    plt.ylabel('Frequency')
    plt.title(f'TH2 Chi2:{chi2options} Distplot')
    plt.legend(loc='upper right')
    plt.show()
    
def plot_dist_tps(df: pd.DataFrame, chi2options: str, bins:int=50, sizex:int=15, sizey:int=9):
    """
    Plots the distribution of Chi2 values for TProfile histograms.
    Args:
        df (Dataframe): The dataframe containing the chi2 values of the TProfile histograms.
        bins (int, optional): The number of bins to use for the histogram. Defaults to 50.
        sizex (int, optional): The x-axis figsize of the plot. Defaults to 15.
        sizey (int, optional): The y-axis figsize of the plot. Defaults to 9.
        chi2options (str): The optional return parameter for chi2 or dist modes.
    """
    
    print("constructing tp data...")
    df_tp = df[df['f_type']=='TProfile']
    # hist_data = [df_tp['chi2ndf_vals'].values]    
    hist_data = df_tp['output_vals'].values

    print("plotting tp data...")
    plt.figure(figsize=(sizex,sizey))
    if "P" in chi2options:
        plt.hist(hist_data, bins=bins, alpha=0.7, color='b', label=f'TProfile P-Value:{chi2options} freq')
        plt.title(f'TProfile P-Values:{chi2options} Distplot')
    elif "NDF" in chi2options:
        plt.hist(hist_data, bins=bins, alpha=0.7, color='b', label=f'TProfile Chi2/NDF Value:{chi2options} freq')
        plt.title(f'TProfile Chi2/NDF Values:{chi2options} Distplot')
    else:
        plt.hist(hist_data, bins=bins, alpha=0.7, color='b', label=f'TProfile Chi2 Value:{chi2options} freq')
        plt.title(f'TProfile Chi2 Values:{chi2options} Distplot')
    plt.xlabel(f'Chi2:{chi2options}')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.grid(True)
    plt.show()
    
    
def plot_diffs(df1: pd.DataFrame, df2: pd.DataFrame,  hist_name_to_view: str, f_type: str, sizex:int=15, sizey:int=9):
    """
    Plots the differences of a selected histogram between the values of a root file and a reference root file.
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
        plt.plot(hist_one['x'], hist_two['occ'].values-hist_one['occ'].values, marker='o', color='blue')
        plt.scatter(hist_one['x'], hist_two['occ'].values-hist_one['occ'].values, marker='o', color='blue')
        plt.title(f'TH1-Diffs:{hist_name_to_view} (data=ref-file)')
        plt.xlabel(r'$\eta$')
        plt.ylabel('Occupancy')
        plt.grid(True)
        plt.legend(loc='upper right')
        plt.show()
        
    elif f_type == 'TH2':
        
        # Calculate and format plotting data for TH2 difference values
        hist_tmp = pd.DataFrame({'x':hist_one['x'], 'y':hist_one['y'], 'occ':hist_two['occ'].values-hist_one['occ'].values})
        pivot_table = hist_tmp.pivot(index='y', columns='x', values='occ') # Align y on the horizontal to be more like a ROOT histogram
        
        # Prepare plot parameters
        colors = [(0, 0, 1), (0, 1, 0), (1, 1, 0), (1, 0, 0)]  # Blue -> Green -> Yellow -> Red
        n_bins = 100  # Discretize the colormap into 100 bins
        cmap_name = 'root_colormap'
        root_cmap = mcolors.LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
        
        # Plot the heatmap of differences
        plt.figure(figsize=(sizex,sizey))
        sns.heatmap(pivot_table, cmap=root_cmap)
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
    
def plot_chi2_th1s(df_th1: pd.DataFrame, chi2options: str, sizex:int=15, sizey:int=9):
    """
    Plot chi2 values calculated from the TH1 histograms between file1 and file2.
    Args:
        df_th1 (DataFrame): _description_
        sizex (int, optional): _description_. Defaults to 15.
        sizey (int, optional): _description_. Defaults to 9.
        chi2options (str): The optional return parameter for chi2 or dist mode.
    """

    # Plot the normalized chi2 data of the TH1 histograms
    plt.figure(figsize=(sizex,sizey))
    # plt.scatter(df_th1['f_name'], df_th1['chi2ndf_vals'], marker='o', color='blue')
    plt.scatter(df_th1['f_name'], df_th1['output_vals'], marker='o', color='blue')
    if "P" in chi2options:
        plt.ylabel(f'P-Value:{chi2options}')
        plt.title(f'TH1 P-Values:{chi2options} values by hist, with norm option')
    elif "NDF" in chi2options:
        plt.ylabel(f'Chi2/NDF:{chi2options}')
        plt.title(f'TH1 Chi2/NDF:{chi2options} values by hist, with norm option')
    else:
        plt.ylabel(f'Chi2 Value:{chi2options}')
        plt.title(f'TH1 Chi2 Values:{chi2options} values by hist, with norm option')
    plt.xlabel('Hist Name')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()
    
def plot_chi2_th2s(df_th2: pd.DataFrame, chi2options: str, sizex:int=15, sizey:int=9):
    """
    Plot the chi2 values of TH2 histograms with various options calculated from given args.
    Args:
        df_th2 (Dataframe): Dataframe containing the Chi2 values of the TH2 histograms.
        sizex (int, optional): The x-axis figsize of the plot. Defaults to 15.
        sizey (int, optional): The y-axis figsize of the plot. Defaults to 9.
        chi2options (str): The optional return parameter for chi2 or dist mode.
        
    Returns:
        None: The histogram data is normalized and plotted in place. 
    """

    # Plot the normalized chi2 data of the TH2 histograms
    plt.figure(figsize=(sizex,sizey))
    # plt.scatter(df_th2['f_name'], df_th2['chi2ndf_vals'], marker='o', color='blue')
    plt.scatter(df_th2['f_name'], df_th2['output_vals'], marker='o', color='blue')
    if "P" in chi2options:
        plt.ylabel(f'P-Value:{chi2options}')
        plt.title(f'TH2 P-Values:{chi2options} values by hist, with norm option')
    elif "NDF" in chi2options:
        plt.ylabel(f'Chi2/NDF:{chi2options}')
        plt.title(f'TH2 Chi2/NDF:{chi2options} values by hist, with norm option')
    else:
        plt.ylabel(f'Chi2 Value:{chi2options}')
        plt.title(f'TH2 Chi2 Values:{chi2options} values by hist, with norm option')
    plt.xlabel('Hist Name')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()
    
def plot_chi2_tps(df_tp: pd.DataFrame, chi2options: str, sizex:int=15, sizey:int=9):
    """
    Plot chi2 values of TProfile histograms with various options calculated from given args.
    Args:
        df_tp (DataFrame): DataFrame of TProfile histograms' data.
        sizex (int, optional): _description_. Defaults to 15.
        sizey (int, optional): _description_. Defaults to 9.
        chi2options (str): The optional return parameter for chi2 or dist mode.
    
    Returns:
        None: The histogram data is normalized and plotted in place. 
    """

    plt.figure(figsize=(sizex,sizey))
    # plt.scatter(df_tp['f_name'], df_tp['chi2ndf_vals'], marker='o', color='blue')
    plt.scatter(df_tp['f_name'], df_tp['output_vals'], marker='o', color='blue')
    if "P" in chi2options:
        plt.ylabel(f'P-Value:{chi2options}')
        plt.title(f'TProfile P-Values:{chi2options} values by hist, with norm option')
    elif "NDF" in chi2options:
        plt.ylabel(f'Chi2/NDF:{chi2options}')
        plt.title(f'TProfile Chi2/NDF:{chi2options} values by hist, with norm option')
    else:
        plt.ylabel(f'Chi2 Value:{chi2options}')
        plt.title(f'TProfile Chi2 Values:{chi2options} values by hist, with norm option')
    plt.xlabel('Hist Name')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()
    
def process_normalization_args(args, chi2options:Optional[str]=None) -> pd.DataFrame:
    """
    Processes the normalization arguments and returns the chi2 dataframe based on the provided arguments.
    Args:
        args (Namespace): A namespace object containing the following attributes:
            - file (str): The file path to the data file.
            - ref (str): The reference data.
            - norm (bool): A flag indicating whether normalization should be applied.
        chi2options (str, optional): The optional return parameter for chi2 or dist mode. Defaults to None.
    Returns:
        DataFrame: The chi2 dataframe processed based on the provided arguments.
    Prints:
        str: Messages indicating the processing steps and whether normalization is applied.
    """

    print("Processing the chi2 dataframe...")
    chi2options = chi2options if chi2options is not None else ''
    normalization_option = args.norm if args.norm else ''
    
    if normalization_option:
        print(f"Normalizing {normalization_option} and Processing histogram datafile...")
    else:
        print("Processing histogram datafile no norm...")

    return chi2df(args.file, args.ref, chi2options, normalization_option)
    
def integral_normalize_histogram(hist_data: Dict[str, Any]) -> Any:
    """
    Normalize the chi-squared values in the histogram data by their integral.
    This function takes a dictionary containing chi-squared values and normalizes
    them by dividing each value by the sum of all chi-squared values. If the sum
    (integral) is zero, the original chi-squared values are returned to avoid
    division by zero.
    Parameters:
    hist_data (dict): A dictionary containing the key 'output_vals' which maps to
                      an array-like structure of chi-squared values.
    Returns:
    numpy.ndarray: An array of normalized chi-squared values.
    """

    # Get the output values (chi2/pvalue/chi2ndf) from the histogram data
    # chi2_vals = hist_data['chi2ndf_vals'].values
    output_vals = hist_data['output_vals'].values
    
    # Get the integral as the sum of magnitude of Chi2 values
    integral = sum(output_vals)

    # If that is 0, no need to scale them
    if integral == 0:
        return output_vals
    
    # Otherwise, scale them according to the integral
    return output_vals / integral


if __name__ == "__main__":
    
    # Set the ROOT ignore level to ignore warnings
    ROOT.gErrorIgnoreLevel = ROOT.kWarning
    
    # Set the seaborn plot style to look more like typical ROOT framework plots
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Define the argument parser
    parser = argparse.ArgumentParser(
        description='Calculate and analyze histogram data for validation using this tool.',
        epilog='''
        --- Additional Information ---

        Required:
            - Running with the singularity avd-tool-container.sif simply requires executing ". run_avd_tool_env.sh" in the terminal.
            - This script requires X11 installed on Linux, X11Server on Windows, or XQuartz on Mac to display on your local machine after running the command on lxplus.
            - You must have logged into lxplus with the -Y option for the plots to display on your local machine after running the command on lxplus.
              For example, on linux running "sudo apt-get update" followed by "sudo apt-get install xorg openbox" has successfully setup X11 on the Author's Linux machine.

        Command walkthrough:
            1. The --file argument is REQUIRED and should be the path to the root file.
            2. The --ref argument is REQUIRED and should be the path to the reference root file.
            3. The --htype argument is REQUIRED and should be the type of histograms to view results about.
            4. The --folders argument is REQUIRED and should be a list of folders to analyze. Provide at least one folder 
            such as "--folders Tau egamma".
            5. The --mode argument is REQUIRED and should be set to either 'dist', 'chi2', or 'diff' to display distribution of chi2 values, 
            chi2 values directory, or differences of actual values respectively.
            6. The --norm argument is OPTIONAL and can be set to 'unit_area', 'occ_area', 'same_entries', 'bin_width', or it can be left out for no applied normalization.
            7. The --hname argument is REQUIRED WHEN USING --diff and should be the full path from run_XXXXXXXX/etc/to/name_of_the_histogram to plot.
            Specific histogram hnames can be discovered in "--mode dist" or "--mode chi2" when mousing over plot values (see corner of plot).
            8a. The --uu argument is an OPTIONAL (chi2 or diff only) parameter and can be used to use unweighted histograms. Can combine with some other options.
            8b. The --uw argument is an OPTIONAL (chi2 or diff only) parameter and can be used to use unweighted histogram for the first histogram and weighted histogram for the second histogram. Can combine with some other options.
            8c. The --ww argument is an OPTIONAL (chi2 or diff only) parameter and can be used to use weighted histograms. Can combine with some other options.
            8d. The --p argument is an OPTIONAL (chi2 or diff only) parameter and can be used to use the p-values. Can combine with some other options.
            8e. The --perndf argument is an OPTIONAL (chi2 or diff only) parameter and can be used to calculate chi2 per degree of freedom. Can combine with some other options.
            Note: At this time, only the choice of --p or --perndf can be used for --htype TH2, not both.

        Example hname commands when using "--mode diff":
            (Example TH1 histogram for --hname when using --mode diff)
            --hname 'run_472943/CaloMonitoring/TileCellMon_NoTrigSel/General/Summary/TIME_execute

            (Example hname for TH2 histogram for --hname when using --mode diff)
            --hname run_472943/Tau/Calo/Tau_Calo_centFracVsLB

            (Example hname for TProfile histogram for --hname when using --mode diff)
            --hname run_472943/CaloMonitoring/TileCellMon_NoTrigSel/General/CellsXEta
    
        Full Commands Examples: (NOT UPDATED -- IGNORE TEMPORARILY)
        (When running the script locally)
            python plots_only_tool.py --file /eos/home-c/crandazz/SWAN_projects/ATLAS_DQ_Dashboard/data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1 --ref /eos/home-c/crandazz/SWAN_projects/ATLAS_DQ_Dashboard/data24_13p6TeV.00472943.physics_Main.merge.HIST.r15810_p6305.root --htype TH1 --folders Tau egamma --mode diff --hname run_472943/CaloMonitoring/TileCellMon_NoTrigSel/General/Summary/TIME_execute
            python plots_only_tool.py --file data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1 --ref data24_13p6TeV.00472943.physics_Main.merge.HIST.r15810_p6305.root --htype TH1 --folders Tau egamma --mode diff --hname run_472943/CaloMonitoring/TileCellMon_NoTrigSel/General/Summary/TIME_execute
            python plots_only_tool.py --file /eos/home-c/crandazz/SWAN_projects/ATLAS_DQ_Dashboard/data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1 --ref /eos/home-c/crandazz/SWAN_projects/ATLAS_DQ_Dashboard/data24_13p6TeV.00472943.physics_Main.merge.HIST.r15810_p6305.root --htype TH1 --folders CaloMonitoring egamma --mode chi2 --norm occ_area --perndf
            python plots_only_tool.py --file data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1 --ref data24_13p6TeV.00472943.physics_Main.merge.HIST.r15810_p6305.root --htype TH1 --folders CaloMonitoring egamma --mode chi2 --norm occ_area --perndf
        (When running the script on LXPLUS, assumed to be in the same directory as the script OR in a cernbox eos location)
            python plots_only_tool.py --file /eos/home-c/crandazz/SWAN_projects/ATLAS_DQ_Dashboard/data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1 --ref /eos/home-c/crandazz/SWAN_projects/ATLAS_DQ_Dashboard/data24_13p6TeV.00472943.physics_Main.merge.HIST.r15810_p6305.root --folders Tau --htype TH2 --mode diff --hname run_472943/Tau/Calo/Tau_Calo_centFracVsLB
            python plots_only_tool.py --file data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1 --ref data24_13p6TeV.00472943.physics_Main.merge.HIST.r15810_p6305.root --folders Tau --htype TH2 --mode diff --hname run_472943/Tau/Calo/Tau_Calo_centFracVsLB
            
        --- Algorithm Info ---
            For the --mode chi2 option and --htype TH2, the algorithm will normalize the histograms by the sum of weights squared (Sumw2) and scale the reference histogram by the 2D histogram. 
            Following that, it will calculate the chi2 values and return a choice of p_value, chi2_value, or chi2_per_ndf depending on if --perndf --p or no additional parameter is supplied.
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Define the required arguments
    parser.add_argument('--file', type=str, help='Required: Path to the root file.', required=True)
    parser.add_argument('--ref', type=str, help='Required: Path to the reference root file.', required=True)
    parser.add_argument('--htype', type=str, choices=['TH1', 'TH2', 'TProfile'], help='Required: Choose the type of histograms to view results about.', required=True)
    parser.add_argument('--folders', nargs='+', required=True,
                        help='Required: List of folders to analyze. Provide at least one folder.')
    parser.add_argument('--mode', type=str, choices=['dist', 'chi2', 'diff'], help='Required: Set plot mode to distribution, chi2, or value differences.', required=True)
    
    # Add additional arguments for various modes
    parser.add_argument('--norm', type=str, choices=['unit_area', 'occ_area', 'same_entries', 'bin_width', ''], default="", help='Optional for chi2 or dist:Normalization mode as either {None, unit_area, same_entries, bin_width}.')
    parser.add_argument('--hname', type=str, help='Required for diff: Provide the name of the histogram to plot.')
    parser.add_argument('--uu', action='store_true', help='Optional for chi2 or dist: Use unweighted histograms. Can combine with some other options.')
    parser.add_argument('--uw', action='store_true', help='Optional for chi2 or dist: Use unweighted histogram for the first histogram and weighted histogram for the second histogram. Can combine with some other options.')
    parser.add_argument('--ww', action='store_true', help='Optional for chi2 or dist: Use weighted histograms. Can combine with some other options.')
    parser.add_argument('--p', action='store_true', help='Optional for chi2 or dist: Use the p-values. Can combine with some other options.')
    parser.add_argument('--perndf', action='store_true', help='Optional for chi2 or dist: Calculate chi2 per degree of freedom. Can combine with some other options.')
    
    # Parse the arguments
    # In this application, args is defined here globally to be used particularly in the validate_hists function or other functions that may need access to it
    args = parser.parse_args()

    # TODO: verify if they do or do not need to be in the working directory
    print("NOTE: files may need to be in the working directory of this script to work properly! (Update pending)")
    
    
    ###################
    # ARGS PROCESSING #
    ###################
    
    # Handle mode error
    if (args.uu or args.uw or args.ww or args.p or args.perndf) and not (args.mode=='dist' or args.mode=='chi2'):
        parser.error("--uu, --uw, --ww, --p, and --perndf require either --mode dist or --mode chi2 to be specified.")
    
    
    # Display given configurations of args from user
    print("--Current Configurations---")
    print(f"file: {args.file}")
    print(f"ref: {args.ref}")
    print(f"histogram type:{args.htype}")
    print(f"folders: {args.folders}")
    
    
    # Processing for chi2options is triggered when "--mode chi2" or "--mode dist" is selected
    if args.mode=='chi2' or args.mode=='dist':
        # Construct the chi2options for Chi2Test based on various mode options given by user
        chi2options = ""
        if args.perndf:
            chi2options += "CHI2/NDF"
            if args.uu:
                chi2options += " UU"
                # TODO: perndf and p cannot be used together at this time
                # if args.p:
                    # chi2options += " P"
            elif args.uw:
                chi2options += " UW"
                # TODO: perndf and p cannot be used together at this time
                # if args.p:
                    # chi2options += " P"
            elif args.ww:
                chi2options += " WW"
                # TODO: perndf and p cannot be used together at this time
                # if args.p:
                    # chi2options += " P"
            # TODO: perndf and p cannot be used together at this time
            # elif args.p:
                # chi2options += " P"
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
    
    # Continue displaying the remainder of the user set configurations when running the script
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
        
        
    # Process the required data for the plots when in "--mode" dist or "--mode chi2"
    if args.mode == 'dist' or args.mode == 'chi2':
        
        # Process normalization args
        try:
            df = process_normalization_args(args, chi2options)
        except NameError:
            df = process_normalization_args(args)
            
    # Process the program when in "--mode chi2"
    if not args.mode=='diff':
        # Plot either the distribution or Chi2 values with set options of TH1,TH2, or TProfile histograms
        if  args.htype == "TH1":
            
            print("Getting TH1 data...")
            df_th1 = df[df['f_type']=='TH1']
            
            if args.norm == 'occ_area':
                print("Normalizing TH1 Chi2 vals to occupancy area...")
                # chi2_normed_vals = integral_normalize_histogram(df_th1) # Normalizes the chi2_val occupancies
                # df_th1.loc[:,'chi2ndf_vals'] = chi2_normed_vals
                output_vals_normed = integral_normalize_histogram(df_th1) # Normalizes the chi2_val occupancies
                df_th1.loc[:,'output_vals'] = output_vals_normed
                
            print("Plotting TH1 histograms...")
            if args.mode == 'dist':
                plot_dist_th1(df_th1, chi2options)
                
            elif args.mode == 'chi2':
                plot_chi2_th1s(df_th1, chi2options)
                
        elif args.htype == "TH2":
            
            print("Getting TH2 data...")
            df_th2 = df[df['f_type']=='TH2']
            
            if args.norm == 'occ_area':
                print("Normalizing TH2 Chi2 vals to occupancy area...")
                # chi2_normed_vals = integral_normalize_histogram(df_th2)
                # df_th2.loc[:,'chi2ndf_vals'] = chi2_normed_vals
                output_vals_normed = integral_normalize_histogram(df_th2)
                df_th2.loc[:,'output_vals'] = output_vals_normed
                
            print("Plotting TH2 histograms...")
            if args.mode == 'dist':
                plot_dist_th2(df_th2, chi2options)
                
            elif args.mode == 'chi2':
                plot_chi2_th2s(df_th2, chi2options)
                
        elif args.htype == "TProfile":
            
            print("Getting TProfile data...")
            df_tp = df[df['f_type']=='TProfile']
            if args.norm == 'occ_area':
                print("Normalizing TProfile Chi2 vals to occupancy area...")
                # chi2_normed_vals = integral_normalize_histogram(df_tp)
                # df_tp.loc[:,'chi2ndf_vals'] = chi2_normed_vals
                output_vals_normed = integral_normalize_histogram(df_tp)
                df_tp.loc[:,'output_vals'] = output_vals_normed
                
            print("Plotting TProfile histograms...")
            if args.mode == 'dist':
                plot_dist_tps(df_tp, chi2options)
                
            elif args.mode == 'chi2':
                plot_chi2_tps(df_tp, chi2options)
            
    # Process the program when in "--mode diff"
    if args.mode == 'diff':
        
        if not args.hname:
            parser.error("--diff additionally requires --hname")
            
        print('Processing "file" histogram data...')
        file_data = hist_to_df(args.file)
        
        print('Processing "ref" histogram data...')
        ref_data = hist_to_df(args.ref)
        
        print("Plotting difference values...")
        plot_diffs(file_data, ref_data, args.hname, args.htype)
