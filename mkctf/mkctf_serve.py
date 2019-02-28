#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#===============================================================================
#  IMPORTS
#===============================================================================
from pathlib import Path
from argparse import ArgumentParser
from aiohttp import web
from mkctf import __banner__
from mkctf.api import MKCTFAPI
from mkctf.helper.log import app_log, log_enable_debug
from mkctf.web_handler import MKCTFWebHandler
from mkctf.helper.formatting import format_enable_colors
# =============================================================================
#  FUNCTIONS
# =============================================================================
def parse_args():
    '''Parse command line arguments
    '''
    parser = ArgumentParser(add_help=True,
                       description="Manage CTF challenges repository.")
    parser.add_argument('--debug', '-d', action='store_true', help="output debug messages")
    parser.add_argument('--repo-root', '-r', type=Path, default=Path.cwd(), help="repository's root folder absolute path.")
    parser.add_argument('--no-color', action='store_true', help="disable colored output")
    # -- parse args and pre-process if needed
    args = parser.parse_args()
    args.configuration = None
    return args

def main():
    '''Main function
    '''
    app_log.info(__banner__)
    args = parse_args()
    log_enable_debug(args.debug)
    format_enable_colors(not args.no_color)
    api = MKCTFAPI(args.repo_root)
    handler = MKCTFWebHandler(api)
    app = web.Application()
    app.add_routes([
        web.get(r'/challenges', handler.enum_challenges),
        web.get(r'/{slug:[a-z0-9\-]+}/status', handler.challenge_status),
        web.post(r'/{slug:[a-z0-9\-]+}/check-flag', handler.check_challenge_flag),
    ])
    app_log.info(f"serving from {args.repo_root}")
    web.run_app(app)

def app():
    '''mkctf-cli script entry point
    '''
    main()
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    app()
