# import ROOT
# import os

# def get_histogram_type(file_path, hist_path):
#     # Check if the file exists
#     if not os.path.exists(file_path):
#         print(f"Error: File does not exist at path: {file_path}")
#         return None
    
#     # Open the ROOT file
#     file = ROOT.TFile.Open(file_path)
    
#     # Check if the file is open
#     if not file or file.IsZombie():
#         print("Error: Could not open file")
#         return None
    
#     # Retrieve the histogram from the given path
#     hist = file.Get(hist_path)
    
#     # Check if the histogram is valid
#     if not hist:
#         print(f"Error: Could not retrieve histogram at path: {hist_path}")
#         file.ls()  # List the contents of the file for debugging
#         return None
    
#     # Get the class name of the histogram
#     hist_type = hist.ClassName()
    
#     # Close the file
#     file.Close()
    
#     return hist_type

# def list_histograms_in_directory(file_path, dir_path):
#     # Check if the file exists
#     if not os.path.exists(file_path):
#         print(f"Error: File does not exist at path: {file_path}")
#         return None
    
#     # Open the ROOT file
#     file = ROOT.TFile.Open(file_path)
    
#     # Check if the file is open
#     if not file or file.IsZombie():
#         print("Error: Could not open file")
#         return None
    
#     # Retrieve the directory
#     directory = file.Get(dir_path)
    
#     # Check if the directory is valid
#     if not directory:
#         print(f"Error: Could not retrieve directory at path: {dir_path}")
#         file.ls()  # List the contents of the file for debugging
#         return None
    
#     # List all keys in the directory
#     keys = directory.GetListOfKeys()
    
#     # Filter and print histogram names
#     hist_names = []
#     for key in keys:
#         obj = key.ReadObj()
#         if isinstance(obj, ROOT.TH1) or isinstance(obj, ROOT.TH2) or isinstance(obj, ROOT.TProfile):
#             hist_names.append(key.GetName())
    
#     # Close the file
#     file.Close()
    
#     return hist_names

# if __name__ == "__main__":
#     # Example usage
#     file_path = "data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1"
#     hist_path = "run_472943/Tau/Trigger/tautrigger2/Calo/tautriggered2_Calo_EMRadius"
#     dir_path = "/".join(hist_path.split('/')[:-1])  # Get the directory path above hist_path

#     hist_type = get_histogram_type(file_path, hist_path)
#     if hist_type:
#         print(f"The histogram type is: {hist_type}")

#     hist_names = list_histograms_in_directory(file_path, dir_path)
#     if hist_names:
#         print(f"Histograms in directory {dir_path}:")
#         for name in hist_names:
#             print(name)



# import ROOT
# import os

# def get_histogram_type(file_path, hist_path):
#     # Check if the file exists
#     if not os.path.exists(file_path):
#         print(f"Error: File does not exist at path: {file_path}")
#         return None
    
#     # Open the ROOT file
#     file = ROOT.TFile.Open(file_path)
    
#     # Check if the file is open
#     if not file or file.IsZombie():
#         print("Error: Could not open file")
#         return None
    
#     # Retrieve the histogram from the given path
#     hist = file.Get(hist_path)
    
#     # Check if the histogram is valid
#     if not hist:
#         print(f"Error: Could not retrieve histogram at path: {hist_path}")
#         file.ls()  # List the contents of the file for debugging
#         return None
    
#     # Get the class name of the histogram
#     hist_type = hist.ClassName()
    
#     # Close the file
#     file.Close()
    
#     return hist_type

# def list_histograms_in_directory(file_path, dir_path):
#     # Check if the file exists
#     if not os.path.exists(file_path):
#         print(f"Error: File does not exist at path: {file_path}")
#         return None
    
#     # Open the ROOT file
#     file = ROOT.TFile.Open(file_path)
    
#     # Check if the file is open
#     if not file or file.IsZombie():
#         print("Error: Could not open file")
#         return None
    
#     # Retrieve the directory
#     directory = file.Get(dir_path)
    
#     # Check if the directory is valid
#     if not directory:
#         print(f"Error: Could not retrieve directory at path: {dir_path}")
#         file.ls()  # List the contents of the file for debugging
#         return None
    
#     # List all keys in the directory
#     keys = directory.GetListOfKeys()
    
#     # Filter and print histogram names
#     hist_names = []
#     for key in keys:
#         obj = key.ReadObj()
#         if isinstance(obj, ROOT.TH1) or isinstance(obj, ROOT.TH2) or isinstance(obj, ROOT.TProfile):
#             hist_names.append(key.GetName())
    
#     # Close the file
#     file.Close()
    
#     return hist_names

