# Simple Usage:". run_avd_tool_env.sh"

# 1. Put the path/to/avd-tool-container.sif where it can be accessed by the container (afs only)

# 2. Put get the path/to/atlas_validation_tool.py (in my public area) where it can be accessed by the container (afs only)

# 3. Put the path/to/root and /path/toreference files where they an be accessed by the container (afs only) 

# 4. Drop into container shell:
# This will drop you to the shell inside the environment where your working directory will be
# working_directory_for_container = wherever you ran ". run_avd_tool_env.sh"
apptainer shell /eos/user/c/crandazz/SWAN_projects/ATLAS_DQ_Dashboard/avd-tool-container.sif

# From there use path/to/atlas_validation_tool.py -h for docs on how to use atlas_validation_tool.py