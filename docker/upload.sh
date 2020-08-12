#!/bin/bash 
VERSION=`python3 ../setup.py --version`
docker image push arcor2/arcor2_upload_fit_demo:$VERSION
docker image push arcor2/arcor2_arserver_fit_demo:$VERSION
docker image push arcor2/arcor2_execution_fit_demo:$VERSION

