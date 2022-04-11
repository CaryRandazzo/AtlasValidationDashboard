Installation and Run Directions:

- Install Docker

- Install Docker Compose,                                                                                                         

- Navigate to the github containing the installtion files (currently CaryRandazzo/AtlasValidationDashboard/),

- Then click code and in terminal at the location you want the files stored enter the command:
git pull https://github.com:CaryRandazzo/AtlasValidationDashboard.git

- Navigate to the /AtlasValidationDashboard/docker-server/ directory and execute the command:
docker compose build
It should successfully build.

- Next, execute the command:
docker compose up
This should return an error due to the data files not being present.

- Install the data and set the configuration folder by the following.
In order to change the configuration, (for now) place the data files to compare in the /AtlasValidationDashboard/docker-server/cary-data/ folder. 
(This may require elevated priveledges to copy the files into the data folder. This folder will be generated after running the previous docker commands.)

- Navigate to the directory where the two data files are located and run something similar to:
sudo cp <datafile1> /AtlasValidationDashboard/docker-server/cary-data/    and
suco cp <datafile1> /AtlasValidationDashboard/docker-server/cary-data/

- Then navigate to the /AtlasValidationDashboard/docker-server/cary-server/server/config.py folder and set the fileOne string variable to the name 
of the first file to compare, similarly set the fileTwo string variable to the name of the second file to compare, and folder_list to the 
folders of interest to analyze for the comparison .

- Save the changes to the config.

- Finally, in /AtlasValidationDashboard/docker-server/ execute the command:
docker compose build

- Then execute the command:
docker compose up

- Then open a web browser and navigate to the url: 
http://localhost:1337/

The dashboard should be visible.

Use ctrl+z in termal to close the server, docker compose down to take down the currently up version of the server, and sometimes rebuilding may be
necessary.

