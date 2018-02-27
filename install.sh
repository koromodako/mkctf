#!/usr/bin/env bash
# -!- encoding:utf8 -!-

function print {
    echo '[install.sh]> ${1}'
}

function check_cmd {
    if ! [ -x "$(command -v ${1})" ]; then
        print 'install ${1} and try again.'
        exit 1
    fi
}

print 'check for mandatory commands'
check_cmd git
check_cmd pip3
print 'creating ~/bin if inexistant'
mkdir -p ~/bin
print 'entering ~/bin'
cd ~/bin
print 'cloning repository'
git clone https://github.com/pdautry/mkctf
print 'installing Python requirements'
pip3 install -r mkctf/requirements.txt
print 'creating symlink'
ln -s mkctf/mkctf.py ~/bin/mkctf
print 'exiting ~/bin'
cd ~/
