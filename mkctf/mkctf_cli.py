#!/usr/bin/env python3
# -!- encoding:utf8 -!-
# ===============================================================================
#  IMPORTS
# ===============================================================================
from asyncio import get_event_loop
from mkctf import version
from mkctf.api import MKCTFAPI
from mkctf.exception import MKCTFAPIException
from mkctf.cli.command import *
from mkctf.helper.log import app_log
from mkctf.helper.signal import setup_signals_handler
from mkctf.helper.argument_parser import MKCTFArgumentParser

# =============================================================================
#  GLOBALS
# =============================================================================
BANNER = r"""
           _     ____ _____ _____    ____ _     ___
 _ __ ___ | | __/ ___|_   _|  ___|  / ___| |   |_ _|
| '_ ` _ \| |/ / |     | | | |_    | |   | |    | |
| | | | | |   <| |___  | | |  _|   | |___| |___ | |
|_| |_| |_|_|\_\\____| |_| |_|      \____|_____|___| v{}
""".format(
    version
)
# =============================================================================
#  FUNCTIONS
# =============================================================================
def parse_args():
    """Parse command line arguments"""
    parser = MKCTFArgumentParser(
        banner=BANNER, description="A CLI to manage a mkCTF repository"
    )
    parser.add_argument(
        '-y',
        '--yes',
        action='store_true',
        help="some operations will stop asking for confirmation",
    )
    # -- add subparsers
    subparsers = parser.add_subparsers(dest='command', metavar='COMMAND')
    subparsers.required = True
    setup_init(subparsers)
    setup_enum(subparsers)
    setup_create(subparsers)
    setup_enable(subparsers)
    setup_disable(subparsers)
    setup_renew_flag(subparsers)
    setup_update_meta(subparsers)
    setup_configure(subparsers)
    setup_build(subparsers)
    setup_deploy(subparsers)
    setup_healthcheck(subparsers)
    setup_delete(subparsers)
    setup_export(subparsers)
    setup_push(subparsers)
    # -- parse args and pre-process if needed
    return parser.parse_args()


async def main():
    """Main function"""
    args = parse_args()
    try:
        api = MKCTFAPI(args.repo_dir)
        rcode = 0 if await args.func(api, args) else 1
    except MKCTFAPIException as exc:
        app_log.critical("critical error: %s", exc.args[0])
        rcode = 1
    except:
        app_log.exception("Ouch... unhandled exception... (>_<)")
        rcode = 2
    return rcode


def app():
    """mkctf-cli script entry point"""
    loop = get_event_loop()
    setup_signals_handler(loop)
    rcode = loop.run_until_complete(main())
    loop.close()
    return rcode


# =============================================================================
#  SCRIPT
# =============================================================================
if __name__ == '__main__':
    exit(app())
