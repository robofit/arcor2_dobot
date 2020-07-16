#!/bin/bash 
docker build --no-cache -f Dockerfile -t arcor2/arcor2_base_fit_demo:`cat ./VERSION`  ../ --build-arg version=`cat ./VERSION`
docker build --no-cache -f Dockerfile-arserver -t arcor2/arcor2_arserver_fit_demo:`cat ./VERSION`  ../ --build-arg version=`cat ./VERSION`
