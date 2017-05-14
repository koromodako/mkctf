#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# file:    py_chall_factory.py
# date:    2017-01-13
# author:  paul dautry
# purpose:
#       This is a framework designed to create challenges and maintain them.
#       Entry point script.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#===============================================================================
#  IMPORTS
#===============================================================================
import os
import sys
import signal
import argparse
from core.logger import Logger
from core.functions import configure
from core.functions import create_challenge
from core.functions import delete_challenge
from core.functions import list_challenges
#===============================================================================
#  FUNCTIONS/CLASSES
#===============================================================================
def sigint_handler(*args):
    print()
    exit(0)

#===============================================================================
#  MAIN SCRIPT
#===============================================================================

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint_handler)
    parser = argparse.ArgumentParser(add_help=True,
        description='A CTF tool for managing challenges.')
    # output specific arguments
    parser.add_argument('-v', '--verbose', action='store_true', help='increase program verbosity')
    parser.add_argument('-d', '--debug', action='store_true', help='output debug messages')
    parser.add_argument('action', metavar='action', choices=['configure', 'create', 'delete', 'list'],
        help='{configure, create, delete, list}')
    args = parser.parse_args()
    # process cmdline options
    Logger.DEBUG = args.debug
    Logger.VERBOSE = args.verbose
    # 
    if args.action == 'configure':
        configure()
    elif args.action == 'create':
        create_challenge()
    elif args.action == 'delete':
        delete_challenge()
    elif args.action == 'list':
        list_challenges()
    print('\nSee you soon! :)\n')
    exit(0)