#!/usr/bin/env python3
# -!- encoding: utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    functions.py
# date:    2017-01-13
# author:  paul dautry
# purpose:
#       All functions used with dispatcher.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import os
import string
from shutil import rmtree
from subprocess import call
from core.config import Config
from core.logger import Logger
from core.utils import read_input

CHARSET = string.ascii_lowercase + string.digits + '-'
ROOT = os.getcwd()
SUBDIRS = ['chall', 'exploit', 'flags', 'src']
CONFIG = Config()
CONFIG.load()

def configure(params):
    """configure"""
    workspace = read_input('Enter workspace directory or skip (empty): ', True)
    if len(workspace) > 0:
        CONFIG.set_property(
            Config.S_DIR, Config.K_WORKSPACE, workspace)
    CONFIG.save()

def create_challenge(params):
    """create_challenge"""
    root = CONFIG.get_property(Config.S_DIR, Config.K_WORKSPACE, 'challenges')
    if not os.path.exists(root):
        Logger.inf('creating missing directory: %s' % root)
        os.makedirs(root)
    challname = read_input('enter challenge name: ')
    challname = challname.strip().lower()
    challname = challname.replace(' ', '-')
    for l in challname:
        if not l in CHARSET:
            challname = challname.replace(l, '')
    challpath = os.path.join(root, challname)
    if os.path.exists(challpath):
        Logger.err('challenge already exists!')
        return
    os.makedirs(challpath)
    for subdir in SUBDIRS:
        os.makedirs(os.path.join(root, challname, subdir))
    with open(os.path.join(root, challname, 'Makefile'), 'w') as makefile:
        makefile.write("""
#-------------------------------------------------------------------------------
#  Makefile generated using PyChallFactory :)
#-------------------------------------------------------------------------------
#===============================================================================
# variables
#===============================================================================
MKDIR=mkdir
CP=cp
ZIP=zip
MD5SUM=md5sum
RM=rm
CHALL=%s
CHALL_ZIP=$(CHALL).zip
CHALL_MD5=$(CHALL).md5
#===============================================================================
# rules
#===============================================================================
# all rule
all: build

# this rule is supposed to call dependencies and/or execute commands to prepare 
# challenge elements and put them in chall/ directory 
build:
\t# write your commands here

# this rule creates a "standard challenge package"
package:
\t$(MKDIR) $(CHALL)
\t$(CP) -r chall/* $(CHALL)/
\t$(ZIP) -r $(CHALL_ZIP) $(CHALL)/
\t$(MD5SUM) $(CHALL_ZIP) > $(CHALL_MD5)
\t$(RM) -rf $(CHALL)
""" % challname)

def delete_challenge(params):
    """delete_challenge"""
    root = CONFIG.get_property(Config.S_DIR, Config.K_WORKSPACE, 'challenges')
    resp = read_input('which challenge do you want to delete ? [<package_name>|all]\n')
    if resp == 'all':
        challs = os.listdir(root)
    else:
        challs = [ resp ]
    for chall in challs:
        challpath = os.path.join(root, chall)
        if not os.path.exists(challpath):
            Logger.err('challenge does not exists!')
            continue
        resp = read_input('do you really want to remove %s ? [yes/*]\n' % chall)
        if resp == 'yes':
            Logger.inf('removing challenge %s...' % chall)
            rmtree(challpath)
            Logger.inf('done!')

def list_challenges(params):
    """list_challenge"""
    root = CONFIG.get_property(Config.S_DIR, Config.K_WORKSPACE, 'challenges')
    print('\nChallenges:')
    for chall in os.listdir(root):
        print('\t%s' % chall)

def build_challenge(params):
    """build_challenge"""
    root = CONFIG.get_property(Config.S_DIR, Config.K_WORKSPACE, 'challenges')
    resp = read_input('which challenge do you want to build ? [<package_name>|all]\n')
    if resp == 'all':
        challs = os.listdir(root)
    else:
        challs = [ resp ]
    for chall in challs:
        challpath = os.path.join(root, chall)
        if not os.path.exists(challpath):
            Logger.err('challenge does not exists!')
            continue
        Logger.inf('building challenge %s...' % chall)
        os.chdir(challpath)
        call(['make'])
        os.chdir(ROOT)
        Logger.inf('done!')

def package_challenge(params):
    """package_challenge"""
    root = CONFIG.get_property(Config.S_DIR, Config.K_WORKSPACE, 'challenges')
    packages = CONFIG.get_property(Config.S_DIR, Config.K_PACKAGES, 'packages')
    if not os.path.exists(packages):
        Logger.inf('creating missing directory: %s' % packages)
        os.makedirs(packages)
    resp = read_input('which challenge do you want to package ? [<package_name>|all]\n')
    if resp == 'all':
        challs = os.listdir(root)
    else:
        challs = [ resp ]
    for chall in challs:
        challpath = os.path.join(root, chall)
        if not os.path.exists(challpath):
            Logger.err('challenge does not exists!')
            continue
        Logger.inf('packaging challenge %s...' % chall)
        os.chdir(challpath)
        call(['make', 'package'])
        os.chdir(ROOT)
        challbase = chall.replace('/', '')
        challzip = challbase + '.zip'
        challmd5 = challbase + '.md5'
        os.rename(os.path.join(challpath, challzip), os.path.join(packages, challzip))
        os.rename(os.path.join(challpath, challmd5), os.path.join(packages, challmd5))
        Logger.inf('done!')

def debug_on(params):
    """debug_on"""
    Logger.DEBUG = True

def verbose_on(params):
    """verbose_on"""
    Logger.VERBOSE = True

def usage(params):
    """usage"""
    prog = params['prog']
    options = params['options']
    print('\n------------------------ PyChallFactory Help ------------------------')
    print("""
python3 %s [options]

options:""" % prog)
    for opt in options:
        print('\t%s, %s: %s' % (opt[0], opt[1], opt[2]))
    print('\n---------------------------------------------------------------------')