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
from core.command.enable import enable
from core.command.export import export
from core.command.disable import disable
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
    print("\nOuch... that's harsh you know... :/")
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
    main_p = argparse.ArgumentParser(add_help=True,
        description="Manage CTF challenges repository.")
    main_p.add_argument('-q', '--quiet', action='store_true',
                        help="decrease program verbosity")
    main_p.add_argument('-d', '--debug', action='store_true',
                        help="output debug messages")
    main_p.add_argument('--no-color', action='store_true',
                        help="disable colored output")
    main_p.add_argument('-w', '--working-dir', default=os.getcwd(),
                        help="")
    # -- add subparsers
    sps = main_p.add_subparsers(dest='command', metavar='COMMAND')
    sps.required = True
    # ---- init
    init_p = sps.add_parser('init', help="initializes mkctf repository.")
    init_p.set_defaults(func=init)
    # ---- show
    show_p = sps.add_parser('show', help="shows challenges.")
    show_p.add_argument('--category', help="challenge's category.")
    show_p.add_argument('-c', '--chall-slug', help="challenge's slug.")
    show_p.set_defaults(func=show)
    # ---- create
    create_p = sps.add_parser('create', help="creates a challenge.")
    create_p.set_defaults(func=create)
    # ---- delete
    delete_p = sps.add_parser('delete', help="deletes a challenge.")
    delete_p.add_argument('category', help="challenge's category.")
    delete_p.add_argument('chall_slug', help="challenge's slug.")
    delete_p.set_defaults(func=delete)
    # ---- configure
    configure_p = sps.add_parser('configure', help="edits repository's config "
                                                   "or challenge's config.")
    configure_p.add_argument('--category', help="challenge's category.")
    configure_p.add_argument('-c', '--chall-slug', help="challenge's slug.")
    configure_p.set_defaults(func=configure)
    # ---- enable
    enable_p = sps.add_parser('enable', help="enables a challenge.")
    enable_p.add_argument('category', help="challenge's category.")
    enable_p.add_argument('chall_slug', help="challenge's slug.")
    enable_p.set_defaults(func=enable)
    # ---- disable
    disable_p = sps.add_parser('disable', help="disables a challenge.")
    disable_p.add_argument('category', help="challenge's category.")
    disable_p.add_argument('chall_slug', help="challenge's slug.")
    disable_p.set_defaults(func=disable)
    # ---- export
    export_p = sps.add_parser('export', help="exports enabled static "
                                             "challenges.")
    export_p.add_argument('export_dir', help="folder where archives must be "
                                             "written. If the folder does not "
                                             "exist it will be created.")
    export_p.add_argument('--category', help="challenge's category.")
    export_p.add_argument('-c', '--chall-slug', help="challenge's slug.")
    export_p.add_argument('--include-disabled', action='store_true',
                          help="export disabled challenges too.")
    export_p.set_defaults(func=export)

    return main_p.parse_args()
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
