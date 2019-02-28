#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#===============================================================================
#  IMPORTS
#===============================================================================
from signal import SIGINT, SIGTERM
from asyncio import get_event_loop
from pathlib import Path
from argparse import ArgumentParser
from mkctf import __banner__
from mkctf.api import MKCTFAPI
from mkctf.cli import (
    setup_init,
    setup_enum,
    setup_build,
    setup_create,
    setup_delete,
    setup_enable,
    setup_export,
    setup_deploy,
    setup_status,
    setup_disable,
    setup_configure,
    setup_renew_flag
)
from mkctf.helper.log import app_log, log_enable_debug
from mkctf.helper.formatting import format_enable_colors
# =============================================================================
#  FUNCTIONS
# =============================================================================
def parse_args():
    '''Parse command line arguments
    '''
    parser = ArgumentParser(add_help=True,
                       description="Manage CTF challenges repository.")
    parser.add_argument('--yes', '-y', action='store_true', help="do not ask for confirmation.")
    parser.add_argument('--debug', '-d', action='store_true', help="output debug messages")
    parser.add_argument('--repo-root', '-r', type=Path, default=Path.cwd(), help="repository's root folder absolute path.")
    parser.add_argument('--no-color', action='store_true', help="disable colored output")
    # -- add subparsers
    subparsers = parser.add_subparsers(dest='command', metavar='COMMAND')
    subparsers.required = True
    setup_init(subparsers)
    setup_enum(subparsers)
    setup_build(subparsers)
    setup_create(subparsers)
    setup_delete(subparsers)
    setup_enable(subparsers)
    setup_export(subparsers)
    setup_deploy(subparsers)
    setup_status(subparsers)
    setup_disable(subparsers)
    setup_configure(subparsers)
    setup_renew_flag(subparsers)
    # -- parse args and pre-process if needed
    args = parser.parse_args()
    args.configuration = None
    return args

def sigint_handler():
    '''Handles user interrupt signal
    '''
    app_log.warning("\nOuch... you just killed me... (x_x)")
    loop = get_event_loop()
    loop.stop()
    loop.close()

async def main():
    '''Main function
    '''
    app_log.info(__banner__)
    args = parse_args()
    log_enable_debug(args.debug)
    format_enable_colors(not args.no_color)
    app_log.debug(args)
    api = MKCTFAPI(args.repo_root)
    try:
        rcode = 0 if await args.func(api, args) else 1
    except:
        app_log.exception("Ouch... unhandled exception... (>_<)")
        rcode = 2
    return rcode

def app():
    '''mkctf-cli script entry point
    '''
    loop = get_event_loop()
    loop.add_signal_handler(SIGINT, sigint_handler)
    loop.add_signal_handler(SIGTERM, sigint_handler)
    rcode = loop.run_until_complete(main())
    loop.close()
    return rcode
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    exit(app())
