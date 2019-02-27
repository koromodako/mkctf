#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#===============================================================================
#  IMPORTS
#===============================================================================
from mkctf.web_handler import MKCTFWebHandler
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
        web.get(r'/{slug:[a-z0-9\-]+}/status'),
        web.post(r'/{slug:[a-z0-9\-]+}/check-flag'),
    ])
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
