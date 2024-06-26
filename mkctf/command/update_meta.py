"""update-meta command
"""

from ..helper.logging import LOGGER


async def update_meta(mkctf_api, args):
    """update-meta command"""
    updated = list(
        mkctf_api.update_meta(
            tags=args.tags, categories=args.categories, slug=args.slug
        )
    )
    if updated:
        LOGGER.info("challenge metadata updated")
    else:
        LOGGER.warning("no challenge metadata updated")
    return bool(updated)


def setup_update_meta(subparsers):
    """Setup update-meta command"""
    parser = subparsers.add_parser(
        'update-meta',
        help="update challenge metadata. You might want to run this command after reconfiguring the repository",
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
        help="category of challenge to include, can appear multiple times.",
    )
    parser.add_argument('-s', '--slug', help="challenge's slug.")
    parser.set_defaults(func=update_meta)
