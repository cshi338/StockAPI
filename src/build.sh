#!/bin/bash
docker build -t catalog -f DockerFile-catalog .
docker build -t order -f DockerFile-order .
docker build -t frontend -f DockerFile-frontend .
docker network create --driver=bridge --subnet=10.0.0.0/24 stockNet
docker run --name=catalog --net=stockNet --ip=10.0.0.242 -p 56892:56892 -v $PWD/catalog-service:/app/catalog-service -d catalog
docker run --name=order --net=stockNet --ip=10.0.0.241 -p 56891:56891 -v $PWD/order-service:/app/order-service -e CATALOG_HOST=10.0.0.242 -d order
docker run --name=frontend --net=stockNet --ip=10.0.0.243 -p 56893:56893 -e CATALOG_HOST=10.0.0.242 -e ORDER_HOST=10.0.0.241 -d frontend
