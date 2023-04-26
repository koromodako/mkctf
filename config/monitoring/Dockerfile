FROM python:alpine

# setup packages
RUN apk update && apk upgrade && apk add git tar wget

# setup mkctf
RUN git clone https://github.com/koromodako/mkctf /mkctf && \
    python3 -m pip install /mkctf && \
    mkdir -p /mkctf.d /root/.config && \
    cp -r /mkctf/config /root/.config/mkctf && \
    rm -rf /mkctf

# set workdir
WORKDIR /mkctf.d

# add resources to container
COPY ctf/.mkctf /mkctf.d/.mkctf
COPY ctf/challenges /mkctf.d/challenges

# set entrypoint
COPY docker-entrypoint.sh /mkctf.d/docker-entrypoint.sh
RUN chmod +x /mkctf.d/docker-entrypoint.sh
ENTRYPOINT ['/mkctf.d/docker-entrypoint.sh']
