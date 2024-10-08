Notice: All information is currently in the process of being and finalized. It will be available in the near future. All instructions are given from the perpective of an Ubuntu based linux operating system/.

### For script instructions ###

use the -h parameter "python atlas_validation_tool.py -h"

### Installation/Running of Docker Container (for locally running container) ###

1. "docker pull rdccdr/dockerhub:avd-tool-env"
2. "docker run -it rdccdr/dockerhub:avd-tool-env /bin/bash" puts you in the shell (make sure you have access to the data files and script from the container)
3. "python atlas_validation_tool.py -h"


### Installation/Running of Singularity (for locally running container) ###
1. See/run singularity_setup.sh
NOTE: "./singularity_setup.sh" will not run out of the box (use it as a guide for semi-manual installation instructions)
2. run "singularity run avd-tool-container.sif" (make sure you have access to the data files and script from the container)
3. run "python atlas_validation_tool.py" 

Alternately: (For lxplus or locally)
1. Update the path inside "run_avd_tool_env.sh" to be according to where the .sif container is
2. execute "./run_avd_tool_env.sh" (puts you in container, make sure you have access to the script and data files)
3. run "python atlas_validation_tool.py" 

### Installation/Running on lxplus with "lsetup root" ###
1. login to lxplus with "ssh -Y username@lxplus.cern.ch"
2. run "lsetup root" and run the lsetup root command suggested by lxplus
3. copy the atlas_validation_tool.py and datafiles into a directory you have access to
4. run "python atlas_validation_tool.py to begin

### Installation/Running directly from custom ROOT environment ###
1. build an env using conda-forge that contains ROOT(from conda-forge), matplotlib, pandas, and seaborn
 "conda create -c conda-forge --name my-environment-name root matplotlib pandas seaborn"
2. "conda activate my-environment-name"
3. "python atlas_validation_tool.py -h"

### Building the Docker Container from Dockerfile - Instructions ###

#### 1. Install Docker
 For an example installation on 20.04 Ubuntu, run the following commands in terminal:
  sudo apt install docker.io
  sudo systemctl enable --now docker

#### 2. Install Docker Compose,                                                                                                         
 For an example installation on 20.04 Ubuntu, we recommend following the installation instructions on DigitalOcean's website for installing docker compose on Ubuntu 20.04. Make sure not to install the standalone version for the following steps to function properly.

#### 3. Navigate to the github containing the installtion files (currently https://github.com/CaryRandazzo/AtlasValidationDashboard),

#### 4. In a terminal at the location you want the files stored enter the command:
Fork the repository at https://github.com/CaryRandazzo/AtlasValidationDashboard

#### 5. Navigate to the /AtlasValidationDashboard/docker-server/ directory and execute the command:
docker compose build
It should successfully build.

#### 6. Next, execute the command:
docker compose up
This should return an error due to the data files not being present.

#### 7. Install the data and set the configuration folder by the following.
In order to change the configuration, (for now) place the data files to compare in the /AtlasValidationDashboard/docker-server/cary-data/ folder. 
(This may require elevated priveledges to copy the files into the data folder. This folder will be generated after running the previous docker commands.)

#### 8. Navigate to the directory where the two data files are located and run something similar to:
sudo cp <datafile1> /AtlasValidationDashboard/docker-server/cary-data/    and
sudo cp <datafile1> /AtlasValidationDashboard/docker-server/cary-data/

#### 9. Navigate to the /AtlasValidationDashboard/docker-server/cary-server/server/config.py folder and set the fileOne string variable to the name 
of the first file to compare, similarly set the fileTwo string variable to the name of the second file to compare, and folder_list to the 
folders of interest to analyze for the comparison .

#### 10. Save the changes to the config.

#### 11. In /AtlasValidationDashboard/docker-server/ execute the command:
docker compose build

#### 12. execute the command:
docker compose up

#### 13. Open a web browser and navigate to the url: 
http://localhost:1337/

#### Final Notes
The dashboard should be visible.

Use ctrl+z in termal to close the server, docker compose down to take down the currently up version of the server, and sometimes rebuilding may be
necessary.
�
