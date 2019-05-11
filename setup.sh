#!/usr/bin/env bash

BIN_DIR=~/bin
VENV_DIR=.mkctf-venv
LOCAL_REPO=/tmp/mkctf
# everything above this line can be modified -------------------------
# everything below this line shall not be modified -------------------
CWD=$(pwd)
CONFIG_DIR=~/.config/mkctf

function print {
    echo "[setup.sh]: ${1}"
}

# -- fetching mkCTF sources
if [ -d ${LOCAL_REPO} ]; then
    print "pulling latest changes of mkCTF repository in ${LOCAL_REPO}"
    cd ${LOCAL_REPO}
    git pull
    cd ${CWD}
else
    print "cloning mkCTF repository in ${LOCAL_REPO}"
    git clone https://github.com/koromodako/mkctf ${LOCAL_REPO}
fi
# -- installing mkctf and its dependencies
if [ ! -d ${BIN_DIR} ]; then
    print "creating ${BIN_DIR} dir"
    mkdir -p ${BIN_DIR}
fi
print "entering ${BIN_DIR}"
cd ${BIN_DIR}
if [ ! -d ${VENV_DIR} ]; then
    print "creating a Python 3 virtual environment"
    python3 -m venv ${VENV_DIR}
fi
print "installing/updating mkCTF in the venv"
${VENV_DIR}/bin/pip install -U ${LOCAL_REPO}
print "creating/updating symbolic links for mkctf scripts"
ln -sf ./mkctf-venv/bin/mkctf-* .
print "leaving ${BIN_DIR}"
cd ${CWD}
# -- installing mkctf configuration
print "creating config directory"
mkdir -p ${CONFIG_DIR}
print "copying configuration files in ${CONFIG_DIR}"
cp -r ${LOCAL_REPO}/config/* ${CONFIG_DIR}
print "setup completed!"
# -- print manual instructions
print "please ensure that ${BIN_DIR} is part of your PATH"
print "then try invoking mkctf-cli running command: "
print "$ mkctf-cli -h"
