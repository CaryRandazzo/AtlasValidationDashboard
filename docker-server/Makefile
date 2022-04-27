# declare bash as shell over sh for newer features
SHELL := /bin/bash

# server name constants
SERVER := "server"
NETWORK := "atlas-net"
REGISTRY := "hub.docker.com"


.PHONY: build-network
build-network:
	[[ ! -z $$(docker network ls -q --filter name=$(NETWORK) 2> /dev/null) ]] || \
		docker network create --driver bridge $(NETWORK)


.PHONY: build-images
build-images:
	[[ ! -z $$(docker images -q $(SERVER):latest 2> /dev/null) ]] || \
		docker build \
			-t $(SERVER) $(SERVER)


.PHONY: run-server
run-server: build-network build-images
	[[ ! -z $$(docker ps -aq --filter name=$(SERVER) 2> /dev/null) ]] || \
		docker run -it \
			-v $$(pwd)/$(SERVER)/src:/app/src \
			-v $$(pwd)/data-files:/app/data \
			--net $(NETWORK) -p 1337:1337 \
			--name $(SERVER) $(SERVER)


.PHONY: push-to-registry
push-to-registry:
	docker build \
		-t $(REGISTRY)/$(SERVER):latest $(SERVER)
	docker push $(REGISTRY)/$(SERVER):latest


.PHONY: diag
diag:
	echo "=====containers====="
	docker ps -a
	echo
	echo "======networks======"
	docker network ls
	echo
	echo "=====ip addresses====="
	echo $(SERVER)
	docker inspect -f \
		'{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
		$(SERVER) 2> /dev/null || echo "none"


.PHONY: stop
stop:
	docker ps -aq | xargs docker stop 2> /dev/null || echo "none"


.PHONY: start
start:
	docker ps -aq | xargs docker start 2> /dev/null || echo "none"


.PHONY: server-refresh
server-refresh:
	docker rm -f $(SERVER) 2> /dev/null || echo "none"


.PHONY: net-refresh
net-refresh:
	docker network rm $(NETWORK) 2> /dev/null || echo "none"


.PHONY: clean
clean: server-refresh net-refresh


.PHONY: rebuild
rebuild: clean run-server


.PHONY: armageddon
armageddon: clean
	docker ps -aq | xargs docker rm -f 2> /dev/null || echo "none"
	docker images -aq | xargs docker rmi -f 2> /dev/null || echo "none"
	docker system prune -af
