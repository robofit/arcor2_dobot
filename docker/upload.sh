#!/bin/bash 
docker image push arcor2/arcor2_base_fit_demo:`cat ./VERSION`
docker image push arcor2/arcor2_arserver_fit_demo:`cat ./VERSION`

