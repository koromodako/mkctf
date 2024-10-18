"""push command
"""

from getpass import getpass
from os import getenv

from yarl import URL

from ..helper.logging import LOGGER


async def push(mkctf_api, args):
    """Creates a challenge"""
    username = args.username or input("Dashboard API username: ")
    password = getenv('MKCTF_API_PSWD') or getpass("Dashboard API password: ")
    pushed, reason = await mkctf_api.push(
        base_url=URL.build(scheme='https', host=args.host, port=args.port),
        tags=args.tags,
        categories=args.categories,
        username=username,
        password=password,
        no_verify_ssl=args.no_verify_ssl,
    )
    if pushed:
        LOGGER.info("challenges configurations pushed to dashboard API")
    else:
        LOGGER.warning("operation failed: %s", reason)
    return pushed


def setup_push(subparsers):
    """Setup push command"""
    parser = subparsers.add_parser(
        'push', help="push challenges configuration to the dashboard API"
    )
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
        '--tag',
        '-t',
        action='append',
        default=[],
        dest='tags',
        metavar='TAG',
        help="tag of challenges to include, can appear multiple times",
    )
    parser.add_argument(
        '--category',
        '-c',
        action='append',
        default=[],
        dest='categories',
        metavar='CATEGORY',
        help="category of challenge to include, can appear multiple times",
    )
    parser.add_argument(
        '--username',
        '-u',
        default=getenv('MKCTF_API_USER'),
        help="dashboard API username, overrides MKCTF_API_USER (env)",
    )
    parser.add_argument(
        '--no-verify-ssl',
        action='store_true',
        help="disable SSL checks. Using this option is strongly discouraged",
    )
    parser.set_defaults(func=push)
