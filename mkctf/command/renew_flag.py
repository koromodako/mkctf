"""renew-flag command
"""

from ..api import FLAG_SIZE
from ..helper.cli import Answer, confirm
from ..helper.logging import LOGGER


async def renew_flag(mkctf_api, args):
    """renew-flag command"""
    if (
        not args.yes
        and confirm('do you really want to renew flags?') == Answer.NO
    ):
        LOGGER.warning("operation cancelled by user")
        return False
    renewed = list(
        mkctf_api.renew_flag(
            tags=args.tags,
            categories=args.categories,
            slug=args.slug,
            size=args.size,
        )
    )
    if renewed:
        LOGGER.info("challenge flag renewed")
    else:
        LOGGER.warning("no challenge flag renewed")
    return bool(renewed)


def setup_renew_flag(subparsers):
    """Setup renew-flag command"""
    parser = subparsers.add_parser(
        'renew-flag',
        help="renew flags. You might want to build and deploy/export after that",
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
        '--size',
        type=int,
        default=FLAG_SIZE,
        help="flag's random string size (in bytes)",
    )
    parser.set_defaults(func=renew_flag)
