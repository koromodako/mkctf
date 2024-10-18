"""mkctf command line interface
"""

from argparse import ArgumentParser
from asyncio import get_event_loop
from sys import exit as sys_exit

from . import version
from .api import create_mkctf_api
from .command import setup_commands
from .helper.argparse import generic_add_arguments, generic_parse_args
from .helper.exception import MKCTFAPIException
from .helper.logging import LOGGER
from .helper.signal import setup_signals_handler


def parse_args():
    """Parse command line arguments"""
    parser = ArgumentParser(description="A CLI to manage a mkCTF repository")
    generic_add_arguments(parser)
    parser.add_argument(
        '--yes',
        '-y',
        action='store_true',
        help="some operations will stop asking for confirmation",
    )
    # -- add subparsers
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    setup_commands(subparsers)
    # -- parse args and pre-process if needed
    return generic_parse_args(parser)


async def main():
    """Main function"""
    LOGGER.info("MKCTF CLI %s", version)
    args = parse_args()
    try:
        mkctf_api = create_mkctf_api(args.repository_directory)
        returncode = 0 if await args.func(mkctf_api, args) else 1
    except MKCTFAPIException as exc:
        LOGGER.critical("%s", exc.args[0])
        returncode = 1
    except:
        LOGGER.exception("unexpected exception caught in main... (>_<)")
        returncode = 2
    return returncode


def app():
    """mkctf-cli script entry point"""
    loop = get_event_loop()
    setup_signals_handler(loop)
    returncode = loop.run_until_complete(main())
    loop.close()
    return returncode


if __name__ == '__main__':
    sys_exit(app())
