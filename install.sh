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
check_cmd pip3
check_cmd python3

if [[ -d "${REPO_DIR}" ]]; then
    print "pulling repository"
    cd ${REPO_DIR}
    git pull
else
    print "cloning repository"
    cd /tmp
    git clone https://github.com/pdautry/mkctf
fi

print "entering ${REPO_DIR}"
cd ${REPO_DIR}

print "installing Python requirements"
pip3 install -r requirements.txt

print "running setup.py"
python3 setup.py install --prefix ${INST_DIR}

print "going back to ${WD}"
cd ${WD}
