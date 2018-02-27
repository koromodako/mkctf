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
from core.config import load_config
from core.command.init import init
from core.command.show import show
from core.command.create import create
from core.command.update import update
from core.command.delete import delete
from core.command.configure import configure
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      SIGINT handler
##
## @param      args  The arguments
##
def sigint_handler(*args):
    print()
    exit(0)
##
## @brief      Entry point
##
def main():
    signal.signal(signal.SIGINT, sigint_handler)

    parser = argparse.ArgumentParser(add_help=True,
        description="Manage CTF challenges repository.")

    parser.add_argument('-v', '--verbose', action='store_true',
                        help="increase program verbosity")
    parser.add_argument('-d', '--debug', action='store_true',
                        help="output debug messages")
    parser.add_argument('-w', '--working-dir', default=os.getcwd(),
                        help="")

    subparsers = parser.add_subparsers(dest='command', metavar='COMMAND')
    subparsers.required = True

    init_parser = subparsers.add_parser('init', help="")
    init_parser.set_defaults(func=init)

    show_parser = subparsers.add_parser('show', help="")
    show_parser.add_argument('-g', '--category', help="")
    show_parser.add_argument('-c', '--challenge', help="")
    show_parser.set_defaults(func=show)

    create_parser = subparsers.add_parser('create', help="")
    create_parser.set_defaults(func=create)

    update_parser = subparsers.add_parser('update', help="")
    update_parser.add_argument('-c', '--challenge', help="")
    update_parser.set_defaults(func=update)

    delete_parser = subparsers.add_parser('delete', help="")
    delete_parser.add_argument('-c', '--challenge', help="")
    delete_parser.set_defaults(func=delete)

    configure_parser = subparsers.add_parser('configure', help="")
    configure_parser.set_defaults(func=configure)

    args = parser.parse_args()

    args.glob_conf_path = os.path.join(os.path.dirname(__file__), '.mkctf.yml')

    logger = Logger(args.debug, args.verbose)

    config = load_config(args, logger)

    try:
        code = 0 if args.func(args, config, logger) else 1
        print('\nSee you soon! :)\n')
    except Exception as e:
        code = 42
        print('\nOuuuuupss.....:(\n')
        (type, value, traceback) = sys.exc_info()
        traceback.print_stack()

    exit(code)
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    main()
