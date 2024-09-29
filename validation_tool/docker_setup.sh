# Run only once
# sudo docker build -t atl-tool-env .

# Run this command to start the container
docker run -it --rm atl-tool-env

# If you need to Restart docker daemon
# sudo systemctl restart docker

# Logout first
# docker logout

# Now login
# docker login -u rdccdr

# Change tags to expected docker hub format
# docker tag avd-tool-env:latest rdccdr/dockerhub:avd-tool-env

# Push the image to docker hub
# docker push rdccdr/dockerhub:avd-tool-env
# docker push rdccdr/avd-tool-env:latest

# After it successfully loading to dockerhub, we login to lxplus
# Move to my eos area
# cd /eos/home-c/crandazz
# singularity run docker://rdccdr/dockerhub:avd-tool-env
#mkdir -p /eos/user/c/crandazz/apptainer_temp
#mkdir -p /eos/user/c/crandazz/apptainer_cache
#export APPTAINER_TMPDIR=/eos/user/c/crandazz/apptainer_temp
#export APPTAINER_CACHEDIR=/eos/user/c/crandazz/apptainer_cache
#(cgpt and https://usatlas.readthedocs.io/projects/af-docs/en/latest/Containers/UsingSingularity/)

# apptainer build --docker-login avd-tool-container.sif docker://rdccdr/dockerhub:avd-tool-env


# singularity build --docker-login avd-tool-container.sif docker://rdccdr/dockerhub:avd-tool-env
# enter docker username
# enter docker password

