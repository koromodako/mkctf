"""mkctf monitor
"""

from argparse import ArgumentParser
from asyncio import get_event_loop
from getpass import getpass
from os import getenv
from sys import exit as sys_exit

from yarl import URL

from . import version
from .api import create_mkctf_api
from .helper.argparse import generic_add_arguments, generic_parse_args
from .helper.exception import MKCTFAPIException
from .helper.logging import LOGGER
from .helper.signal import setup_signals_handler
from .monitoring import MKCTFMonitor, MonitorNotifier


def parse_args():
    """Parse command line arguments"""
    parser = ArgumentParser(
        description="A tool to monitor CTF challenges running cron-like healthchecks",
    )
    generic_add_arguments(parser)
    # -- add arguments
    parser.add_argument(
        '--host',
        default=getenv('MKCTF_API_HOST', 'dashboard.example.ctf'),
        help="dashboard API host, overrides MKCTF_API_HOST (env)",
    )
    parser.add_argument(
        '--port',
        default=int(getenv('MKCTF_API_PORT', '443')),
        type=int,
        help="dashboard API port, overrides MKCTF_API_PORT (env)",
    )
    parser.add_argument(
        '--username',
        '-u',
        default=getenv('MKCTF_API_USER'),
        help="dashboard API username, overrides MKCTF_API_USER (env)",
    )
    parser.add_argument(
        '--count',
        default=-1,
        type=int,
        help="maximum execution count for each task, -1 means infinite",
    )
    parser.add_argument(
        '--delay',
        default=600,
        type=int,
        help="minimum interval between two execution of the same task (in seconds)",
    )
    parser.add_argument(
        '--timeout',
        default=480,
        type=int,
        help="maximum execution time for a task (in seconds)",
    )
    parser.add_argument(
        '--worker',
        default=4,
        type=int,
        help="count of workers to be spawned",
    )
    parser.add_argument(
        '--post-timeout',
        default=60,
        type=int,
        help="timeout for post request to the dashboard API (in seconds)",
    )
    parser.add_argument(
        '--no-verify-ssl',
        action='store_true',
        help="disable dashboard API SSL checks, using this option is strongly discouraged",
    )
    # -- parse args and pre-process if needed
    return generic_parse_args(parser)


async def async_app():
    """Main function"""
    LOGGER.info("MKCTF Monitor %s", version)
    args = parse_args()
    args.username = args.username or input("Dashboard API username: ")
    args.password = getenv('MKCTF_API_PSWD') or getpass(
        "Dashboard API password: "
    )
    try:
        mkctf_api = create_mkctf_api(args.repository_directory)
        notifier = MonitorNotifier(
            base_url=URL.build(scheme='https', host=args.host, port=args.port),
            username=args.username,
            password=args.password,
            timeout=args.post_timeout,
            ssl=(not args.no_verify_ssl),
        )
        monitor = MKCTFMonitor(
            mkctf_api=mkctf_api,
            notifier=notifier,
            count=args.count,
            delay=args.delay,
            timeout=args.timeout,
            worker=args.worker,
        )
        await monitor.run()
        returncode = 0
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
    returncode = loop.run_until_complete(async_app())
    loop.close()
    return returncode


if __name__ == '__main__':
    sys_exit(app())
