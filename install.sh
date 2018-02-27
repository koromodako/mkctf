#!/usr/bin/env bash
# -!- encoding:utf8 -!-

function check_cmd {
    if ! [ -x "$(command -v ${1})" ]; then
        echo '[install.sh]> install ${1} and try again.' >&2
        exit 1
    fi
}

check_cmd git
check_cmd pip3

mkdir -p ~/bin

cd ~/bin

git clone https://github.com/pdautry/mkctf

pip3 install -r mkctf/requirements.txt

ln -s mkctf/mkctf.py mkctf

cd ~/