# if __name__ == "__main__":
#     # Example usage
#     file_path = "data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1"
#     hist_path = "run_472943/Tau/Trigger/tauTrigger2/Calo/tautriggered2_Calo_EMRadius"  # Corrected path
#     dir_path = "/".join(hist_path.split('/')[:-1])  # Get the directory path above hist_path

#     hist_type = get_histogram_type(file_path, hist_path)
#     if hist_type:
#         print(f"The histogram type is: {hist_type}")

#     hist_names = list_histograms_in_directory(file_path, dir_path)
#     if hist_names:
#         print(f"Histograms in directory {dir_path}:")
#         for name in hist_names:
#             print(name)

import ROOT
import os

def get_histogram_type(file_path, hist_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File does not exist at path: {file_path}")
        return None
    
    # Open the ROOT file
    file = ROOT.TFile.Open(file_path)
    
    # Check if the file is open
    if not file or file.IsZombie():
        print("Error: Could not open file")
        return None
    
    # Retrieve the histogram from the given path
    hist = file.Get(hist_path)
    
    # Check if the histogram is valid
    if not hist:
        print(f"Error: Could not retrieve histogram at path: {hist_path}")
        file.ls()  # List the contents of the file for debugging
        return None
    
    # Get the class name of the histogram
    hist_type = hist.ClassName()
    
    # Close the file
    file.Close()
    
    return hist_type

def list_histograms_in_directory(file_path, dir_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File does not exist at path: {file_path}")
        return None
    
    # Open the ROOT file
    file = ROOT.TFile.Open(file_path)
    
    # Check if the file is open
    if not file or file.IsZombie():
        print("Error: Could not open file")
        return None
    
    # Retrieve the directory
    directory = file.Get(dir_path)
    
    # Check if the directory is valid
    if not directory:
        print(f"Error: Could not retrieve directory at path: {dir_path}")
        file.ls()  # List the contents of the file for debugging
        return None
    
    # List all keys in the directory
    keys = directory.GetListOfKeys()
    
    # Filter and print histogram names
    hist_names = []
    for key in keys:
        obj = key.ReadObj()
        if isinstance(obj, ROOT.TH1) or isinstance(obj, ROOT.TH2) or isinstance(obj, ROOT.TProfile):
            hist_names.append(key.GetName())
    
    # Close the file
    file.Close()
    
    return hist_names

def print_histogram_data(file_path, hist_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File does not exist at path: {file_path}")
        return
    
    # Open the ROOT file
    file = ROOT.TFile.Open(file_path)
    
    # Check if the file is open
    if not file or file.IsZombie():
        print("Error: Could not open file")
        return
    
    # Retrieve the histogram from the given path
    hist = file.Get(hist_path)
    
    # Check if the histogram is valid
    if not hist:
        print(f"Error: Could not retrieve histogram at path: {hist_path}")
        file.ls()  # List the contents of the file for debugging
        return
    
    # Print histogram data
    if isinstance(hist, ROOT.TH1):
        print(f"Histogram {hist_path} data:")
        for bin in range(1, hist.GetNbinsX() + 1):
            print(f"Bin {bin}: {hist.GetBinContent(bin)}")
    elif isinstance(hist, ROOT.TH2):
        print(f"Histogram {hist_path} data:")
        for xbin in range(1, hist.GetNbinsX() + 1):
            for ybin in range(1, hist.GetNbinsY() + 1):
                print(f"Bin ({xbin}, {ybin}): {hist.GetBinContent(xbin, ybin)}")
    elif isinstance(hist, ROOT.TProfile):
        print(f"Histogram {hist_path} data:")
        for bin in range(1, hist.GetNbinsX() + 1):
            print(f"Bin {bin}: {hist.GetBinContent(bin)}")
    else:
        print(f"Unsupported histogram type: {hist.ClassName()}")
    
    # Close the file
    file.Close()

if __name__ == "__main__":
    # Example usage
    file_path = "data24_13p6TeV.00472943.physics_Main.merge.HIST.f1442_h464._0001.1"
    hist_path = "run_472943/Tau/Trigger/tauTrigger2/Calo/tautriggered2_Calo_EMRadius"  # Corrected path
    dir_path = "/".join(hist_path.split('/')[:-1])  # Get the directory path above hist_path

    hist_type = get_histogram_type(file_path, hist_path)
    if hist_type:
        print(f"The histogram type is: {hist_type}")

    hist_names = list_histograms_in_directory(file_path, dir_path)
    if hist_names:
        print(f"Histograms in directory {dir_path}:")
        for name in hist_names:
            print(name)
    
    # Print histogram data
    print_histogram_data(file_path, hist_path)