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
from core.utils import read_input_loop
from core.utils import select_category

CHARSET = string.ascii_lowercase + string.digits + '-'
ROOT = os.getcwd()
CONFIG_FILE = 'py_chall_factory.pref'
CONFIG = Config()
CONFIG.load(CONFIG_FILE)
# override defaults if a valid configuration is found
CATEGORIES = CONFIG.get_property(Config.K_CATEGORIES, default=[])
DIRECTORIES = CONFIG.get_property(Config.K_DIRECTORIES, default=[])
FILES = CONFIG.get_property(Config.K_FILES, default=[])
#

def configure():
    """configure"""
    global CONFIG
    CONFIG = Config()
    workspace = read_input('Enter workspace directory: ', False)
    categories = read_input_loop('Enter categories (finish with [dot]) or use default (empty):', 
        'Enter next category: ')
    directories = read_input_loop('Enter directories (finish with [dot]) or use default (empty):',
        'Enter next directory: ')
    files = read_input_loop('Enter files (finish with [dot]) or  use default (empty):',
        'Enter next file: ')
    if len(workspace) > 0:
        CONFIG.set_property(Config.K_WORKSPACE, workspace)
    if len(categories) > 0:
        CONFIG.set_property(Config.K_CATEGORIES, categories)
    if len(directories) > 0:
        CONFIG.set_property(Config.K_DIRECTORIES, directories)
    if len(files) > 0:
        files_tuples = []
        for f in files:
            resp = read_input('Should <%s> be an executable ? [yes/*]: ' % f)
            files_tuples.append([f, resp == 'yes'])
        CONFIG.set_property(Config.FILES, files_tuples)
    CONFIG.save(CONFIG_FILE)
    Logger.inf('configuration file saved.')

def __make_fs_tree(root):
    if not os.path.exists(root):
        Logger.inf('creating missing directory: %s' % root)
        os.makedirs(root)
    for category in CATEGORIES:
        if not os.path.exists(os.path.join(root, category)):
            Logger.inf('creating missing directory: %s' % root)
            os.makedirs(os.path.join(root, category))

def create_challenge():
    """create_challenge"""
    root = CONFIG.get_property(Config.K_WORKSPACE, 'challenges')
    __make_fs_tree(root)
    chall_name = read_input('enter challenge name: ')
    chall_name = chall_name.strip().lower()
    chall_name = chall_name.replace(' ', '-')
    for l in chall_name:
        if not l in CHARSET:
            chall_name = chall_name.replace(l, '')
    chall_points = read_input('enter challenge points: ', expect_digit=True)
    chall_category = select_category(CATEGORIES)
    chall_path = os.path.join(root, chall_category, chall_name + "-" + str(chall_points))
    if os.path.exists(chall_path):
        Logger.err('challenge already exists!')
        return
    os.makedirs(chall_path)
    for subdir in DIRECTORIES:
        os.makedirs(os.path.join(chall_path, subdir))
    for subfile, executable in FILES:
        file_path = os.path.join(chall_path, subfile)
        with open(file_path, 'w') as sf:
            sf.write('\n')
        if executable:
            os.chmod(file_path, stat.S_IRWXU|stat.S_IRGRP|stat.S_IXGRP|stat.S_IROTH|stat.S_IXOTH)

def __confirm_rmtree(path):
    if os.path.exists(path):
        resp = read_input('do you really want to remove <%s> ? [yes/*]\n' % path)
        if resp == 'yes':
            Logger.inf('removing challenge <%s> ...' % path)
            rmtree(path)
            Logger.inf('done!')
            return True
    else:
        Logger.wrn('could not find <%s> ...' % path)
    return False

def __delete_all_challs_in(root, category):
    path = os.path.join(root, category)
    if __confirm_rmtree(path):
        os.makedirs(path)

def __delete_challs(root, category, target):
    if category == 'all':
        if target == 'all':
            for c in CATEGORIES: 
                __delete_all_challs_in(c)
        else:
            for c in CATEGORIES:
                path = os.path.join(root, category, target)
                __confirm_rmtree(path)
    else:
        if target == 'all':
            __delete_all_challs_in(category)
        else:
            path = os.path.join(root, category, target)
            __confirm_rmtree(path)

def delete_challenge():
    """delete_challenge"""
    root = CONFIG.get_property(Config.K_WORKSPACE, 'challenges')
    print('[?] > first, select the category where the challenge you want to delete is.')
    category = select_category(CATEGORIES + ['all (search in all categories)'])
    if category == 'all (delete all challenges)':
        category = 'all'
        list_challenges()
    else:
        list_challenges(category)
    target = read_input('now, what is the name of the challenge you want to delete? [<package_name>|all]: ')
    __delete_challs(root, category, target)

def list_challenges(category=None):
    """list_challenge"""
    root = CONFIG.get_property(Config.K_WORKSPACE, 'challenges')
    if category is None:
        category = select_category(CATEGORIES + ['all (delete all challenges)'])
    if category == 'all (delete all challenges)':
        categories_to_print = CATEGORIES
    else:
        categories_to_print = [category]
    print('\nChallenges:')
    for category in categories_to_print:
        print('\t%s:' % category)
        path = os.path.join(root, category)
        if os.path.isdir(path):
            challs = []
            for entry in os.listdir(path):
                if os.path.isdir(os.path.join(path, entry)):
                    challs.append(entry)    
            for c in challs:
                if c[0] != '.':
                    print('\t\t%s' % c)
            if len(challs) == 0:
                print('\t\t> no challenge in this directory.')
        else:
            print('\t\tmissing directory.')
