#!/bin/bash 
VERSION=`cd ../../arcor2;python3 setup.py --version;cd - > /dev/null`
docker image push arcor2/arcor2_upload_fit_demo:$VERSION
docker image push arcor2/arcor2_arserver_fit_demo:$VERSION

