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
import signal
import argparse
import traceback
import os.path as path
from core.logger import Logger
from core.config import load_config
from core.repository import Repository
from core.command.init import init
from core.command.show import show
from core.command.create import create
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
## @brief      { function_description }
##
def resolve_script_dir(fpath):
    while path.islink(fpath):
        fpath = os.readlink(fpath)
        if fpath.startswith('..'):
            print('script path impossible to resolve...')
            exit(2)
    return path.dirname(fpath)
##
## @brief      Entry point
##
def main():
    signal.signal(signal.SIGINT, sigint_handler)

    parser = argparse.ArgumentParser(add_help=True,
        description="Manage CTF challenges repository.")

    parser.add_argument('-q', '--quiet', action='store_true',
                        help="decrease program verbosity")
    parser.add_argument('-d', '--debug', action='store_true',
                        help="output debug messages")
    parser.add_argument('--no-color', action='store_true',
                        help="disable colored output")
    parser.add_argument('-w', '--working-dir', default=os.getcwd(),
                        help="")

    subparsers = parser.add_subparsers(dest='command', metavar='COMMAND')
    subparsers.required = True

    init_parser = subparsers.add_parser('init',
                                        help="Initialize mkctf repository.")
    init_parser.set_defaults(func=init)

    show_parser = subparsers.add_parser('show',
                                        help="show one or many challenges.")
    show_parser.add_argument('-c', '--challenge',
                             help="challenge name.")
    show_parser.set_defaults(func=show)

    create_parser = subparsers.add_parser('create',
                                          help="create a challenge.")
    create_parser.set_defaults(func=create)

    delete_parser = subparsers.add_parser('delete',
                                          help="delete a challenge.")
    delete_parser.add_argument('challenge', help="challenge name.")
    delete_parser.set_defaults(func=delete)

    configure_parser = subparsers.add_parser('configure',
                                             help="edit ctf or challenge "
                                                  "configuration.")
    configure_parser.add_argument('-c', '--challenge',
                                  help="challenge name.")
    configure_parser.set_defaults(func=configure)

    args = parser.parse_args()


    args.glob_conf_path = path.join(resolve_script_dir(__file__), '.mkctf.glob.yml')

    logger = Logger(args.debug, args.quiet, args.no_color)

    glob_conf = load_config(args)

    logger.debug(glob_conf)
    repo = Repository(args, logger, glob_conf)

    try:
        code = 0 if args.func(args, repo, logger) else 1
    except Exception as e:
        code = 42
        traceback.print_exc()
        logger.fatal('Ouuuuupss.....:(')

    exit(code)
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    main()
