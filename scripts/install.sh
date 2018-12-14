#!/usr/bin/env bash
# -!- encoding:utf8 -!-

WD=$(pwd)
INST_DIR=~/.local
REPO_DIR=/tmp/mkctf

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
check_cmd python3

if [[ -d "${REPO_DIR}" ]]; then
    print "pulling repository"
    cd ${REPO_DIR}
    git pull
else
    print "cloning repository"
    cd /tmp
    git clone https://github.com/koromodako/mkctf
fi

print "entering ${REPO_DIR}"
cd ${REPO_DIR}

print "creating venv"
python3 -m venv .venv

print "installing Python requirements"
.venv/bin/pip install .

print "going back to ${WD}"
cd ${WD}
