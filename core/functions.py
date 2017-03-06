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
import stat
import string
from shutil import rmtree
from subprocess import call
from core.config import Config
from core.logger import Logger
from core.utils import read_input
from core.utils import select_category

CHARSET = string.ascii_lowercase + string.digits + '-'
ROOT = os.getcwd()
CATEGORIES = [
    'bugbounty',
    'crypto',
    'forensics',
    'misc',
    'programming',
    'pwn',
    'reverse',
    'web'
]
SUBDIRS = [
    'server-files',
    'public-files',
    'exploit',
    'src'
]
SUBFILES = [
#   (filename, executable?)
    ('writeup.md', False),
    ('flag.txt', False),
    ('public-files/description.md', False),
    ('exploit/exploit.py', True)
]
CONFIG = Config()
CONFIG.load()

def configure(params):
    """configure"""
    workspace = read_input('Enter workspace directory or skip (empty): ', True)
    if len(workspace) > 0:
        CONFIG.set_property(
            Config.S_DIR, Config.K_WORKSPACE, workspace)
    CONFIG.save()

def make_fs_tree(root):
    if not os.path.exists(root):
        Logger.inf('creating missing directory: %s' % root)
        os.makedirs(root)
    for category in CATEGORIES:
        if not os.path.exists(os.path.join(root, category)):
            Logger.inf('creating missing directory: %s' % root)
            os.makedirs(os.path.join(root, category))

def create_challenge(params):
    """create_challenge"""
    root = CONFIG.get_property(Config.S_DIR, Config.K_WORKSPACE, 'challenges')
    make_fs_tree(root)
    chall_name = read_input('enter challenge name: ')
    chall_name = chall_name.strip().lower()
    chall_name = chall_name.replace(' ', '-')
    for l in chall_name:
        if not l in CHARSET:
            chall_name = chall_name.replace(l, '')
    chall_category = select_category(CATEGORIES)
    chall_path = os.path.join(root, chall_category, chall_name)
    if os.path.exists(chall_path):
        Logger.err('challenge already exists!')
        return
    os.makedirs(chall_path)
    for subdir in SUBDIRS:
        os.makedirs(os.path.join(chall_path, subdir))
    for subfile, executable in SUBFILES:
        file_path = os.path.join(chall_path, subfile)
        with open(file_path, 'w') as sf:
            sf.write('\n')
        if executable:
            os.chmod(file_path, stat.S_IRWXU|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)

def delete_chall(root, category, target):
    if target == 'all':
        challs = os.listdir(os.path.join(root, category))
    else:
        challs = [ target ]
    for chall_name in challs:
        chall_path = os.path.join(root, category, chall_name)
        if not os.path.exists(chall_path):
            Logger.err('challenge does not exists!')
            continue
        resp = read_input('do you really want to remove %s ? [yes/*]\n' % chall_name)
        if resp == 'yes':
            Logger.inf('removing challenge %s...' % chall_name)
            rmtree(chall_path)
            Logger.inf('done!')

def delete_challenge(params):
    """delete_challenge"""
    root = CONFIG.get_property(Config.S_DIR, Config.K_WORKSPACE, 'challenges')
    target = read_input('which challenge do you want to delete ? [<package_name>|all]\n')
    category = select_category(CATEGORIES + ['all'])
    if category == 'all':
        for c in CATEGORIES:
            delete_chall(root, c, target)
    else:
        delete_chall(root, category, target)

def list_challenges(params):
    """list_challenge"""
    root = CONFIG.get_property(Config.S_DIR, Config.K_WORKSPACE, 'challenges')
    print('\nChallenges:')
    for category in CATEGORIES:
        print('\t%s:' % category)
        for chall in os.listdir(os.path.join(root, category)):
            if chall[0] != '.':
                print('\t\t%s' % chall)

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
