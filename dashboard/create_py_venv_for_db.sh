# Create a conda environment that automatically installs CERN's ROOT framework
# conda create -n ROOTenv -c conda-forge root -y
conda create -n ROOTenv -c conda-forge python=3.10 root pandas matplotlib seaborn numpy sqlalchemy -y

# Activate the conda environment
conda activate ROOTenv


conda install pandas -y
conda install seaborn -y
conda install matplotlib -y
conda install numpy -y

# Install the required Python packages
pip install -r requirements.txt