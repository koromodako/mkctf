"""enum command
"""

from ..helper.display import display_challenge_api
from ..helper.logging import LOGGER


async def enum(mkctf_api, args):
    """Enumerates challenges"""
    found = False
    for challenge_api in mkctf_api.enum(
        tags=args.tags, categories=args.categories, slug=args.slug
    ):
        found = True
        display_challenge_api(challenge_api, args.summarize)
    if not found:
        LOGGER.warning("no challenge found")
    return found


def setup_enum(subparsers):
    """Setup enum command"""
    parser = subparsers.add_parser('enum', help="enumerate challenges")
    parser.add_argument(
        '--summarize',
        action='store_true',
        help="print a list of challenges without details",
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
    parser.set_defaults(func=enum)
