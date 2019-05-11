#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#===============================================================================
#  IMPORTS
#===============================================================================
from aiohttp import web
from mkctf import __version__
from mkctf.api import MKCTFAPI
from mkctf.helper.log import app_log
from mkctf.web_handler import MKCTFWebHandler
from mkctf.helper.argument_parser import MKCTFArgumentParser
# =============================================================================
#  GLOBALS
# =============================================================================
BANNER = r"""
           _     ____ _____ _____   ____
 _ __ ___ | | __/ ___|_   _|  ___| / ___|  ___ _ ____   _____ _ __
| '_ ` _ \| |/ / |     | | | |_    \___ \ / _ \ '__\ \ / / _ \ '__|
| | | | | |   <| |___  | | |  _|    ___) |  __/ |   \ V /  __/ |
|_| |_| |_|_|\_\\____| |_| |_|     |____/ \___|_|    \_/ \___|_|   v{}

""".format(__version__)
# =============================================================================
#  FUNCTIONS
# =============================================================================
def main():
    '''Main function
    '''
    parser = MKCTFArgumentParser(BANNER, "An HTTP API to perform operations on a mkCTF repository.")
    args = parser.parse_args()
    api = MKCTFAPI(args.repo_dir)
    handler = MKCTFWebHandler(api)
    app = web.Application()
    app.add_routes([
        web.get(r'/challenges', handler.enum_challenges),
        web.get(r'/{slug:[a-z0-9\-]+}/health', handler.challenge_status),
        web.post(r'/{slug:[a-z0-9\-]+}/check-flag', handler.check_challenge_flag),
    ])
    app_log.info(f"serving from {args.repo_dir}")
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
