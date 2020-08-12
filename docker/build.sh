#!/bin/bash 
VERSION_BASE=`cd ../../arcor2;python3 setup.py --version;cd - > /dev/null`
VERSION=`python3 ../setup.py --version`
docker build --no-cache -f Dockerfile -t arcor2/arcor2_upload_fit_demo:$VERSION  ../ --build-arg version=$VERSION_BASE
docker build --no-cache -f Dockerfile-arserver -t arcor2/arcor2_arserver_fit_demo:$VERSION  ../ --build-arg version=$VERSION_BASE
docker build --no-cache -f Dockerfile-execution -t arcor2/arcor2_execution_fit_demo:$VERSION  ../ --build-arg version=$VERSION_BASE

