#!/usr/bin/env bash

function print {
    echo "[setup.sh]: ${1}"
}

print "clone mkctf repository in tmp directory"
git clone https://github.com/koromodako/mkctf /tmp/mkctf
print "create ~/bin dir if required and enter ~/bin"
mkdir -p ~/bin && cd ~/bin
print "create a Python 3 virtual environment"
python3 -m venv .mkctf-venv
print "install mkctf in the venv"
.mkctf-venv/bin/pip install /tmp/mkctf
print "create symbolic links for mkctf scripts"
ln -s ./mkctf-venv/bin/mkctf-* .
print "leave ~/bin"
cd ..
print "ensure that config directory exists and copy configuration files in it"
mkdir -p ~/.config && cp -r /tmp/mkctf/config ~/.config/mkctf
print "ensure that ~/bin is part of your path and try invoking mkctf-cli running command: mkctf-cli -h"

