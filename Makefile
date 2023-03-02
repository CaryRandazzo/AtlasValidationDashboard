# declare bash as shell over sh for newer features
SHELL := /bin/bash

# server name constants
DATAGEN := "data-gen"
DASHBOARD := "dashboard"
ATLASNET := "atlas-net"
REGISTRY := "hub.docker.com"


#####################################################
# DATA-GENERATION
#####################################################
.PHONY: build-data-gen
build-data-gen:
	docker build -t $(DATAGEN) $(DATAGEN)


.PHONY: run-data-gen
run-data-gen:
	[[ ! -z $$(docker images -q $(DATAGEN):latest 2> /dev/null) ]] || \
		docker build \
			-t $(DATAGEN) $(DATAGEN)
	[[ ! -z $$(docker ps -aq --filter name=$(DATAGEN) 2> /dev/null) ]] || \
		docker run -it --rm \
			-v $$(pwd)/$(DATAGEN)/src:/app/src:ro \
			$(DATAGEN) python3 /app/src/stage1.py
			# -p 8888:8888 \
			# -v $$(pwd)/data-files:/app/data \


#####################################################
# TENSORFLOW
#####################################################
.PHONY: build-tensorflow
build-tensorflow:
	docker build -t $(ATLASNET) $(ATLASNET)


.PHONY: run-tensorflow
run-tensorflow:
	[[ ! -z $$(docker images -q $(ATLASNET):latest 2> /dev/null) ]] || \
		docker build \
			-t $(ATLASNET) $(ATLASNET)
	[[ ! -z $$(docker ps -aq --filter name=$(ATLASNET) 2> /dev/null) ]] || \
		docker run -it --rm \
			-v $$(pwd)/$(ATLASNET)/src:/app/src \
			-v $$(pwd)/$(ATLASNET)/data-files:/app/data \
			--gpus all \
			$(ATLASNET) python3 /app/src/atlasUnsupAnomDet.py


#####################################################
# DASHBOARD
#####################################################
.PHONY: build-dashboard
build-dashboard:
	docker build -t $(DASHBOARD) $(DASHBOARD)


.PHONY: run-dashboard
run-dashboard:
	[[ ! -z $$(docker images -q $(DASHBOARD):latest 2> /dev/null) ]] || \
		docker build \
			-t $(DASHBOARD) $(DASHBOARD)
	[[ ! -z $$(docker ps -aq --filter name=$(DASHBOARD) 2> /dev/null) ]] || \
		docker run -it \
			-v $$(pwd)/$(DASHBOARD)/src:/app/src \
			-v $$(pwd)/$(DASHBOARD)/data-files:/app/data \
			-p 1337:1337 \
			--name $(DASHBOARD) $(DASHBOARD)


#####################################################
# UTILITIES
#####################################################
.PHONY: push-to-registry
push-to-registry:
	docker build \
		-t $(REGISTRY)/$(DASHBOARD):latest $(DASHBOARD)
	docker push $(REGISTRY)/Randazzo-CERN-ATLAS-DASHBOARD:latest


.PHONY: diag
diag:
	echo "=====containers====="
	docker ps -a
	echo
	echo "======networks======"
	docker network ls
	echo
	echo "=====ip addresses====="
	echo $(DATAGEN)
	docker inspect -f \
		'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
		$(DATAGEN) 2> /dev/null || echo "none"
	echo $(ATLASNET)
	docker inspect -f \
		'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
		$(ATLASNET) 2> /dev/null || echo "none"
	echo $(DASHBOARD)
	docker inspect -f \
		'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
		$(DASHBOARD) 2> /dev/null || echo "none"


.PHONY: armageddon
armageddon: clean
	docker ps -aq | xargs docker rm -f 2> /dev/null || echo "none"
	docker images -aq | xargs docker rmi -f 2> /dev/null || echo "none"
	docker system prune -af
