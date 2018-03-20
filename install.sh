#!/usr/bin/env bash
# -!- encoding:utf8 -!-

WD=$(pwd)
BIN_DIR=~/bin
CONF_DIR=~/.config
REPO_DIR=${BIN_DIR}/mkctf

function print {
    echo "[install.sh]> ${1}"
}

function check_cmd {
    if ! [ -x "$(command -v ${1})" ]; then
        print "install ${1} and try again."
        exit 1
    fi
}

print "check for mandatory commands"
check_cmd git
check_cmd pip3

print "creating ${BIN_DIR} if inexistant"
mkdir -p ${BIN_DIR}

print "entering ${BIN_DIR}"
cd ${BIN_DIR}

if [[ -d "${REPO_DIR}" ]]; then
    print "pulling repository"
    cd ${REPO_DIR}
    git pull
    cd ${BIN_DIR}
else
    print "cloning repository"
    git clone https://github.com/pdautry/mkctf
fi

print "installing Python requirements"
pip3 install -r ${REPO_DIR}/requirements.txt

print "creating symlink"
ln -s ${REPO_DIR}/mkctf.py ${BIN_DIR}/mkctf-cli

print "creating configuration"
mkdir -p ${CONF_DIR}
cp ${REPO_DIR}/mkctf.yml.dist ${CONF_DIR}/mkctf.yml

print "going back to ${WD}"
cd ${WD}
