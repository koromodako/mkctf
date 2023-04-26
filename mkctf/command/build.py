"""build command
"""
from ..helper.cli import Answer, confirm
from ..helper.logging import LOGGER
from ..helper.display import display_cpr
from ..helper.subprocess import DEFAULT_PROG_TIMEOUT, CalledProcessState


async def build(mkctf_api, args):
    """Builds at least one challenge"""
    if (
        not args.yes
        and confirm('do you really want to perform a build?') == Answer.NO
    ):
        LOGGER.warning("operation cancelled by user.")
        return False
    success = True
    async for slug, cpr in mkctf_api.build(
        tags=args.tags,
        categories=args.categories,
        slug=args.slug,
        dev=args.dev,
        timeout=args.timeout,
    ):
        display_cpr(slug, cpr)
        if cpr.returnstate == CalledProcessState.EXCEPTION:
            success = False
    return success


def setup_build(subparsers):
    """Setup build command"""
    parser = subparsers.add_parser(
        'build',
        help="build challenges. After building challenges you might want to deploy/export",
    )
    parser.add_argument(
        '--dev',
        action='store_true',
        help="runs the script in development mode",
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
    parser.add_argument('-s', '--slug', help="challenge's slug")
    parser.add_argument(
        '--timeout',
        type=int,
        default=DEFAULT_PROG_TIMEOUT,
        help="override default timeout for subprocesses",
    )
    parser.set_defaults(func=build)
