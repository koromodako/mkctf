#!/usr/bin/env bash

BIN_DIR="${HOME}/.local/bin"
LIB_DIR="${HOME}/.local/lib"
CNF_DIR="${HOME}/.config/mkctf"
VNV_DIR="${LIB_DIR}/mkctf-venv"
TMP_DIR="$(mktemp -d --suffix=.mkctf)"
GIT_URL="https://github.com/koromodako/mkctf"

function print {
    echo "[setup.sh]: ${1}"
}

print "ensure directory exists"
mkdir -p "${BIN_DIR}" \
         "${LIB_DIR}" \
         "${CNF_DIR}"

print "fetch mkctf repository"
git clone "${GIT_URL}" "${TMP_DIR}"

print "reset mkctf configuration"
rm -rf "${CNF_DIR}"/*
cp -r "${TMP_DIR}"/config/* "${CNF_DIR}/"

print "reset python virtual environment"
rm -rf "${VNV_DIR}"
python3 -m venv "${VNV_DIR}"

print "install mkctf package"
"${VNV_DIR}"/bin/python -m pip install "${TMP_DIR}"

print "create symbolic links"
ln -sf "${VNV_DIR}"/bin/mkctf-* "${BIN_DIR}"/

print "cleanup mkctf repository"
rm -rf "${TMP_DIR}"

print "please ensure that ${BIN_DIR} is part of your PATH"
print "then try invoking mkctf-cli running command: "
print "$ mkctf-cli -h"
