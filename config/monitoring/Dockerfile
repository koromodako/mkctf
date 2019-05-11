FROM ubuntu:19.04
##
## Install monitoring script dependencies
##
RUN apt update && apt upgrade -y
RUN DEBIAN_FRONTEND=noninteractive apt install -y \
    git tar wget \
    python3 python3-dev python3-pip
##
## Prepare directories
##
RUN mkdir -p /mkctf-mon && mkdir -p /root/.config/mkctf/
##
## Install mkCTF
##
RUN git clone https://github.com/koromodako/mkctf /mkctf && \
    pip3 install /mkctf && \
    cp -r /mkctf/config/* /root/.config/mkctf/
##
## Set working directory
##
WORKDIR /mkctf-mon
##
## Add resources to container
##
ADD ./.mkctf /mkctf-mon/.mkctf
ADD ./challenges /mkctf-mon/challenges
ADD ./monitoring/mkctf.env /mkctf-mon/run-mkctf-mon.sh
##
## Prepare monitoring script
##
RUN echo 'mkctf-monitor --task-timeout 600 --iter-delay 600' >> /mkctf-mon/run-mkctf-mon.sh
##
## Start monitoring script
##
CMD bash /mkctf-mon/run-mkctf-mon.sh
