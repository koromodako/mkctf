# retrieve base image
FROM image
# upgrade system
RUN apt-get update && apt-get upgrade -y
# install dependencies
RUN apt-get install -y
# create a server dir and use it as working directory
RUN mkdir -p /srv
WORKDIR /srv
# add some files
ADD server-files/file.1 /srv
# start the server
CMD start server command
