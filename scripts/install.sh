#!/usr/bin/env bash
# -!- encoding:utf8 -!-

CWD=$(pwd)
INST_DIR=~/bin
REPO_DIR=/tmp/mkctf
VENV_DIR=${INST_DIR}/.mkctf-venv

function print {
    echo "[install.sh]> ${1}"
}

function check_cmd {
    print "checking for ${1}"
    if ! [ -x "$(command -v ${1})" ]; then
        print "install ${1} and try again."
        exit 1
    else
        print "ok"
    fi
}

check_cmd git
check_cmd python3

if [[ -d "${REPO_DIR}" ]]; then
    print "pulling repository..."
    cd ${REPO_DIR}
    git pull
    cd ${CWD}
else
    print "cloning repository..."
    git clone https://github.com/koromodako/mkctf ${REPO_DIR}
fi

print "creating venv..."
python3 -m venv ${VENV_DIR}
print "installing/upgrading..."
${VENV_DIR}/bin/pip install -U ${REPO_DIR}
ln -s ${VENV_DIR}/bin/mkctf-cli ${INST_DIR}
ln -s ${VENV_DIR}/bin/mkctf-serve ${INST_DIR}
