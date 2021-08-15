docker build -t pythondev .
docker container run -it -v /<WorkDir>:/workdir --name <ContainerName> pythondev /bin/bash