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
from core.command.init import init
from core.command.show import show
from core.command.create import create
from core.command.delete import delete
from core.command.configure import configure
from core.object.repository import Repository
# =============================================================================
#  FUNCTIONS
# =============================================================================
##
## @brief      SIGINT handler
##
## @param      args  The arguments
##
def sigint_handler(*args):
    exit(1)
##
## @brief      { function_description }
##
def resolve_script_dir(logger, fpath):
    while path.islink(fpath):
        fpath = os.readlink(fpath)

        if fpath.startswith('..'):
            logger.fatal("relative path is impossible to resolve properly...")

    return path.dirname(fpath)
##
## @brief      Parses commandline arguments
##
def parse_args():
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
    # -- init
    init_parser = subparsers.add_parser('init',
                                        help="initializes mkctf repository.")
    init_parser.set_defaults(func=init)
    # -- show
    show_parser = subparsers.add_parser('show',
                                        help="shows challenges.")
    show_parser.add_argument('--category',
                             help="challenge's category.")
    show_parser.add_argument('-c', '--chall-slug',
                             help="challenge's slug.")
    show_parser.set_defaults(func=show)
    # -- create
    create_parser = subparsers.add_parser('create',
                                          help="creates a challenge.")
    create_parser.set_defaults(func=create)
    # -- delete
    delete_parser = subparsers.add_parser('delete',
                                          help="deletes a challenge.")
    delete_parser.add_argument('category', help="challenge's category.")
    delete_parser.add_argument('chall_slug', help="challenge's slug.")
    delete_parser.set_defaults(func=delete)
    # -- configure
    configure_parser = subparsers.add_parser('configure',
                                             help="edits repository's config "
                                                  "or challenge's config.")
    configure_parser.add_argument('--category',
                                  help="challenge's category.")
    configure_parser.add_argument('-c', '--chall-slug',
                                  help="challenge's slug.")
    configure_parser.set_defaults(func=configure)

    return parser.parse_args()
##
## @brief      Entry point
##
def main():
    signal.signal(signal.SIGINT, sigint_handler)

    args = parse_args()

    logger = Logger(args.debug, args.quiet, args.no_color)
    logger.info("mkctf starts.")
    logger.debug(args)

    args.glob_conf_path = path.join(resolve_script_dir(logger, __file__),
                                    '.mkctf.glob.yml')

    glob_conf = load_config(args)
    repo_conf_path = path.join(args.working_dir,
                               glob_conf['files']['config']['repository'])

    logger.debug(glob_conf)
    repo = Repository(logger, repo_conf_path, glob_conf)

    if args.command != 'init' and repo.get_conf() is None:
        logger.fatal("mkctf repository must be initialized first. Run "
                     "`mkctf init`.")

    try:
        success = args.func(args, repo, logger)
    except Exception as e:
        code = 42
        traceback.print_exc()
        logger.fatal("Ouuuuupss.....:(")

    if success:
        logger.info("mkctf ended successfully.")
    else:
        logger.error("mkctf ended with errors.")

    exit(0 if success else 1)
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    main()
