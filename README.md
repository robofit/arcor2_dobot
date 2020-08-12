# arcor2_fit_demo

### Run system 

For this demo, ARServer and Execution services from acror2_fit_demo package has to be used, while Build service could be from basic arcor2 package (as it is specified in docker/docker-compose.yml file). Proper version of all services has to be set using environment variables. 

#### Windows

It is recommended to use explicit stable version of each image instead of latest (as latest is considered unstable).

```bash
cd docker
$env:ARCOR2_VERSION="latest"
$env:ARCOR2_BUILD_VERSION="latest"
$env:ARCOR2_EXECUTION_VERSION="latest"
docker-compose up
```

For persistent variables, use this:

```bash
[Environment]::SetEnvironmentVariable("ARCOR2_VERSION", "latest", "User")
[Environment]::SetEnvironmentVariable("ARCOR2_BUILD_VERSION", "latest", "User")
[Environment]::SetEnvironmentVariable("ARCOR2_EXECUTION_VERSION", "latest", "User")
```
Restart powershell or open new window.
```
cd docker
docker-compose up
```


#### Linux

It is recommended to use explicit stable version of each image instead of latest (as latest is considered unstable).

```bash
cd docker
export ARCOR2_VERSION=latest
export ARCOR2_BUILD_VERSION=latest
export ARCOR2_EXECUTION_VERSION=latest
sudo -E docker-compose up
```

## Uploading builtin object_types to project service
Use docker exec to attach to arserver container and run following scripts and restart arserver.
```bash
arcor2_upload_builtin_objects
```

## Uploading dobot object_type
Use prepared arcor2_upload_fit_demo docker image
```bash
sudo docker run --network="docker_fitnet" --env ARCOR2_PERSISTENT_STORAGE_URL=http://mocks:5012 arcor2/arcor2_upload_fit_demo:VERSION
```
Replace VERSION with currnet version of arcor2_fit_demo package
