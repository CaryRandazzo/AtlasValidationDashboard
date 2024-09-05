# Create a conda environment that automatically installs CERN's ROOT framework
conda create -n ROOTenv -c conda-forge root -y

# Activate the conda environment
conda activate ROOTenv

# Install the required Python packages
pip install -r requirements.txt