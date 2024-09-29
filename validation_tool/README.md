## How to create the .sif

singularity.def is the file that can be used to create the .sif container directly, but in practice, I converted it from docker container on dockerhub to a sif using the following command:<br>

```bash
singularity build avd-tool-container.sif docker://rdccdr/dockerhub:avd-tool-env   # (what i called it on dockerhub or w/e)
```

To get that on dockerhub, we discuss that in the next section

## How to create and get a docker container/image on dockerhub for converting to .sif

1. avd-tools-env was created in docker locally using the "Dockerfile" we have in the same folder as this readme and the following commands (see docker_setup.sh)


Note, these commands are not given in any order YET, this is just a collection of the useful commands:

```bash
# Run only once
sudo docker build -t atl-tool-env .

# Run this command to start the container
docker run -it --rm atl-tool-env

# If you need to Restart docker daemon
sudo systemctl restart docker

# Logout first
docker logout

# Now login
docker login -u rdccdr

# Change tags to expected docker hub format
docker tag avd-tool-env:latest rdccdr/dockerhub:avd-tool-env

# Push the image to docker hub
# docker push rdccdr/dockerhub:avd-tool-env
docker push rdccdr/avd-tool-env:latest

# --- (LXPLUS) ----
# After it successfully loading to dockerhub, we login to lxplus
# Move to my eos area
# cd /eos/home-c/crandazz

# If you would like to build the .sif from the dockerhub image, now use this
apptainer build --docker-login avd-tool-container.sif docker://rdccdr/dockerhub:avd-tool-env
# or
singularity build --docker-login avd-tool-container.sif docker://rdccdr/dockerhub:avd-tool-env
# enter docker username
# enter docker password

# To run the container from dockerhub use this
singularity run docker://rdccdr/dockerhub:avd-tool-env

# Some other commands I used which may or may not help
#mkdir -p /eos/user/c/crandazz/apptainer_temp
#mkdir -p /eos/user/c/crandazz/apptainer_cache
#export APPTAINER_TMPDIR=/eos/user/c/crandazz/apptainer_temp
#export APPTAINER_CACHEDIR=/eos/user/c/crandazz/apptainer_cache
#(cgpt and https://usatlas.readthedocs.io/projects/af-docs/en/latest/Containers/UsingSingularity/)

```

Now, in what order do we run these?

1. Create the Dockerfile (we have given this in the repo)
2. build it: 
```bash
sudo docker build -t atl-tool-env .
```
3. run it and check that it works: 
```bash
docker run -it --rm atl-tool-env
```
4. try to logout of docker: 
```bash
docker logout
```
5. login to docker: docker 
```bash
login -u <your_username>, enter password
```
6. Change tags to expected docker hub format:
```bash
docker tag avd-tool-env:latest rdccdr/avd-tool-env # try this first, or
docker tag avd-tool-env:latest rdccdr/dockerhub:avd-tool-env
```
7. Push the image to dockerhub
```bash
docker push rdccdr/avd-tool-env:latest
```
8. On your local machine, make sure singularity is installed (see singaulrity_setup.sh, best to consult their docs, it requires installing go and a host of things) UNLESS you already have singularity installed on a linux machine
9. Convert the docker container to a singularity image with singularity now installed
```bash
singularity build avd-tools-container.sif docker://rdccdr/dockerhub:avd-tools-env # This is the current format/name/tag it exists on my dockerhub, not sure if i can remove the dockerhub part
```
10. Upload that image to lxplus in some accessible location
```bash
scp avd-tools-container.sif username@lxplus.cern.ch:/path/to/your/directory
```

<hr>

If the avd-tools-container.sif already is built and exists on lxplus, start your steps here. If not, start at step 1 above to build and push the container to lcplus

11. Now, login to lxplus with 
```bash
ssh -Y username@lxplus.cern.ch
```
12. make sure that X11/XQuarts/X11server etc has properly forwarded your display
```bash
echo $DISPLAY # should show something like   "localhost" or ":0" or something
```
13. Next, we do not want to execute commands to the .sif container, we want to drop into a shell directly (I may or may have created a run_avd_tools_container.sh script to simplify this command)
```bash
apptainer shell path/to/avd-tools-container.sif # No sure when/how the apptainer command got substituted, but theres documentation of when i used those commands in the .sh files, may need to use
singularity shell path/to/avd-tools-container.sif
```
14. If all goes well, then you will be in the container at /afs/cern.ch/user/<your_first_username_letter>/<your_username> which will have access to the datafiles you have stored there. It should also have access to other afs areas that are public (as it is linked to afs). The container itself may contain a copy of plots_only_tool.py (verify this) if so run that. If not, navigate to /afs/cern.ch/user/c/crandazz/public for plots_only_tool.py

15. Finally, with the path for plots_only_tool.py in hand and being inside the container, you can run plots_only_tool.py -h to get documentation on how to run the script and its specific commands to do the validation