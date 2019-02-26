#!/usr/bin/env python3
# -!- encoding:utf8 -!-
'''
file:    main.py
date:    2018-07-31
author:  koromodako
purpose:
      This is a framework designed to create challenges and maintain them.
      Entry point script.
'''
#===============================================================================
#  IMPORTS
#===============================================================================
from sys import stderr
from json import dumps
from signal import SIGINT, SIGTERM
from asyncio import get_event_loop
from mkctf import __banner__
from mkctf.api import MKCTFAPI
from mkctf.helper.log import app_log, log_enable_debug
from mkctf.helper.formatting import format_disable_colors
# =============================================================================
#  FUNCTIONS
# =============================================================================
def parse_args():
    '''Parse command line arguments
    '''
    parser = ArgumentParser(add_help=True,
                       description="Manage CTF challenges repository.")
    parser.add_argument('--debug', '-d', action='store_true', help="output debug messages")
    parser.add_argument('--no-color', action='store_true', help="disable colored output")
    parser.add_argument('--repo-root', '-r', type=Path, default=Path.cwd(), help="repository's root folder absolute path.")
    parser.add_argument('--yes', '-y', action='store_true', help="do not ask for confirmation.")
    # -- add subparsers
    sps = parser.add_subparsers(dest='command', metavar='COMMAND')
    sps.required = True
    # ---- init
    init_p = sps.add_parser('init', help="initialize mkctf repository.")
    init_p.set_defaults(func=init)
    # ---- list
    show_p = sps.add_parser('list', help="list challenges.")
    show_p.add_argument('--tags', '-t', action='append', default=[], help="challenge's tags.")
    show_p.add_argument('--slug', '-s', help="challenge's slug.")
    show_p.set_defaults(func=show)
    # ---- create
    create_p = sps.add_parser('create', help="create a challenge.")
    create_p.set_defaults(func=create)
    # ---- delete
    delete_p = sps.add_parser('delete', help="delete a challenge.")
    delete_p.add_argument('slug', help="challenge's slug.")
    delete_p.set_defaults(func=delete)
    # ---- configure
    configure_p = sps.add_parser('configure', help="edits repository's config "
                                                   "or challenge's config.")
    configure_p.add_argument('--slug', '-s', help="challenge's slug.")
    configure_p.set_defaults(func=configure)
    # ---- enable
    enable_p = sps.add_parser('enable', help="enable a challenge.")
    enable_p.add_argument('slug', help="challenge's slug.")
    enable_p.set_defaults(func=enable)
    # ---- disable
    disable_p = sps.add_parser('disable', help="disable a challenge.")
    disable_p.add_argument('slug', help="challenge's slug.")
    disable_p.set_defaults(func=disable)
    # ---- export
    export_p = sps.add_parser('export', help="export enabled static challenges.")
    export_p.add_argument('export_dir', type=Path, help="folder where archives must be written. If the folder does not exist it will be created.")
    export_p.add_argument('--tags', '-t', action='append', default=[], help="challenge's tags.")
    export_p.add_argument('--slug', '-s', help="challenge's slug.")
    export_p.add_argument('--include-disabled', action='store_true', help="export disabled challenges too.")
    export_p.set_defaults(func=export)
    # ---- renew-flag
    renew_flag_p = sps.add_parser('renew-flag',
                                   help="renew flags. You might want to build and deploy/export after that.")
    renew_flag_p.add_argument('--tags', '-t', action='append', default=[], help="challenge's tags.")
    renew_flag_p.add_argument('--slug', '-s', help="challenge's slug.")
    renew_flag_p.add_argument('--size', type=int, default=DEFAULT_SIZE, help="flag's random string size (in bytes).")
    renew_flag_p.set_defaults(func=renew_flag)
    # ---- build
    build_p = sps.add_parser('build', help="build challenges. After building challenges you might want to deploy/export.")
    build_p.add_argument('--tags', '-t', action='append', default=[], help="challenge's tags.")
    build_p.add_argument('--slug', '-s', help="challenge's slug.")
    build_p.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, help="override default timeout for subprocesses.")
    build_p.set_defaults(func=build)
    # ---- deploy
    deploy_p = sps.add_parser('deploy', help="deploy challenges.")
    deploy_p.add_argument('--tags', '-t', action='append', default=[], help="challenge's tags.")
    deploy_p.add_argument('--slug', '-s', help="challenge's slug.")
    deploy_p.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, help="override default timeout for subprocesses.")
    deploy_p.set_defaults(func=deploy)
    # ---- status
    status_p = sps.add_parser('status', help="check deployed challenge's status using exploit/exploit.")
    status_p.add_argument('--tags', '-t', action='append', default=[], help="challenge's tags.")
    status_p.add_argument('--slug', '-s', help="challenge's slug.")
    status_p.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT, help="override default timeout for subprocesses.")
    status_p.set_defaults(func=status)
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
    stderr.write(__banner__)
    args = parse_args()

    log_enable_debug(args.debug)
    if args.no_color:
        format_disable_colors()

    api = MKCTFAPI(args.repo_root)

    success = await api.perform(args)

    if isinstance(success, dict):
        print(dumps(success))
        success = True

    return 0 if success else 1

def app():
    '''mkctf-cli script entry point
    '''
    loop = get_event_loop()
    loop.add_signal_handler(SIGINT, sigint_handler)
    loop.add_signal_handler(SIGTERM, sigint_handler)
    loop.run_until_complete(main())
# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    app()
