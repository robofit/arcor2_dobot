#!/bin/bash 
VERSION=`cd ../../arcor2;python3 setup.py --version;cd - > /dev/null`
docker build --no-cache -f Dockerfile -t arcor2/arcor2_upload_fit_demo:$VERSION  ../ --build-arg version=$VERSION
docker build --no-cache -f Dockerfile-arserver -t arcor2/arcor2_arserver_fit_demo:$VERSION  ../ --build-arg version=$VERSION
